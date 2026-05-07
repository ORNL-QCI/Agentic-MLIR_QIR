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

    Handles many formats the LLM might produce:
      {"operations": ["h 0", "cnot 0 1"]}
      {"entry_function": {"operations": ["call void @...", ...]}}
      {"ModuleID": ..., "llvm_ir": ["call void @__quantum__qis__...", ...]}
      {"Module": {"functions": [{"body": [{"op": "...", "operands": [...]}]}]}}
      {"gate_calls": ["__quantum__qis__h__body(null)", ...]}

    Falls back to a recursive scan for any list whose elements look like
    QIR gate calls or ops in any of the known forms.
    """
    text = raw.strip()

    start = text.find("{")
    if start < 0:
        return []

    # Find the first {...} balanced JSON object
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

    json_text = text[start:end]
    try:
        obj = json.loads(json_text)
    except (json.JSONDecodeError, TypeError):
        # Common LLM failure mode: unescaped newlines/tabs inside quoted strings.
        # Sanitize by replacing raw control chars inside strings with spaces.
        try:
            obj = json.loads(_sanitise_json(json_text))
        except (json.JSONDecodeError, TypeError):
            return []

    # Well-known keys first
    for key_path in [
        ["operations"],
        ["entry_function", "operations"],
        ["llvm_ir"],             # list of LLVM IR strings
        ["gate_calls"],          # list of gate call strings
    ]:
        cur: object = obj
        for key in key_path:
            if isinstance(cur, dict) and key in cur:
                cur = cur[key]
            else:
                cur = None
                break
        if isinstance(cur, list) and cur:
            ops = _normalise_ops_list(cur)
            if ops:
                return ops

    # Recursive fallback: scan every list in the JSON tree and pick
    # the one with the highest count of actual QIR gate ops (not __rt__ runtime calls)
    best_ops: list[str] = []
    _GATE_PREFIXES = ('h ', 'x ', 'y ', 'z ', 's ', 't ', 'cnot ', 'cz ', 'swap ',
                      'rx ', 'ry ', 'rz ', 'mz ', 'measure ')

    def _score(ops: list[str]) -> int:
        score = 0
        for op in ops:
            if not isinstance(op, str):
                continue
            lower = op.lower().strip()
            # __rt__ runtime calls are NOT gates — skip
            if '__quantum__rt__' in lower:
                continue
            # Strong signal: starts with a known gate keyword
            if any(lower.startswith(p) for p in _GATE_PREFIXES):
                score += 2
            elif '__quantum__qis__' in lower:
                score += 2
            elif ' ' in lower:
                score += 1
        return score

    for candidate in _iter_lists(obj):
        ops = _normalise_ops_list(candidate)
        if _score(ops) > _score(best_ops):
            best_ops = ops
    return best_ops


def _iter_lists(obj):
    """Yield every list found in a nested JSON structure."""
    if isinstance(obj, list):
        yield obj
        for item in obj:
            yield from _iter_lists(item)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _iter_lists(v)


def _sanitise_json(text: str) -> str:
    """Fix common LLM JSON issues: unescaped newlines/tabs inside string values.

    Walks the text tracking whether we're inside a quoted string; any raw
    control character encountered inside a string is replaced with a space.
    Structural whitespace (outside strings) is preserved.
    """
    out = []
    in_string = False
    escaped = False
    for ch in text:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == '\\':
            out.append(ch)
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            out.append(ch)
            continue
        if in_string and ch in '\n\r\t\x00':
            out.append(' ')
            continue
        out.append(ch)
    return ''.join(out)


def _normalise_ops_list(ops: list) -> list[str]:
    """Convert a list of ops (strings, dicts, or mixed) into short-form strings.

    Handles three common LLM output formats:
      1. Short form:  "h 0", "cnot 0 1", "rx 1.5708 0"
      2. Dict form:   {"name": "__quantum__qis__h__body", "args": ["%q0"]}
      3. Dict form:   {"gate": "h", "qubits": [0]} or similar variants

    SSA variable names like "%q0", "%h0", "%cz01_0" are converted to qubit
    indices by tracking first-appearance order: %q0 -> 0, %q1 -> 1, etc.
    """
    # Track SSA var -> qubit index in order of first appearance.
    # Use a separate counter for genuinely-new qubits so aliases don't inflate it.
    ssa_to_qubit: dict[str, int] = {}
    qubit_counter = [0]  # wrapped in list for closure mutability

    def ssa_to_idx(val: str) -> str:
        """Convert an SSA variable name or bare integer to a qubit index string.

        Returns existing index if already registered. Otherwise assigns the
        next available qubit index (qubit_counter) and increments it.
        """
        val = str(val).strip()
        if val.startswith("%"):
            val = val[1:]
        # If already an integer, use as-is
        try:
            return str(int(val))
        except ValueError:
            pass
        if val not in ssa_to_qubit:
            ssa_to_qubit[val] = qubit_counter[0]
            qubit_counter[0] += 1
        return str(ssa_to_qubit[val])

    def ssa_alias(alias_name: str, qubit_idx: int) -> None:
        """Register an SSA variable as an alias for an existing qubit index.
        Does NOT increment the qubit counter."""
        name = str(alias_name).strip()
        if name.startswith("%"):
            name = name[1:]
        if name not in ssa_to_qubit:
            ssa_to_qubit[name] = qubit_idx

    # Recognized QIR gate keywords, longest-match first.
    _GATE_KEYWORDS = [
        'cnot', 'cx', 'swap', 'measure',
        'cz', 'rx', 'ry', 'rz', 'mz',
        'h', 'x', 'y', 'z', 's', 't',
    ]
    _KW_ALIASES = {
        'cx': 'cnot', 'measure': 'mz',
    }

    def gate_suffix(name: str) -> str:
        """Extract the canonical QIR gate keyword from an MLIR or QIR name.

        Handles many shapes the LLM might produce:
          __quantum__qis__h__body                      -> h
          ftqc.logical_h                               -> h
          logical_cnot                                 -> cnot
          ftqc.logical_cz                              -> cz
          cirq.h_gate                                  -> h
          init_zero                                    -> init_zero
          "%q0 = ftqc.init_zero : ..."                 -> init_zero (from full MLIR line)
          "%h0 = ftqc.logical_h %q0 : ..."             -> h
        """
        raw = str(name).strip().lower()
        # QIR form anywhere in the string
        m = re.search(r'__quantum__qis__(\w+?)__body', raw)
        if m:
            return _KW_ALIASES.get(m.group(1), m.group(1))
        # Extract <dialect>.<op_name> pattern from anywhere in the string
        # (handles full MLIR lines like "%q0 = ftqc.init_zero : ...")
        m = re.search(r'\b[a-z][a-z0-9_]*\.([a-z0-9_]+)', raw)
        if m:
            raw = m.group(1)
        # Strip dialect prefix if it's still there (handles "logical_h" with no prefix)
        elif '.' in raw:
            raw = raw.rsplit('.', 1)[-1]
        # Split on underscores and scan tokens for a recognised keyword
        tokens = raw.split('_')
        # Longest match across tokens
        for kw in _GATE_KEYWORDS:
            if kw in tokens:
                return _KW_ALIASES.get(kw, kw)
        # Check if this is clearly an init op
        if "init" in raw:
            return "init_zero"
        # Fallback: return stripped name
        return raw.strip('_')

    def parse_call_like_string(s: str) -> Optional[str]:
        """Parse strings like '__quantum__qis__h__body(null)' or
        'call void @__quantum__qis__cnot__body(ptr null, ptr inttoptr (i64 1 to ptr))'
        into short form 'h 0' / 'cnot 0 1'. Returns None if not a call string.
        """
        # Find the gate name. Use non-greedy match to handle malformed LLM
        # output like "@__quantum__qis__logical_h__body" → gate_suffix("logical_h") -> "h"
        gate_m = re.search(r'__quantum__qis__(\w+?)__body\s*\(', s)
        if not gate_m:
            return None
        raw_gate = gate_m.group(1)
        # Canonicalize via gate_suffix to handle malformed names with prefixes
        # (e.g. "logical_h" -> "h", "ftqc.logical_cz" -> "cz")
        gate = gate_suffix(raw_gate)
        # Extract everything inside the outermost (...) after __body
        start_idx = gate_m.end()
        depth = 1
        end_idx = start_idx
        while end_idx < len(s) and depth > 0:
            if s[end_idx] == '(':
                depth += 1
            elif s[end_idx] == ')':
                depth -= 1
            if depth == 0:
                break
            end_idx += 1
        args_str = s[start_idx:end_idx]

        # Split top-level args on commas (ignore commas inside nested parens)
        tokens: list[str] = []
        current = []
        paren_depth = 0
        for ch in args_str:
            if ch == '(':
                paren_depth += 1
                current.append(ch)
            elif ch == ')':
                paren_depth -= 1
                current.append(ch)
            elif ch == ',' and paren_depth == 0:
                tokens.append("".join(current).strip())
                current = []
            else:
                current.append(ch)
        if current:
            tokens.append("".join(current).strip())

        qubits: list[int] = []
        for tok in tokens:
            if not tok:
                continue
            int_m = (re.search(r'i64\s+(\d+)', tok)
                     or re.search(r'inttoptr\s*\(\s*(\d+)', tok)
                     or re.search(r'\((\d+)\)', tok))
            if int_m:
                qubits.append(int(int_m.group(1)))
            elif 'null' in tok.lower():
                qubits.append(0)
        # For mz gate, only keep the qubit arg (first), not the result arg
        if gate == 'mz' and len(qubits) >= 2:
            qubits = qubits[:1]
        parts = [gate] + [str(q) for q in qubits]
        return " ".join(parts)

    normalised: list[str] = []
    for op in ops:
        if isinstance(op, str):
            # Try to parse as a call-like string first
            call_parsed = parse_call_like_string(op)
            if call_parsed is not None:
                normalised.append(call_parsed)
                continue
            normalised.append(op)
            continue
        if isinstance(op, dict):
            # Normalise keys to lowercase for resilience to Title-Case variations
            op_lc = {str(k).lower(): v for k, v in op.items()}
            # Try common key names for gate (also handle "Op", "Name" etc.)
            gate_name = (
                op_lc.get("name") or op_lc.get("gate") or op_lc.get("op")
                or op_lc.get("function") or op_lc.get("operation")
            )
            # Fallback: if `op` is a long string (whole MLIR line) and there's
            # a separate `type` field with a short name, prefer `type`.
            if gate_name and isinstance(gate_name, str) and len(gate_name) > 40:
                type_field = op_lc.get("type")
                if type_field and isinstance(type_field, str) and len(type_field) < 40:
                    gate_name = type_field
            if not gate_name:
                continue
            gate = gate_suffix(gate_name)
            # Skip initialisation, control flow, and non-gate ops
            non_gate = {"init_zero", "alloc", "init", "prepare", "extract",
                        "init_zero__body", "__init_zero",
                        "return", "func", "yield", "br", "cond_br",
                        "constant", "discriminate"}
            if gate in non_gate or "init" in gate:
                result = op_lc.get("result") or op_lc.get("results")
                # If no explicit result field, try to extract SSA name from
                # the op string itself: "%q0 = ftqc.init_zero : ..."
                if result is None:
                    op_str = op_lc.get("op") or op_lc.get("operation") or ""
                    m = re.match(r'\s*(%[\w.]+)\s*=', str(op_str))
                    if m:
                        result = m.group(1)
                if isinstance(result, str):
                    ssa_to_idx(result)  # registers as a new qubit
                elif isinstance(result, list):
                    for r in result:
                        if isinstance(r, str):
                            ssa_to_idx(r)
                continue
            # Prefer integer `qubits` list over `args`/`operands` SSA names
            # when both are provided.
            qubits_field = op_lc.get("qubits")
            if isinstance(qubits_field, list) and qubits_field and all(
                isinstance(q, (int, float)) or (isinstance(q, str) and q.strip().lstrip('-').isdigit())
                for q in qubits_field
            ):
                args = qubits_field
            else:
                args = (op_lc.get("args") or op_lc.get("operands")
                        or op_lc.get("arguments") or [])
            if not isinstance(args, list):
                continue
            # If no args provided explicitly, try to extract operand SSA
            # variables from the full MLIR line in the `op` field.
            # Pattern: "%result = dialect.op_name %operand1, %operand2 : ..."
            if not args:
                op_str = op_lc.get("op") or op_lc.get("operation") or ""
                if isinstance(op_str, str) and "=" in op_str:
                    # Get RHS after "="
                    rhs = op_str.split("=", 1)[1]
                    # Strip type annotation (after ":")
                    if ":" in rhs:
                        rhs = rhs.split(":", 1)[0]
                    # Extract all %var tokens AFTER the op name
                    # e.g. "ftqc.logical_h %q0" -> ["%q0"]
                    ssa_vars = re.findall(r'%[\w.]+', rhs)
                    if ssa_vars:
                        args = ssa_vars
                elif isinstance(op_str, str):
                    # No "=" — the RHS is the whole line (e.g. measurement)
                    if ":" in op_str:
                        part = op_str.split(":", 1)[0]
                    else:
                        part = op_str
                    ssa_vars = re.findall(r'%[\w.]+', part)
                    if ssa_vars:
                        args = ssa_vars
            # Gate-arity awareness: for LLM outputs that stuff both result
            # and operand SSA names into `args` (e.g. args=["%h0", "%q0"]
            # for single-qubit H), detect this and split into result/operand.
            expected_qubits = {
                'h': 1, 'x': 1, 'y': 1, 'z': 1, 's': 1, 't': 1,
                'rx': 1, 'ry': 1, 'rz': 1,
                'cnot': 2, 'cz': 2, 'swap': 2,
            }
            n_q = expected_qubits.get(gate)
            # Only apply split if no explicit result field given
            has_explicit_result = bool(op_lc.get("result") or op_lc.get("results"))
            implicit_results: list = []
            if (n_q and not has_explicit_result and isinstance(args, list)
                    and len(args) > n_q):
                # Assume first (len-n_q) args are result SSAs, rest are operands
                n_results = len(args) - n_q
                implicit_results = args[:n_results]
                args = args[n_results:]
            # Separate numeric parameters from qubit args
            param_parts: list[str] = []
            qubit_parts: list[str] = []
            for a in args:
                # Parameter = float or numeric string that's not an SSA var
                if isinstance(a, (int, float)) and not isinstance(a, bool):
                    # Ambiguous — could be qubit index. Check gate type.
                    if gate in ("rx", "ry", "rz", "r1") and not param_parts:
                        param_parts.append(str(a))
                    else:
                        qubit_parts.append(str(a))
                elif isinstance(a, str):
                    s = a.strip()
                    # Numeric float param
                    try:
                        float(s)
                        if "." in s and gate in ("rx", "ry", "rz", "r1") and not param_parts:
                            param_parts.append(s)
                            continue
                    except ValueError:
                        pass
                    qubit_parts.append(ssa_to_idx(s))
            # Register result SSA vars as aliases for the same qubits as their
            # corresponding operands (output[i] aliases input[i]).
            result = op_lc.get("result") or op_lc.get("results")
            # If args contained implicit results (gate-arity split above), use them
            if not result and implicit_results:
                result = implicit_results if len(implicit_results) > 1 else implicit_results[0]
            # If no explicit result field, parse the LHS of the op string:
            # "%cn_ctrl, %cn_tgt = ftqc.logical_cnot ..." -> ["%cn_ctrl", "%cn_tgt"]
            if result is None:
                op_str = op_lc.get("op") or op_lc.get("operation") or ""
                if isinstance(op_str, str) and "=" in op_str:
                    lhs = op_str.split("=", 1)[0]
                    lhs_vars = re.findall(r'%[\w.]+', lhs)
                    if lhs_vars:
                        result = lhs_vars if len(lhs_vars) > 1 else lhs_vars[0]
            if qubit_parts:
                # Map operand-side qubits (indices) back for aliasing
                op_qubits = [int(q) for q in qubit_parts]
                if isinstance(result, str):
                    # Single result aliases the first operand's qubit
                    ssa_alias(result, op_qubits[0])
                elif isinstance(result, list):
                    for i, r in enumerate(result):
                        if isinstance(r, str) and i < len(op_qubits):
                            ssa_alias(r, op_qubits[i])
            # Skip emitting a gate call for measurement/logical_measure ops here
            # (the assembler adds measurements automatically for all qubits)
            if gate in ("mz", "measure"):
                continue
            parts = [gate] + param_parts + qubit_parts
            normalised.append(" ".join(parts))
    return normalised


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
        is_known_dialect: bool = True,
    ) -> str:
        """Translate MLIR to QIR, optionally incorporating feedback from a prior attempt.

        Args:
            mlir_code:     MLIR source code.
            dialect:       Detected dialect name, or None / "unknown" for unrecognised.
            feedback:      Structured failure feedback from the previous iteration.
            previous_qir:  The QIR produced in the previous iteration.
            iteration:     Current iteration number (1-based).
            is_known_dialect: Whether the dialect was recognised by the deterministic parser.

        Returns:
            Generated QIR code string.
        """
        dialect_is_unknown = (
            not is_known_dialect
            or dialect is None
            or dialect.lower() in ("unknown", "unseen")
        )
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
            "  Short-form ops: gate qubit_index... (e.g. 'h 0', 'cnot 0 1', 'rx 1.5708 0')\n"
            "  CRITICAL for Option B: use INTEGER qubit indices (0, 1, 2, ...), NOT SSA variable names\n"
            "  like '%q0' or '%h0'. Map each MLIR SSA variable to a qubit index by first appearance\n"
            "  of the underlying qubit (e.g. %q0->0, %q1->1, %q2->2). If a gate outputs new SSA\n"
            "  names (e.g. %h0 from H on %q0), they refer to the same qubit — use the same index.\n"
            "  Do NOT use the dict form like {\"name\": \"...\", \"args\": [...]}; use string form only.\n\n"
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
