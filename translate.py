#!/usr/bin/env python3
"""Backward-compatible CLI shim — delegates to ``agentic_mlir_qir.cli:main``.

Kept so existing scripts and the experiment drivers in ``experiments/run_e*.sh``
continue to work without modification.

For library use, prefer:

    from agentic_mlir_qir import translate
    result = translate(open("circuit.mlir").read())

For installed-CLI use, prefer:

    agentic-mlir-qir circuit.mlir          # console_scripts entry point
    mlir2qir         circuit.mlir          # alias
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make `import agentic_mlir_qir` work even from a fresh checkout that has not
# been `pip install`-ed yet.
_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT))

from agentic_mlir_qir.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
