"""Capture terminal output (logging + stdout) for a translation run to a markdown file."""

import contextlib
import io
import logging
import re
import sys
from datetime import datetime
from pathlib import Path

# Matches all ANSI escape sequences (colours, cursor, box-drawing resets, etc.)
_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[mABCDEFGHJKSTfinsulhp]')
# Box-drawing characters used by CrewAI's rich panels
_BOX_RE  = re.compile(r'[╭╮╰╯─│]')


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape codes and box-drawing characters."""
    text = _ANSI_RE.sub('', text)
    text = _BOX_RE.sub('', text)
    # Collapse lines that are now just whitespace
    lines = [l.rstrip() for l in text.splitlines()]
    # Remove runs of more than 2 consecutive blank lines
    cleaned, prev_blank = [], 0
    for line in lines:
        if line == '':
            prev_blank += 1
            if prev_blank <= 2:
                cleaned.append(line)
        else:
            prev_blank = 0
            cleaned.append(line)
    return '\n'.join(cleaned)


def _mlir_module_name(mlir_code: str) -> str:
    """Extract module name from MLIR, e.g. @run_ghz5 → run_ghz5."""
    m = re.search(r'module\s+@(\w+)', mlir_code)
    return m.group(1) if m else "translation"


@contextlib.contextmanager
def capture_translation_log(mlir_code: str, error_dir: Path):
    """Context manager — captures all Python logging + stdout during the block.

    Strips ANSI escape codes so the saved markdown is human-readable.
    Writes report to error_dir/<module_name>_<timestamp>.md.

    Yields:
        Path — the log file written on exit.
    """
    name = _mlir_module_name(mlir_code)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    error_dir.mkdir(parents=True, exist_ok=True)
    out_path = error_dir / f"{name}_{ts}.md"

    # ── Capture logging ───────────────────────────────────────────────────────
    log_records: list[str] = []

    class _ListHandler(logging.Handler):
        def emit(self, record):
            log_records.append(self.format(record))

    handler = _ListHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s  %(levelname)-8s  %(name)s: %(message)s")
    )
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)

    # ── Tee stdout (CrewAI verbose prints go here) ────────────────────────────
    old_stdout = sys.stdout
    stdout_buf = io.StringIO()

    class _Tee:
        def write(self, text):
            old_stdout.write(text)
            stdout_buf.write(text)

        def flush(self):
            old_stdout.flush()

        def __getattr__(self, attr):
            return getattr(old_stdout, attr)

    sys.stdout = _Tee()

    try:
        yield out_path
    finally:
        sys.stdout = old_stdout
        root_logger.removeHandler(handler)

        stdout_text = _strip_ansi(stdout_buf.getvalue())
        log_text    = "\n".join(log_records)   # logging already plain text

        # ── Write markdown report ─────────────────────────────────────────────
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# Translation Run Log — `{name}`\n\n")
            f.write(f"- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"- **Module**: `{name}`\n\n")
            f.write("---\n\n")

            f.write("## MLIR Input\n\n")
            f.write(f"```mlir\n{mlir_code}\n```\n\n")
            f.write("---\n\n")

            f.write("## Agent / Verbose Output\n\n")
            if stdout_text.strip():
                f.write(f"```\n{stdout_text}\n```\n\n")
            else:
                f.write("_(no stdout output — deterministic path, no agent invoked)_\n\n")
            f.write("---\n\n")

            f.write("## Python Logging\n\n")
            if log_text.strip():
                f.write(f"```\n{log_text}\n```\n\n")
            else:
                f.write("_(no log records captured)_\n\n")
