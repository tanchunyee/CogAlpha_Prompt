"""CogAlpha evolutionary loop: seven-level agents -> quality checker -> fitness -> thinking evolution."""
from __future__ import annotations

import json
import random
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path

import numpy as np
import pandas as pd

from . import data as D
from . import factors as F
from . import metrics as M
from . import prompts as P
from .llm import ClaudeCLI, QuotaExhausted


class Trial:
    def __init__(self, cfg: dict, run_dir: Path, log=print):
        self.cfg, self.run_dir, self.log = cfg, run_dir, log
        run_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = run_dir / "state.json"
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {"agents": {}}

        dc = cfg["data"]
        self.panel = D.load_panel(dc)
        self.label = D.forward_return(self.panel, dc["horizon"])
        dates = self.panel.index.get_level_values("date")
        self.train_mask = np.asarray((dates >= dc["train"][0]) & (dates <= dc["train"][1]))
        # Factors are computed on data up to the end of validation only: the test period stays unseen.
        self.search_panel = self.panel[dates <= pd.Timestamp(dc["valid"][1])]
        self.search_train_mask = self.train_mask[np.asarray(dates <= pd.Timestamp(dc["valid"][1]))]
        self.ctx = {"columns_desc": D.columns_desc(self.panel), "columns_num": self.panel.shape[1],
                    "forecast_horizon": dc["horizon"], "num_per_request": cfg["evolution"]["num_per_request"]}

        lc = cfg["llm"]
        self.llm = ClaudeCLI(P.system_message(), run_dir / "llm_calls.jsonl", lc["timeout_s"], lc["max_calls"])
        self.pool = ThreadPoolExecutor(max_workers=lc["max_parallel"])
        self.rng = random.Random(cfg.get("seed", 0))
        self.names: set[str] = {f["name"] for a in self.state["agents"].values() for f in a["factors"]}
        self.seen = {self._fingerprint(f["name"], f["code"]) for a in self.state["agents"].values() for f in a["factors"]}

    # ---------------------------------------------------------------- LLM roles
    def gen(self, prompt, role):
        lc = self.cfg["llm"]
        return self.llm(prompt, lc["generation_model"], role, lc.get("generation_thinking_tokens"))

    def check(self, prompt, role):
        lc = self.cfg["llm"]
        return self.llm(prompt, lc["checker_model"], role, lc.get("checker_thinking_tokens"))

    # ---------------------------------------------------------------- bookkeeping
    def _unique(self, name: str, code: str) -> tuple[str, str]:
        new, k = name, 2
        while new in self.names:
            new, k = f"{name}_v{k}", k + 1
        self.names.add(new)
        return new, (code if new == name else re.sub(rf"\b{re.escape(name)}\b", new, code))

    @staticmethod
    def _fingerprint(name: str, code: str) -> str:
        body = re.sub(r'""".*?"""|#[^\n]*', "", code.replace(name, "F"), flags=re.S)
        return re.sub(r"\s+", "", body)

    def _candidates(self, text, agent, origin, gen, parents=()) -> list[F.Factor]:
        out = []
        for name, code in F.parse_functions(text):
            if (fp := self._fingerprint(name, code)) in self.seen:  # identical logic already tried
                continue
            self.seen.add(fp)
            name, code = self._unique(name, code)
            out.append(F.Factor(name, code, agent, origin, gen, list(parents)))
        return out

    def _save(self):
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1, default=float))
        tmp.replace(self.state_path)

    # ---------------------------------------------------------------- quality checker
    def qualify(self, f: F.Factor) -> F.Factor:
        """Static -> execute -> numeric -> leakage -> (LLM judge) -> fitness, with repair loops."""
        q = self.cfg["quality"]
        if q["llm_code_quality"]:
            reply = self.check(P.code_quality_prompt(f.code), "code_quality")
            if not reply.lstrip().startswith("The code is correct"):
                self._replace_code(f, reply, "code_quality")
        attempts = 0
        while True:
            err = self._run_checks(f)
            if err is None and q["llm_judge"]:
                verdict = self.check(P.judge_prompt(f.code), "judge")
                if re.search(r"Final Recommendation:\**\s*Reject", verdict, re.I):
                    err = ("judge", verdict)
            if err is None:
                f.status = "evaluated"
                return f
            kind, msg = err
            f.history.append(f"{kind}: {msg[:300]}")
            if attempts >= q["max_repairs"]:
                f.status, f.fail_reason = "failed", f"{kind}: {msg[:300]}"
                return f
            attempts += 1
            prompt = (P.logic_improvement_prompt(self.ctx, f.code, msg) if kind == "judge"
                      else P.repair_prompt(self.ctx, f.code, msg))
            if not self._replace_code(f, self.check(prompt, "logic_improvement" if kind == "judge" else "code_repair"), kind):
                f.status, f.fail_reason = "failed", f"{kind}: repair produced no function"
                return f

    def _replace_code(self, f: F.Factor, reply: str, why: str) -> bool:
        fns = F.parse_functions(reply)
        if not fns:
            return False
        name, code = fns[-1]
        if name != f.name:  # keep the registered name stable
            code = re.sub(rf"\b{re.escape(name)}\b", f.name, code)
        f.code = code
        return True

    def _run_checks(self, f: F.Factor):
        q = self.cfg["quality"]
        if err := F.static_check(f.code):
            return "static", err
        if f.name not in re.findall(r"def\s+(\w+)\s*\(", f.code):
            return "static", f"function must be named {f.name}"
        full, trunc, err = F.execute(f.code, f.name, self.search_panel, q["exec_timeout_s"])
        if err:
            return "runtime", err
        full = full.reindex(self.search_panel.index)
        if err := F.numeric_check(full, self.search_train_mask, q["max_nan_ratio"], q["min_distinct_per_day"]):
            return "numeric", err
        if err := F.leakage_check(full, trunc):
            return "leakage", err
        train = full[self.search_train_mask]
        f.metrics = M.evaluate(train, self.label, self.cfg["fitness"]["mi_samples"])
        return None

    def qualify_all(self, cands: list[F.Factor]) -> list[F.Factor]:
        return list(self.pool.map(self.qualify, cands))

    # ---------------------------------------------------------------- generation operators
    def agent_generate(self, agent, gen, eff, ineff, origin="initial") -> list[F.Factor]:
        _, guidance = P.agent_blocks(agent)
        if self.cfg["evolution"]["diversified_guidance"]:
            style = self.rng.choice(P.PARAPHRASE_STYLES)
            guidance = self.check(P.paraphrase_prompt(guidance, style), f"paraphrase_{style}").strip() or guidance
        prompt = P.generation_prompt(agent, self.ctx, guidance, eff, ineff)
        return self._candidates(self.gen(prompt, f"agent_{agent}"), agent, origin, gen)

    def evolve_child(self, agent, gen, parents: list[F.Factor], extra) -> list[F.Factor]:
        intro = P.agent_intro(agent, {**self.ctx, "num_per_request": 1})
        w = self.cfg["evolution"]["op_weights"]
        op = self.rng.choices(list(w), weights=list(w.values()))[0] if len(parents) > 1 else "mutation"
        if op == "mutation":
            p = self.rng.choice(parents)
            text = self.gen(P.mutation_prompt(intro, extra, p.code), "mutation")
            return self._candidates(text, agent, op, gen, [p.name])[:1]
        p1, p2 = self.rng.sample(parents, 2)
        text = self.gen(P.crossover_prompt(intro, extra, p1.code, p2.code), "crossover")
        if op == "crossover_mutation" and (fns := F.parse_functions(text)):
            text = self.gen(P.mutation_prompt(intro, extra, fns[0][1]), "mutation")
        return self._candidates(text, agent, op, gen, [p1.name, p2.name])[:1]

    def summarise(self, kind, factors: list[F.Factor]) -> str | None:
        if not factors or not self.cfg["evolution"]["adaptive_generation"]:
            return None
        blocks = []
        for i, f in enumerate(factors, 1):
            m = f.metrics
            state = "valid" if kind == "effective" else "low_metrics"
            metr = (f"{m['ic']:.4f} / {m['rank_ic']:.4f} / {m['icir']:.4f} / {m['rank_icir']:.4f}" if m else "n/a")
            blocks.append(f"<<factor {i}>>\nState: {state}\nMetrics: IC / RankIC / ICIR / RankICIR = {metr}\n"
                          f"Code:\n<<function {i}>>\n{f.code}\n<</function {i}>>\n<</factor {i}>>")
        return self.check(P.summary_prompt(kind, blocks), f"{kind}_summary").strip()

    # ---------------------------------------------------------------- main loop
    def run_agent(self, agent: str):
        ev, fit = self.cfg["evolution"], self.cfg["fitness"]
        st = self.state["agents"].setdefault(agent, {"generation": -1, "factors": [], "parents": [], "elite": [],
                                                      "carry": [], "effective": None, "ineffective": None,
                                                      "done": False})
        if st["done"]:
            return
        by_name = {d["name"]: F.Factor(**d) for d in st["factors"]}
        while st["generation"] < ev["generations"]:
            g = st["generation"] + 1
            eff, ineff = st["effective"], st["ineffective"]
            self.log(f"[{agent}] generation {g}/{ev['generations']} (llm calls so far: {self.llm.calls})")
            parents = [by_name[n] for n in st["parents"]]
            if g == 0 or len(parents) < 1:
                jobs = [self.pool.submit(self.agent_generate, agent, g, eff, ineff) for _ in range(ev["initial_requests"])]
            else:
                extra = P.feedback_block(P.agent_blocks(agent)[1], eff, ineff)
                jobs = [self.pool.submit(self.evolve_child, agent, g, parents, extra) for _ in range(ev["children"])]
                if g % ev["inject_every"] == 0:
                    jobs.append(self.pool.submit(self.agent_generate, agent, g, eff, ineff, "inject"))
            cands = [c for j in jobs for c in j.result()]
            done = self.qualify_all(cands)
            for f in done:
                by_name[f.name] = f

            evaluated = [f for f in done if f.status == "evaluated"] + [by_name[n] for n in st["carry"]]
            qualified, elite = M.select({f.name: f.metrics for f in evaluated}, fit)
            ranked = sorted(evaluated, key=lambda f: M.score(f.metrics), reverse=True)
            parent_names = sorted(qualified, key=lambda n: M.score(by_name[n].metrics), reverse=True)[:ev["parent_pool"]]
            if len(parent_names) < 2:  # tiny trial generations: keep the search alive with the best survivors
                parent_names = [f.name for f in ranked[:max(2, len(parent_names))]]
            st["elite"] = sorted(set(st["elite"]) | set(elite))
            st["carry"] = [n for n in parent_names if n in elite][:ev["elite_carry"]]
            st["parents"] = parent_names

            valid = [by_name[n] for n in qualified] or ranked[:1]
            invalid = [f for f in ranked[::-1] if f.name not in qualified]
            k = ev["feedback_samples"]
            st["effective"] = self.summarise("effective", self.rng.sample(valid, min(k, len(valid))))
            st["ineffective"] = self.summarise("ineffective", invalid[:k])

            n_fail = sum(f.status == "failed" for f in done)
            self.log(f"[{agent}] gen {g}: {len(cands)} candidates, {n_fail} failed checks, "
                     f"{len(qualified)} qualified, {len(elite)} elite; best: "
                     + (f"{ranked[0].name} RankIC={ranked[0].metrics['rank_ic']:.4f}" if ranked else "none"))
            st["generation"] = g
            st["factors"] = [asdict(f) for f in by_name.values()]
            self._save()
        st["done"] = True
        self._save()

    def run(self) -> bool:
        """Returns True if all agents finished, False if stopped by quota."""
        try:
            for agent in self.cfg["agents"]:
                self.run_agent(agent)
            return True
        except QuotaExhausted as e:
            self._save()
            self.log(f"Stopped: {e}. State saved; rerun with --resume to continue.")
            return False
        finally:
            self.log(f"LLM calls: {self.llm.calls}, notional API-equivalent cost ${self.llm.cost_usd:.2f}")
