#!/usr/bin/env bash
#
# One-shot environment setup for a fresh clone of the Agentic MLIR-to-QIR
# repository. Creates a virtual environment, installs the Python
# dependencies (including the OpenQASM frontend and QIR runtime), attempts to
# install CUDA-Q where supported, and bootstraps a .env file for the
# HuggingFace token used by the agentic path.
#
# Usage:
#   bash scripts/setup.sh
#
# After it finishes, edit .env and set HF_TOKEN=hf_... (only needed for the
# agentic / unseen-dialect path). The deterministic MLIR path needs no token.

set -euo pipefail

# Resolve repo root (this script lives in <root>/scripts/).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

VENV_DIR="${ROOT_DIR}/venv"

log()  { printf '\033[1;36m[setup]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[setup]\033[0m %s\n' "$*" >&2; }

# ---------------------------------------------------------------------------
# 1. Virtual environment
# ---------------------------------------------------------------------------
if [ ! -d "${VENV_DIR}" ]; then
    log "Creating virtual environment at ${VENV_DIR}"
    python3 -m venv "${VENV_DIR}"
else
    log "Reusing existing virtual environment at ${VENV_DIR}"
fi
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"
python -m pip install --upgrade pip >/dev/null

# ---------------------------------------------------------------------------
# 2. Core Python dependencies (deterministic path + QASM frontend + QIR runtime)
# ---------------------------------------------------------------------------
log "Installing Python dependencies from requirements.txt"
pip install -r requirements.txt

log "Installing the package itself (editable)"
pip install -e . >/dev/null

log "Installing QIR runtime (qir-runner)"
pip install "qirrunner==0.9.1"

# ---------------------------------------------------------------------------
# 3. CUDA-Q (needed for OpenQASM -> Quake MLIR and Quake verification)
#    Not on standard PyPI at 0.13 and Linux-only; install best-effort.
# ---------------------------------------------------------------------------
OS="$(uname -s)"
ARCH="$(uname -m)"
if python -c "import cudaq" 2>/dev/null; then
    log "CUDA-Q already installed — skipping."
elif [ "${OS}" = "Linux" ] && { [ "${ARCH}" = "x86_64" ] || [ "${ARCH}" = "aarch64" ]; }; then
    log "Attempting to install CUDA-Q (cudaq) for ${OS}/${ARCH}"
    if pip install "cudaq==0.13.0"; then
        log "CUDA-Q installed."
    else
        warn "Could not install CUDA-Q automatically."
        warn "OpenQASM->QIR and Quake verification will be unavailable until it is installed."
        warn "See: https://nvidia.github.io/cuda-quantum/latest/using/install/install.html"
    fi
else
    warn "CUDA-Q is Linux x86_64/aarch64 only; detected ${OS}/${ARCH}."
    warn "OpenQASM->QIR and Quake verification are unavailable on this platform."
    warn "The deterministic MLIR path and the agentic (HF token) path still work."
fi

# ---------------------------------------------------------------------------
# 4. .env bootstrap (HuggingFace token for the agentic path)
# ---------------------------------------------------------------------------
if [ ! -f "${ROOT_DIR}/.env" ]; then
    log "Creating .env from .env.example"
    cp "${ROOT_DIR}/.env.example" "${ROOT_DIR}/.env"
    warn "Edit .env and set HF_TOKEN=hf_... to enable the agentic (unseen-dialect) path."
else
    log ".env already exists — leaving it untouched."
fi

# ---------------------------------------------------------------------------
# 5. Smoke check
# ---------------------------------------------------------------------------
log "Verifying the deterministic path on a Bell state"
python translate.py example/catalyst_mlir/code_bell.mlir --no-verify --quiet >/dev/null \
    && log "Deterministic MLIR -> QIR: OK"

if python -c "import cudaq" 2>/dev/null; then
    log "Verifying the OpenQASM path on a Bell state"
    python translate.py example/qasm/bell_state_v2.qasm --no-verify --quiet >/dev/null \
        && log "OpenQASM -> QIR: OK"
fi

log "Done. Activate the environment with:  source venv/bin/activate"
