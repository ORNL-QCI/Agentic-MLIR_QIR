"""Simulator discovery tool for CrewAI agents.

When the system encounters an unseen MLIR dialect, this tool helps the agent
search for an appropriate quantum simulator that can execute circuits from
that dialect, enabling MLIR-side verification.

Discovered simulators are persisted to a JSON cache file so that a dialect
only needs to be discovered once — subsequent runs treat it as known.
"""

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

_CACHE_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "discovered_simulators.json"

# Built-in dialect-to-simulator mappings.
_BUILTIN_SIMULATORS = {
    "catalyst": {
        "simulator": "PennyLane Catalyst",
        "package": "pennylane-catalyst",
        "install": "pip install pennylane pennylane-catalyst",
        "docs": "https://docs.pennylane.ai/projects/catalyst/",
    },
    "quake": {
        "simulator": "CUDA Quantum",
        "package": "cuda-quantum",
        "install": "pip install cuda-quantum",
        "docs": "https://nvidia.github.io/cuda-quantum/",
    },
    "openqasm": {
        "simulator": "Qiskit Aer",
        "package": "qiskit-aer",
        "install": "pip install qiskit qiskit-aer",
        "docs": "https://qiskit.github.io/qiskit-aer/",
    },
    "cirq": {
        "simulator": "Cirq Simulator",
        "package": "cirq-core",
        "install": "pip install cirq-core",
        "docs": "https://quantumai.google/cirq",
    },
    "quil": {
        "simulator": "PyQuil / QVM",
        "package": "pyquil",
        "install": "pip install pyquil",
        "docs": "https://pyquil-docs.rigetti.com/",
    },
    "stim": {
        "simulator": "Stim",
        "package": "stim",
        "install": "pip install stim",
        "docs": "https://github.com/quantumlib/Stim",
    },
}


def _load_discovered_cache() -> dict:
    """Load previously discovered simulator mappings from disk."""
    if _CACHE_FILE.exists():
        try:
            return json.loads(_CACHE_FILE.read_text())
        except (json.JSONDecodeError, OSError) as e:
            logger.warning("Could not load simulator cache: %s", e)
    return {}


def _save_discovered_cache(cache: dict) -> None:
    """Persist discovered simulator mappings to disk."""
    try:
        _CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(cache, indent=2))
        logger.info("Simulator cache saved to %s", _CACHE_FILE)
    except OSError as e:
        logger.warning("Could not save simulator cache: %s", e)


def get_all_known_simulators() -> dict:
    """Return merged dict of built-in + discovered simulators."""
    merged = dict(_BUILTIN_SIMULATORS)
    merged.update(_load_discovered_cache())
    return merged


def register_discovered_simulator(
    dialect: str,
    simulator: str,
    package: str,
    install: str,
    docs: str = "",
) -> None:
    """Persist a newly discovered dialect→simulator mapping for future runs."""
    cache = _load_discovered_cache()
    cache[dialect.lower()] = {
        "simulator": simulator,
        "package": package,
        "install": install,
        "docs": docs,
        "source": "discovered",
    }
    _save_discovered_cache(cache)
    logger.info("Registered discovered simulator for '%s': %s", dialect, simulator)


class SimulatorDiscoveryTool:
    """Search for quantum simulators that can execute a given MLIR dialect.

    First checks built-in mappings and the persistent discovery cache,
    then suggests web search for truly unseen dialects.
    """

    name: str = "Search for quantum simulator"
    description: str = (
        "Find a quantum simulator capable of executing circuits from a given "
        "MLIR dialect. Input: the dialect name (e.g. 'catalyst', 'quake', "
        "'openqasm'). Returns simulator name, package, install command, and "
        "documentation URL. If you discover a simulator via web search, call "
        "this tool again with the format: "
        "'register:<dialect>|<simulator_name>|<package>|<install_cmd>|<docs_url>' "
        "to save it for future use."
    )

    def _run(self, dialect: str) -> str:
        text = dialect.strip()

        # Handle registration requests: register:<dialect>|<sim>|<pkg>|<install>|<docs>
        if text.lower().startswith("register:"):
            return self._handle_register(text[len("register:"):])

        dialect_lower = text.lower()
        all_known = get_all_known_simulators()

        # Check known + cached mappings
        if dialect_lower in all_known:
            info = all_known[dialect_lower]
            source = info.get("source", "built-in")
            return (
                f"Simulator found for '{dialect}' dialect ({source}):\n"
                f"  Name: {info['simulator']}\n"
                f"  Package: {info['package']}\n"
                f"  Install: {info['install']}\n"
                f"  Docs: {info.get('docs', 'N/A')}\n"
                f"\nThis simulator can be used for MLIR-side verification."
            )

        # Check SimulatorRegistry for a live runner
        try:
            from src.verification.simulator_registry import SimulatorRegistry
            runner = SimulatorRegistry.find_runner_for_dialect(dialect_lower)
            if runner:
                return (
                    f"Backend '{runner.name}' is already registered and available "
                    f"for the '{dialect}' dialect. No additional installation needed."
                )
        except Exception:
            pass

        # Not found — guide the agent to search and register
        return (
            f"No known simulator found for '{dialect}' dialect.\n\n"
            f"Next steps:\n"
            f"  1. Use your web search tool to find '{dialect} MLIR dialect simulator'\n"
            f"  2. Check https://mlir.llvm.org/docs/Dialects/ for dialect docs\n"
            f"  3. Search PyPI for '{dialect}-quantum' or '{dialect}-simulator'\n\n"
            f"Once you find a simulator, register it by calling this tool with:\n"
            f"  register:{dialect}|<simulator_name>|<pip_package>|<install_cmd>|<docs_url>\n\n"
            f"Until a simulator is registered, verification is limited to "
            f"QIR-side execution and gate counting (no MLIR-side TVD comparison)."
        )

    def _handle_register(self, payload: str) -> str:
        parts = [p.strip() for p in payload.split("|")]
        if len(parts) < 4:
            return (
                "Registration format: register:<dialect>|<simulator_name>|<package>|<install_cmd>|<docs_url>\n"
                "Example: register:openpulse|Qiskit Pulse|qiskit|pip install qiskit|https://qiskit.org"
            )
        dialect = parts[0]
        simulator = parts[1]
        package = parts[2]
        install = parts[3]
        docs = parts[4] if len(parts) > 4 else ""

        register_discovered_simulator(dialect, simulator, package, install, docs)
        return (
            f"Successfully registered simulator for '{dialect}' dialect:\n"
            f"  Name: {simulator}\n"
            f"  Package: {package}\n"
            f"  Install: {install}\n"
            f"  Docs: {docs}\n"
            f"\nThis mapping is now cached — '{dialect}' will be recognized in future runs."
        )


def get_simulator_discovery_tool() -> Optional[object]:
    """Return a CrewAI-compatible SimulatorDiscoveryTool, or None on failure."""
    try:
        from crewai.tools import BaseTool

        class _SimDiscovery(BaseTool):
            name: str = SimulatorDiscoveryTool.name
            description: str = SimulatorDiscoveryTool.description

            def _run(self, dialect: str) -> str:
                return SimulatorDiscoveryTool()._run(dialect)

        return _SimDiscovery()
    except Exception as e:
        logger.warning("Could not create SimulatorDiscoveryTool: %s", e)
        return None
