#!/usr/bin/env python3
"""mlir-to-qir  —  command-line MLIR → QIR translator

Usage examples
──────────────
  # Translate a file (QIR to stdout, metadata to stderr)
  python translate.py examples/mlir/bell_state.mlir

  # Read MLIR from stdin
  cat circuit.mlir | python translate.py -

  # Write QIR to a file (metadata printed to stdout)
  python translate.py circuit.mlir -o circuit.ll

  # Use the agentic pipeline with a local Ollama model
  python translate.py circuit.mlir --model llama3.1-8b

  # Use the free GPT-OSS model via HuggingFace (requires HF_TOKEN)
  python translate.py circuit.mlir --model gpt-oss-20b

  # Skip simulation verification (faster)
  python translate.py circuit.mlir --no-verify

  # Output everything as JSON (great for scripting / CI)
  python translate.py circuit.mlir --json

  # List all available LLM model keys
  python translate.py --list-models
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# ── Bootstrap project path ─────────────────────────────────────────────────────
_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "src"))

# ── ANSI colour helpers ────────────────────────────────────────────────────────
_USE_COLOUR = True


def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _USE_COLOUR else text


def GREEN(t: str)  -> str: return _c("32", t)
def RED(t: str)    -> str: return _c("31", t)
def YELLOW(t: str) -> str: return _c("33", t)
def CYAN(t: str)   -> str: return _c("36", t)
def BOLD(t: str)   -> str: return _c("1",  t)
def DIM(t: str)    -> str: return _c("2",  t)


# ── Run-info report writer ─────────────────────────────────────────────────────

def _write_run_info(
    *,
    source_label: str,
    model_key: str,
    mlir_code: str,
    qir_code: str,
    dialect: str,
    translation_path: str,
    translation_time_s: float,
    iterations: int,
    success: bool,
    error_message: str | None,
    gate_comparison: dict,
    verification_result: "dict | None",
    shots: int,
) -> None:
    """Write a detailed markdown run report to example_run_info/."""
    from datetime import datetime

    now = datetime.now()
    ts = now.strftime("%Y%m%d_%H%M%S")

    # Derive a short slug from source label (filename stem or 'stdin')
    import re
    slug = re.sub(r"[^a-zA-Z0-9_-]", "_", Path(source_label).stem if source_label != "-" else "stdin")
    filename = f"run_cli_{slug}_{ts}.md"
    out_dir = _ROOT / "example_run_info"
    out_dir.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────────────
    lines += [
        f"# CLI Translation Run — `{slug}`",
        "",
        f"- **Date**: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **Source**: `{source_label}`",
        f"- **Model**: `{model_key if model_key else 'deterministic (no LLM)'}`",
        f"- **Dialect**: `{dialect}`",
        f"- **Translation Path**: `{translation_path}`",
        f"- **Iterations**: {iterations}",
        f"- **Translation Time**: {translation_time_s * 1000:.1f} ms" if translation_time_s < 1.0
            else f"- **Translation Time**: {translation_time_s:.2f} s",
        f"- **Simulation Shots**: {shots}",
        f"- **Overall Result**: {'✅ SUCCESS' if success else '❌ NOT VERIFIED'}",
        "",
        "---",
        "",
    ]

    # ── Gate Comparison ──────────────────────────────────────────────────────────
    lines += ["## Gate Comparison", ""]
    gc = gate_comparison or {}
    mlir_gates: dict = gc.get("mlir_gates", {})
    qir_gates:  dict = gc.get("qir_gates",  {})
    all_gates = sorted(set(mlir_gates) | set(qir_gates))

    if all_gates:
        lines += ["| Gate | MLIR | QIR | Status |", "|------|------|-----|--------|"]
        for g in all_gates:
            mc, qc = mlir_gates.get(g, 0), qir_gates.get(g, 0)
            status = "✅ match" if mc == qc else "❌ mismatch"
            lines.append(f"| `{g}` | {mc} | {qc} | {status} |")
        mt = gc.get("mlir_total", sum(mlir_gates.values()))
        qt = gc.get("qir_total",  sum(qir_gates.values()))
        total_status = "✅ match" if mt == qt else "❌ mismatch"
        lines += [
            f"| **Total** | **{mt}** | **{qt}** | **{total_status}** |",
            "",
        ]
        if gc.get("discrepancies"):
            lines += ["**Discrepancies:**", ""]
            for d in gc["discrepancies"]:
                diff = d["difference"]
                lines.append(f"- `{d['gate']}`: MLIR={d['mlir_count']}, QIR={d['qir_count']} (diff {'+' if diff > 0 else ''}{diff})")
            lines.append("")
    else:
        lines += ["*(no gate data available)*", ""]

    lines.append("---")
    lines.append("")

    # ── Verification Results ─────────────────────────────────────────────────────
    lines += ["## Verification Results", ""]
    if verification_result and verification_result.get("success"):
        vr = verification_result
        gate_match = vr.get("gate_comparison", {}).get("matches", False)
        sim_pass   = vr.get("similarity_passes", False)
        sim_pct    = vr.get("similarity", 0.0) * 100
        qir_lbl  = "mock" if vr.get("qir_is_mock")      else "real execution"
        mlir_lbl = "mock" if vr.get("catalyst_is_mock") else "real execution"
        runner   = vr.get("mlir_runner_label", "MLIR runner")

        lines += [
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| QIR backend | {qir_lbl} |",
            f"| MLIR backend | {runner} ({mlir_lbl}) |",
            f"| Gate match | {'✅ PASS' if gate_match else '❌ FAIL'} |",
            f"| TVD similarity | {sim_pct:.1f}% — {'✅ PASS' if sim_pass else '❌ FAIL (need ≥ 95%)'} |",
            "",
        ]

        qir_dist  = vr.get("qir_distribution", {})
        mlir_dist = vr.get("catalyst_distribution", {})
        if qir_dist or mlir_dist:
            lines += ["### Distribution Comparison", "", "| Outcome | QIR Count | MLIR Count |", "|---------|-----------|------------|"]
            all_keys = sorted(set(qir_dist) | set(mlir_dist))
            for k in all_keys:
                lines.append(f"| `{k}` | {qir_dist.get(k, 0)} | {mlir_dist.get(k, 0)} |")
            lines.append("")
    elif error_message:
        lines += [f"⚠️ {error_message}", ""]
    else:
        lines += ["*(verification not run)*", ""]

    lines.append("---")
    lines.append("")

    # ── Iteration History ────────────────────────────────────────────────────────
    # (only for agentic runs that expose iteration history via model_key)
    if model_key and iterations > 1:
        lines += [f"## Agent Iterations", "", f"Total refinement iterations: **{iterations}**", ""]
        lines.append("---")
        lines.append("")

    # ── MLIR Input ───────────────────────────────────────────────────────────────
    lines += ["## MLIR Input", "", "```mlir", mlir_code.rstrip(), "```", "", "---", ""]

    # ── QIR Output ───────────────────────────────────────────────────────────────
    lines += ["## QIR Output", "", "```llvm", qir_code.rstrip() if qir_code else "(none)", "```", ""]

    out_path = out_dir / filename
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return str(out_path)


# ── Metadata renderer ──────────────────────────────────────────────────────────

def _print_metadata(
    stream,
    *,
    dialect: str,
    translation_path: str,
    translation_time_s: float,
    iterations: int,
    gate_comparison: dict,
    verification_result: "dict | None",
    success: bool,
) -> None:
    """Print human-readable translation metadata to *stream*."""

    def w(*args, **kwargs):
        print(*args, file=stream, **kwargs)

    w()
    w(BOLD("── Translation Metadata " + "─" * 28))
    w(f"  Dialect          : {CYAN(dialect)}")

    path_colours = {
        "deterministic":        GREEN("deterministic"),
        "ai_agent":             CYAN("ai_agent"),
        "deterministic+repair": YELLOW("deterministic+repair"),
    }
    w(f"  Translation path : {path_colours.get(translation_path, translation_path)}")

    time_str = (
        f"{translation_time_s * 1000:.1f} ms"
        if translation_time_s < 1.0
        else f"{translation_time_s:.2f} s"
    )
    w(f"  Translation time : {time_str}")
    w(f"  Iterations       : {iterations}")

    # Gate count table
    w()
    w(BOLD("── Gate Counts " + "─" * 37))
    gc = gate_comparison or {}
    mlir_gates: dict = gc.get("mlir_gates", {})
    qir_gates:  dict = gc.get("qir_gates",  {})
    all_gates = sorted(set(mlir_gates) | set(qir_gates))

    if all_gates:
        w(f"  {'Gate':<14} {'MLIR':>5} {'QIR':>5}  Status")
        w("  " + "─" * 34)
        for g in all_gates:
            mc = mlir_gates.get(g, 0)
            qc = qir_gates.get(g, 0)
            status = GREEN("✓ match") if mc == qc else RED("✗ mismatch")
            w(f"  {g:<14} {mc:>5} {qc:>5}  {status}")

        mlir_total = gc.get("mlir_total", sum(mlir_gates.values()))
        qir_total  = gc.get("qir_total",  sum(qir_gates.values()))
        total_sym  = GREEN("✓ match") if mlir_total == qir_total else RED("✗ mismatch")
        w("  " + "─" * 34)
        w(f"  {'Total':<14} {mlir_total:>5} {qir_total:>5}  {total_sym}")
    else:
        w("  (no gate data available)")

    if gc.get("discrepancies"):
        w()
        w(BOLD("── Gate Discrepancies " + "─" * 30))
        for d in gc["discrepancies"]:
            diff = d["difference"]
            sign = "+" if diff > 0 else ""
            w(f"  {d['gate']}: MLIR={d['mlir_count']}  QIR={d['qir_count']}  diff={sign}{diff}")

    # Simulation verification
    if verification_result and verification_result.get("success"):
        vr = verification_result
        w()
        w(BOLD("── Simulation Verification " + "─" * 25))
        qir_lbl  = "mock" if vr.get("qir_is_mock")      else "real"
        mlir_lbl = "mock" if vr.get("catalyst_is_mock") else "real"
        runner   = vr.get("mlir_runner_label", "MLIR runner")
        w(f"  QIR backend      : {qir_lbl} execution")
        w(f"  MLIR backend     : {runner} ({mlir_lbl} execution)")

        gate_match = vr.get("gate_comparison", {}).get("matches", False)
        sim_pass   = vr.get("similarity_passes", False)
        sim_pct    = vr.get("similarity", 0.0) * 100
        w(f"  Gate match       : {GREEN('PASS') if gate_match else RED('FAIL')}")
        w(f"  TVD similarity   : {sim_pct:.1f}%  {GREEN('PASS') if sim_pass else RED('FAIL (need ≥ 95%)')}")

        qir_dist = vr.get("qir_distribution", {})
        if qir_dist:
            dist_str = "  ".join(f"{k}:{v}" for k, v in sorted(qir_dist.items()))
            w(f"  QIR distribution : {dist_str}")
        mlir_dist = vr.get("catalyst_distribution", {})
        if mlir_dist:
            dist_str = "  ".join(f"{k}:{v}" for k, v in sorted(mlir_dist.items()))
            w(f"  MLIR distribution: {dist_str}")

    # Overall status banner
    w()
    if success:
        w(BOLD(GREEN("✓ SUCCESS")) + " — translation verified")
    else:
        w(BOLD(YELLOW("⚠ DONE")) + " — translation complete (verification may not have fully passed)")
    w()


# ── Translation functions ──────────────────────────────────────────────────────

def _run_deterministic(mlir_code: str) -> dict:
    """Parse + generate deterministically (no LLM)."""
    from src.parsers.mlir_parser import MLIRParser
    from src.generators.qir_generator import QIRGenerator

    parser = MLIRParser()
    detected_dialect = parser.get_detected_dialect(mlir_code)   # raises UnsupportedDialectError
    circuit = parser.parse(mlir_code)
    qir_code = QIRGenerator().generate(circuit, module_id="translated-circuit")
    return {
        "qir_code":         qir_code,
        "dialect":          detected_dialect,
        "translation_path": "deterministic",
        "iterations":       1,
        "success":          True,
        "error_message":    None,
        "verification_result": None,
    }


def _build_llm(model_key: str):
    """Construct a crewai LLM object for the given model key."""
    from src.config.llm_config import LLMConfig
    from src.config.settings import settings
    from crewai.llm import LLM

    model_info = LLMConfig.get_model_info(model_key)
    if model_info is None:
        raise ValueError(
            f"Unknown model key '{model_key}'. "
            "Run `python translate.py --list-models` to see available keys."
        )

    if model_info.provider == "huggingface":
        token = os.environ.get(model_info.api_key_env, "")
        if not token:
            raise RuntimeError(
                f"HF_TOKEN not set. "
                f"Get a free token at https://huggingface.co/settings/tokens "
                f"then: export {model_info.api_key_env}=hf_..."
            )
        return LLM(
            model=model_info.get_litellm_model(),
            api_key=token,
            temperature=settings.LLM_TEMPERATURE,
        )

    if model_info.provider == "openai":
        api_key = os.environ.get(model_info.api_key_env, "")
        if not api_key:
            raise RuntimeError(
                f"API key not found. export {model_info.api_key_env}=<your-key>"
            )
        return LLM(
            model=model_info.get_litellm_model(),
            api_key=api_key,
            temperature=settings.LLM_TEMPERATURE,
        )

    # Ollama
    import ollama as _ollama
    _ollama.list()   # raises ConnectionError if server is down
    return LLM(
        model=LLMConfig.get_litellm_model(model_key),
        base_url=settings.LLM_BASE_URL,
        temperature=settings.LLM_TEMPERATURE,
    )


def _run_agentic(
    mlir_code: str,
    model_key: str,
    max_iterations: int,
    shots: int,
    force_agentic: bool = False,
) -> dict:
    """Full agentic pipeline: translate + simulation-verified repair loop."""
    from src.agents.crew_manager import CrewManager

    llm = _build_llm(model_key)
    manager = CrewManager(llm=llm, max_iterations=max_iterations, verbose=False)
    tr = manager.translate_with_verification(mlir_code, shots=shots, force_agentic=force_agentic)
    return {
        "qir_code":            tr.qir_code or "",
        "dialect":             tr.dialect or "unknown",
        "translation_path":    tr.translation_path,
        "iterations":          tr.iterations,
        "success":             tr.success,
        "error_message":       tr.error_message,
        "verification_result": tr.verification_result,
    }


def _run_agentic_no_verify(mlir_code: str, model_key: str, max_iterations: int) -> dict:
    """Agentic translation without simulation verification (faster)."""
    from src.agents.crew_manager import CrewManager

    llm = _build_llm(model_key)
    manager = CrewManager(llm=llm, max_iterations=max_iterations, verbose=False)
    tr = manager.translate(mlir_code)   # legacy agent-only path
    return {
        "qir_code":            tr.qir_code or "",
        "dialect":             tr.dialect or "unknown",
        "translation_path":    tr.translation_path,
        "iterations":          tr.iterations,
        "success":             tr.success,
        "error_message":       tr.error_message,
        "verification_result": None,
    }


def _gate_comparison_only(mlir_code: str, qir_code: str) -> dict:
    """Compute gate comparison without simulation (used when --no-verify)."""
    from src.verification.gate_counter import GateCounter

    gc = GateCounter()
    mlir_gates = gc.count_mlir_gates(mlir_code)
    mlir_gates.pop("measure", None)
    mlir_gates.pop("mz", None)
    qir_gates = gc.count_qir_gates(qir_code)
    qir_gates.pop("measure", None)
    return gc.compare(mlir_gates, qir_gates)


# ── Argument parser ────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="translate",
        description="Translate an MLIR quantum circuit to QIR.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "input", metavar="FILE|-", nargs="?",
        help="Path to MLIR file, or '-' to read from stdin",
    )
    p.add_argument(
        "-o", "--output", metavar="FILE",
        help=(
            "Write QIR to FILE instead of stdout. "
            "Metadata is then printed to stdout instead of stderr."
        ),
    )
    p.add_argument(
        "--model", metavar="MODEL_KEY", default=None,
        help=(
            "Enable the agentic pipeline with this model key "
            "(e.g. llama3.1-8b, gpt-oss-20b). "
            "Without this flag only the deterministic parser is used."
        ),
    )
    p.add_argument(
        "--max-iterations", type=int, default=5, metavar="N",
        help="Max agent refinement iterations (default: 5, only used with --model)",
    )
    p.add_argument(
        "--shots", type=int, default=1000, metavar="N",
        help="Simulation shots for verification (default: 1000)",
    )
    p.add_argument(
        "--force-agentic", action="store_true",
        help=(
            "Force LLM translation even for known dialects (skip deterministic parser). "
            "Requires --model. Useful for benchmarking LLM performance."
        ),
    )
    p.add_argument(
        "--no-verify", action="store_true",
        help="Skip quantum simulation verification (gate comparison still shown)",
    )
    p.add_argument(
        "--json", action="store_true",
        help="Output everything as a single JSON object to stdout (for scripting/CI)",
    )
    p.add_argument(
        "--no-colour", "--no-color", action="store_true",
        help="Disable ANSI colour codes",
    )
    p.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress all metadata — only QIR is written",
    )
    p.add_argument(
        "--list-models", action="store_true",
        help="Print available LLM model keys and exit",
    )
    return p


def _list_models() -> None:
    from src.config.llm_config import LLMConfig

    print(BOLD("Available model keys:"))
    print()
    for key, info in LLMConfig.MODELS.items():
        provider_tag = f"[{info.provider}]"
        free_tag = " (free tier)" if info.free_tier else ""
        print(f"  {CYAN(key):<30} {DIM(provider_tag):<20} {info.size}, {info.speed}{free_tag}")
        print(f"    {DIM('Use case:')} {info.recommended_for}")
        if info.provider == "ollama":
            print(f"    {DIM('Setup:   ')} ollama pull {info.ollama_name}")
        elif info.provider == "huggingface":
            print(f"    {DIM('Setup:   ')} export {info.api_key_env}=hf_...  (free at huggingface.co/settings/tokens)")
        print()


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> int:
    global _USE_COLOUR

    parser = _build_parser()
    args = parser.parse_args()

    if args.no_colour:
        _USE_COLOUR = False

    if args.list_models:
        _list_models()
        return 0

    if not args.input:
        parser.print_help()
        return 0

    # ── Read MLIR ──────────────────────────────────────────────────────────────
    if args.input == "-":
        if sys.stdin.isatty():
            print("Reading MLIR from stdin (Ctrl-D to finish)…", file=sys.stderr)
        mlir_code = sys.stdin.read()
    else:
        path = Path(args.input)
        if not path.exists():
            print(f"{RED('Error:')} file not found: {args.input}", file=sys.stderr)
            return 1
        mlir_code = path.read_text()

    if not mlir_code.strip():
        print(f"{RED('Error:')} empty input", file=sys.stderr)
        return 1

    # When QIR goes to a file, metadata prints to stdout; otherwise metadata → stderr
    meta_stream = sys.stdout if (args.output or args.json) else sys.stderr

    # ── Translate ──────────────────────────────────────────────────────────────
    t0 = time.time()
    try:
        if args.model:
            if args.no_verify:
                result = _run_agentic_no_verify(mlir_code, args.model, args.max_iterations)
            else:
                result = _run_agentic(
                    mlir_code, args.model, args.max_iterations, args.shots,
                    force_agentic=args.force_agentic,
                )
        else:
            try:
                result = _run_deterministic(mlir_code)
            except Exception as exc:
                from src.dialects.base_dialect import UnsupportedDialectError
                if isinstance(exc, UnsupportedDialectError):
                    print(
                        f"{RED('Error:')} unrecognized MLIR dialect — "
                        "use --model <key> to enable the agentic pipeline "
                        "(run --list-models to see options).",
                        file=sys.stderr,
                    )
                    return 2
                raise

            # Deterministic path — run simulation verification unless skipped
            if not args.no_verify:
                from src.verification.pipeline import run_verification_pipeline
                if not args.quiet and not args.json:
                    print("Running simulation verification…", file=meta_stream)
                result["verification_result"] = run_verification_pipeline(
                    mlir_code, result["qir_code"], shots=args.shots
                )

    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"{RED('Error:')} {exc}", file=sys.stderr)
        return 1

    elapsed = time.time() - t0

    # ── Gate comparison ────────────────────────────────────────────────────────
    # Prefer gate data from verification_result; fall back to standalone counter.
    vr = result.get("verification_result") or {}
    gate_comparison = (
        vr.get("gate_comparison")
        or _gate_comparison_only(mlir_code, result.get("qir_code", ""))
    )

    qir_code = result.get("qir_code", "")

    # ── Write example_run_info/ report (capture filename for JSONL cross-link) ──
    run_info_file: str | None = None
    try:
        run_info_file = _write_run_info(
            source_label=args.input,
            model_key=args.model,
            mlir_code=mlir_code,
            qir_code=qir_code,
            dialect=result.get("dialect", "unknown"),
            translation_path=result.get("translation_path", "deterministic"),
            translation_time_s=elapsed,
            iterations=result.get("iterations", 1),
            success=result.get("success", False),
            error_message=result.get("error_message"),
            gate_comparison=gate_comparison,
            verification_result=result.get("verification_result"),
            shots=args.shots,
        )
        if run_info_file:
            run_info_file = Path(run_info_file).name  # store just the filename
    except Exception:
        pass  # run-info writing must never break the CLI

    # ── Log to translations.jsonl (same format as UI) ──────────────────────────
    try:
        from datetime import datetime
        log_record = {
            "timestamp": datetime.now().isoformat(),
            "session_id": "cli",
            "source": args.input,
            "model": args.model or "deterministic",
            "dialect": result.get("dialect", "unknown"),
            "translation_time_s": elapsed,
            "translation_path": result.get("translation_path", "deterministic"),
            "force_agentic": getattr(args, "force_agentic", False),
            "iterations": result.get("iterations", 1),
            "shots": args.shots,
            "success": result.get("success", False),
            "circuit_info": result.get("circuit_info", {}),
            "run_info_file": run_info_file,  # cross-link to detailed report
            "mlir_input": mlir_code,
            "qir_output": result.get("qir_code", ""),
        }
        log_file = _ROOT / "logs" / "translations.jsonl"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as _lf:
            _lf.write(json.dumps(log_record) + "\n")
    except Exception:
        pass  # logging must never break the CLI

    # ── JSON output ────────────────────────────────────────────────────────────
    if args.json:
        payload = {
            "qir":               qir_code,
            "dialect":           result.get("dialect", "unknown"),
            "translation_path":  result.get("translation_path", "deterministic"),
            "translation_time_s": elapsed,
            "iterations":        result.get("iterations", 1),
            "success":           result.get("success", False),
            "error_message":     result.get("error_message"),
            "gate_comparison":   gate_comparison,
            "verification":      result.get("verification_result"),
        }
        print(json.dumps(payload, indent=2))
        return 0 if result.get("success") else 1

    # ── Human-readable metadata ────────────────────────────────────────────────
    if not args.quiet:
        _print_metadata(
            meta_stream,
            dialect=result.get("dialect", "unknown"),
            translation_path=result.get("translation_path", "deterministic"),
            translation_time_s=elapsed,
            iterations=result.get("iterations", 1),
            gate_comparison=gate_comparison,
            verification_result=result.get("verification_result"),
            success=result.get("success", False),
        )

    # ── Write QIR ─────────────────────────────────────────────────────────────
    if args.output:
        Path(args.output).write_text(qir_code)
        if not args.quiet:
            print(f"QIR written to: {BOLD(args.output)}", file=meta_stream)
    else:
        print(qir_code)

    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
