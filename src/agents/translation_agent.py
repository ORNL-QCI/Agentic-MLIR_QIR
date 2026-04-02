"""Translation agent for MLIR to QIR conversion."""

from crewai import Agent, Task
from crewai.tasks.task_output import TaskOutput
from typing import Any, Optional
import json
import logging
import re

from ..tools.qir_reference import get_qir_reference_context
from ..generators.qir_assembler import assemble_qir_from_operations

logger = logging.getLogger(__name__)


# ── QIR output guardrail ───────────────────────────────────────────────────────

def qir_output_guardrail(output: TaskOutput) -> tuple[bool, Any]:
    """CrewAI Task guardrail: validate/transform LLM output into valid QIR.

    Returns (True, qir_string) if output is usable, or (False, error_msg)
    to trigger CrewAI auto-retry with the error as feedback.
    """
    raw = str(output.raw).strip() if output.raw else ""

    # ── 1. LLVM IR (complete or incomplete) ──
    if raw.lstrip().startswith("; ModuleID") or raw.lstrip().startswith("define void"):
        cleaned = _extract_qir(raw)
        if cleaned:
            if _is_complete_qir(cleaned):
                logger.info("Guardrail: output is complete LLVM IR, passing through")
                return (True, cleaned)
            # Incomplete — reassemble from gate calls
            ir_ops = _extract_ops_from_llvm_ir(cleaned)
            if ir_ops:
                logger.info("Guardrail: incomplete LLVM IR, reassembling from %d gate calls", len(ir_ops))
                qir = assemble_qir_from_operations(ir_ops)
                if qir:
                    return (True, qir)

    # ── 2. JSON with operations list — assemble QIR ──
    ops = _extract_operations_from_json(raw)
    if ops:
        logger.info("Guardrail: found %d operations in JSON, assembling QIR", len(ops))
        qir = assemble_qir_from_operations(ops)
        if qir:
            return (True, qir)
        return (False, "Found operations in JSON but assembly failed. "
                "Output the operations as short form: 'h 0', 'cnot 0 1', etc.")

    # ── 3. Tool-call JSON (LLM confused about tool use) ──
    if raw.startswith("{"):
        try:
            obj = json.loads(raw)
            if obj.get("type") == "function" or ("name" in obj and "parameters" in obj):
                return (False, "Do not output tool calls as your final answer. "
                        "Output the QIR translation directly. Either raw LLVM IR "
                        "starting with '; ModuleID' or JSON with an 'operations' list.")
        except (json.JSONDecodeError, TypeError):
            pass

    # ── 4. Try extracting LLVM IR from prose/markdown ──
    cleaned = _extract_qir(raw)
    if cleaned and ("__quantum__" in cleaned or "define void" in cleaned):
        logger.info("Guardrail: extracted LLVM IR from wrapped output")
        return (True, cleaned)

    # ── 5. Nothing usable — reject for retry ──
    return (False,
        "Your output must be one of:\n"
        "Option A (PREFERRED): Raw LLVM IR starting with ; ModuleID = 'quantum_module'\n"
        "Option B: JSON with {\"operations\": [\"h 0\", \"cnot 0 1\", ...], \"num_qubits\": N}\n"
        "Do NOT output prose, tool calls, or incomplete fragments.")


def _extract_operations_from_json(raw: str) -> list[str]:
    """Try to extract an operations list from JSON output.

    Handles formats like:
      {"operations": ["h 0", "cnot 0 1"]}
      {"entry_function": {"operations": ["call void @...", ...]}}
      {"ModuleID": ..., "entry_function": {"operations": [...]}}
    """
    # Try to find JSON in the raw text
    text = raw.strip()

    # Find the first { and matching }
    start = text.find("{")
    if start < 0:
        return []

    # Try parsing from the first {
    depth = 0
    end = start
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    try:
        obj = json.loads(text[start:end])
    except (json.JSONDecodeError, TypeError):
        return []

    # Direct operations key
    if "operations" in obj and isinstance(obj["operations"], list):
        return [str(op) for op in obj["operations"]]

    # Nested under entry_function
    entry = obj.get("entry_function", {})
    if isinstance(entry, dict) and "operations" in entry:
        ops = entry["operations"]
        if isinstance(ops, list):
            return [str(op) for op in ops]

    return []


# ── QIR extraction helpers ─────────────────────────────────────────────────────

def _extract_qir(raw: str) -> str:
    """Extract valid LLVM IR from an LLM response that may be wrapped in JSON
    or markdown fences.

    Handles these common LLM output patterns:
      * {"answer": "...", ...}          — JSON object with a text field
      * ```llvm\\n...```               — markdown-fenced code block
      * Raw LLVM IR (no wrapper needed)
    """
    text = str(raw).strip()

    # ── 1. JSON wrapper ───────────────────────────────────────────────────────
    if text.startswith("{"):
        try:
            obj = json.loads(text)
            # Detect LLM outputting a tool-call as its answer (common failure mode
            # with smaller models that can't use CrewAI tool calling properly).
            if obj.get("type") == "function" or "name" in obj and "parameters" in obj:
                logger.warning("LLM emitted a tool-call JSON instead of QIR: %s", text[:120])
                return ""
            for key in ("answer", "qir", "qir_code", "result", "output", "code"):
                if key in obj and isinstance(obj[key], str):
                    text = obj[key].strip()
                    break
        except (json.JSONDecodeError, TypeError):
            pass

    # ── 2. Markdown fenced code block ─────────────────────────────────────────
    fence_match = re.search(
        r"```(?:llvm|llvmir|ir|c|cpp)?\s*\n(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if fence_match:
        text = fence_match.group(1).strip()

    # ── 3. Strip any remaining leading prose up to first LLVM IR token ────────
    # Valid LLVM IR lines begin with: ';', '%', '@', 'define', 'declare',
    # 'attributes', '!', 'source_filename', 'target', 'ModuleID'
    _LLVM_START = re.compile(
        r"^(;|%\w|@\w|define |declare |attributes |!|source_filename|target |ModuleID)",
        re.MULTILINE,
    )
    m = _LLVM_START.search(text)
    if m and m.start() > 0:
        text = text[m.start():]

    return text.strip()


def _is_complete_qir(text: str) -> bool:
    """Check if LLVM IR text has all required sections (not just gate calls)."""
    has_types = "%Qubit = type opaque" in text or "%Qubit" in text
    has_declare = "declare " in text
    has_attributes = "attributes #" in text
    return has_types and has_declare and has_attributes


def _extract_ops_from_llvm_ir(text: str) -> list[str]:
    """Extract gate call statements from incomplete LLVM IR for reassembly."""
    ops = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("call void @__quantum__qis__") and "__body" in stripped:
            ops.append(stripped)
    return ops


def _apply_output_guardrail(raw: str) -> str:
    """Post-process LLM output: assemble QIR from JSON ops if needed.

    This applies the same logic as qir_output_guardrail but is called
    directly (since Agent.execute_task does not invoke Task guardrails).

    Order of attempts:
      1. If output looks like complete LLVM IR → extract and return
      2. If output is incomplete LLVM IR (missing declarations/attributes) → reassemble
      3. If output is JSON with operations → assemble QIR via qir_assembler
      4. Fall back to _extract_qir for markdown/prose cleanup
    """
    text = raw.strip() if raw else ""
    if not text:
        return ""

    # ── 1. Check for LLVM IR (complete or incomplete) ──
    if text.lstrip().startswith("; ModuleID") or text.lstrip().startswith("define void"):
        cleaned = _extract_qir(text)
        if cleaned:
            if _is_complete_qir(cleaned):
                logger.info("Output guardrail: complete LLVM IR detected")
                return cleaned
            # ── 2. Incomplete LLVM IR — extract gate calls and reassemble ──
            ir_ops = _extract_ops_from_llvm_ir(cleaned)
            if ir_ops:
                logger.info("Output guardrail: incomplete LLVM IR with %d gate calls, reassembling", len(ir_ops))
                qir = assemble_qir_from_operations(ir_ops)
                if qir:
                    return qir
                logger.warning("Output guardrail: reassembly from LLVM IR calls failed")

    # ── 3. JSON with operations → assemble QIR ──
    ops = _extract_operations_from_json(text)
    if ops:
        logger.info("Output guardrail: found %d operations in JSON, assembling QIR", len(ops))
        qir = assemble_qir_from_operations(ops)
        if qir:
            return qir
        logger.warning("Output guardrail: assembly failed despite finding operations")

    # ── 4. Try _extract_qir for markdown/prose wrapped IR ──
    cleaned = _extract_qir(text)
    if cleaned and ("__quantum__" in cleaned or "define void" in cleaned):
        if _is_complete_qir(cleaned):
            logger.info("Output guardrail: extracted complete LLVM IR from wrapped output")
            return cleaned
        # Try reassembly from incomplete wrapped IR
        ir_ops = _extract_ops_from_llvm_ir(cleaned)
        if ir_ops:
            logger.info("Output guardrail: reassembling from %d extracted gate calls", len(ir_ops))
            qir = assemble_qir_from_operations(ir_ops)
            if qir:
                return qir

    # Nothing usable
    logger.warning("Output guardrail: could not extract valid QIR from output (first 200 chars): %s",
                    text[:200])
    return ""


class TranslationAgent:
    """AI agent specialized in MLIR to QIR translation."""

    def __init__(self, llm, tools: list, verbose: bool = True):
        self.agent = Agent(
            role="MLIR to QIR Translation Specialist",

            goal=(
                "Convert MLIR quantum circuits to valid QIR (LLVM IR) format. "
                "Output raw LLVM IR text only — no JSON, no markdown fences, no prose."
            ),

            backstory=(
                "You are an expert in quantum circuit representations with deep knowledge "
                "of MLIR dialects (Catalyst, Quake) and QIR specifications.\n\n"
                "OUTPUT FORMAT (choose one):\n"
                "Option A (PREFERRED): Raw LLVM IR starting with ; ModuleID = 'quantum_module'\n"
                "Option B: JSON with {\"operations\": [\"h 0\", \"cnot 0 1\"], \"num_qubits\": N}\n\n"
                "You have all the gate mappings and QIR patterns you need in the task "
                "description. Use them directly — do not try to call tools to look up "
                "information that is already provided to you."
            ),

            tools=tools,
            llm=llm,
            verbose=verbose,
            allow_delegation=False,
            max_iter=15,
        )

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def translate(self, mlir_code: str, dialect: Optional[str] = None) -> str:
        """Translate MLIR to QIR (first attempt, no prior feedback)."""
        return self.translate_with_feedback(mlir_code, dialect, iteration=1)

    def translate_with_feedback(
        self,
        mlir_code: str,
        dialect: Optional[str],
        feedback: Optional[str] = None,
        previous_qir: Optional[str] = None,
        iteration: int = 1,
    ) -> str:
        """Translate MLIR to QIR, optionally incorporating feedback from a prior attempt.

        Args:
            mlir_code:     MLIR source code.
            dialect:       Detected dialect name, or None / "unknown" for unrecognised.
            feedback:      Structured failure feedback from the previous iteration.
            previous_qir:  The QIR produced in the previous iteration.
            iteration:     Current iteration number (1-based).

        Returns:
            Generated QIR code string.
        """
        dialect_is_unknown = dialect is None or dialect.lower() in ("unknown", "unseen")
        dialect_info = f" ({dialect} dialect)" if dialect and not dialect_is_unknown else ""

        # ---- Build task description ----------------------------------------
        parts = []

        if dialect_is_unknown:
            parts.append(
                "UNSEEN DIALECT DETECTED.\n\n"
                "This MLIR dialect is not yet recognized by the system. Follow these steps:\n"
                "1. If you have a 'Search for quantum simulator' tool, use it with the "
                "dialect name to find a matching simulator for verification. If you discover "
                "one via web search, register it using the tool's register: format so it is "
                "remembered for future runs.\n"
                "2. If you have a 'Read website content' tool, use it to fetch "
                "documentation for the namespace prefixes you see in the code below.\n"
                "3. Use the gate mapping reference provided below to translate "
                "any gates you can identify.\n\n"
            )

        # ── Inline QIR reference (context engineering: inject, don't retrieve) ──
        qir_ref = get_qir_reference_context()

        parts.append(
            "OUTPUT FORMAT (choose one):\n"
            "Option A (PREFERRED): Raw LLVM IR starting with ; ModuleID = 'quantum_module'\n"
            "Option B: JSON object with {\"operations\": [\"h 0\", \"cnot 0 1\", ...], \"num_qubits\": N}\n"
            "  Short-form ops: gate qubit... (e.g. 'h 0', 'cnot 0 1', 'rx 1.5708 0')\n\n"
            f"--- QIR REFERENCE (use this, do NOT call any retrieval tool) ---\n\n"
            f"{qir_ref}\n"
            f"--- END REFERENCE ---\n\n"
            f"Translate the following MLIR quantum circuit{dialect_info} to QIR format:\n\n"
            f"```mlir\n{mlir_code}\n```\n\n"
            "Requirements:\n"
            "1. Use the gate mappings and template above — do NOT call a tool to look them up\n"
            "2. Map each MLIR gate to the corresponding __quantum__qis__*__body call\n"
            "3. Use correct qubit pointer syntax (null for qubit 0, inttoptr for others)\n"
            "4. Include measurements for ALL qubits and output recording at the end\n"
            "5. If you cannot produce complete LLVM IR, output JSON Option B instead\n\n"
            "Start your answer with ; ModuleID = 'quantum_module' (Option A) "
            "or { (Option B)."
        )

        if iteration > 1 and previous_qir and feedback:
            parts.append(
                f"\n\n--- PREVIOUS ATTEMPT (iteration {iteration - 1}) ---\n"
                f"The previous QIR had the following issues:\n\n{feedback}\n\n"
                f"Previous QIR code:\n```llvm\n{previous_qir}\n```\n\n"
                "Fix EVERY issue listed above. Do not repeat the same mistakes."
            )

        task_description = "".join(parts)

        logger.info(f"Translation agent starting (iteration {iteration})...")

        task = Task(
            description=task_description,
            expected_output="Complete QIR LLVM IR code",
            agent=self.agent,
        )
        result = self.agent.execute_task(task)
        result_str = str(result).strip()

        # Apply guardrail logic manually (execute_task does NOT invoke
        # Task guardrails — those only run in the full Crew pipeline).
        qir = _apply_output_guardrail(result_str)

        logger.debug(f"Extracted QIR (first 120 chars): {qir[:120]!r}")
        return qir
