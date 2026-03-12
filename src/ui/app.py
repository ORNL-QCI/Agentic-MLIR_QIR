"""Streamlit app for MLIR to QIR translation."""

import streamlit as st
import sys
from pathlib import Path

# Add project root and src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

import json
import logging
import os

# Disable CrewAI telemetry BEFORE any crewai import.
# CrewAI telemetry registers OS signal handlers which fail in Streamlit's
# background thread ("signal only works in main thread").
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")
import threading
import time
import uuid
from datetime import datetime

import pandas as pd
import plotly.express as px

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="MLIR to QIR Translator",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    .stTextArea textarea {
        font-family: 'Courier New', monospace;
        font-size: 13px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'translation_result' not in st.session_state:
        st.session_state.translation_result = None
    if 'mlir_input' not in st.session_state:
        st.session_state.mlir_input = ""
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "llama3.1:8b"
    if 'session_id' not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex[:8]


_log_lock = threading.Lock()
_LOG_FILE = project_root / "logs" / "translations.jsonl"


def _log_translation(
    session_id: str,
    mlir_input: str,
    result: dict,
    model: str = "deterministic",
    run_info_file: str | None = None,
    force_agentic: bool = False,
) -> None:
    """Append one translation record to logs/translations.jsonl (thread-safe)."""
    record = {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "source": "ui",
        "model": model,
        "dialect": result.get("dialect", "unknown"),
        "translation_time_s": result.get("translation_time_s", 0),
        "translation_path": result.get("translation_path", "deterministic"),
        "force_agentic": force_agentic,
        "iterations": result.get("iterations", 1),
        "shots": result.get("shots", 1000),
        "success": result.get("success", False),
        "circuit_info": result.get("circuit_info", {}),
        "run_info_file": run_info_file,  # cross-link to detailed report
        "mlir_input": mlir_input,
        "qir_output": result.get("qir_code", ""),
    }
    _LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with _log_lock:
        with _LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")


def load_examples():
    """Load example MLIR circuits (Catalyst + Quake dialects)."""
    examples = {}

    for file_path in sorted(Path("examples/mlir").glob("*.mlir")):
        try:
            name = "[Catalyst] " + file_path.stem.replace("_", " ").title()
            examples[name] = file_path.read_text()
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")

    for file_path in sorted(Path("examples/quake_mlir").glob("*.mlir")):
        try:
            stem = file_path.stem.replace("code_", "").replace("_", " ").title()
            name = f"[Quake] {stem}"
            examples[name] = file_path.read_text()
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")

    return examples


def render_sidebar():
    """Render sidebar with configuration."""
    st.sidebar.title("⚙️ Configuration")

    st.sidebar.subheader("LLM Model")

    from src.config.llm_config import LLMConfig

    model_options = list(LLMConfig.MODELS.keys())

    def _model_label(key: str) -> str:
        info = LLMConfig.MODELS[key]
        provider_tag = "☁️ API" if info.provider != "ollama" else "💻 Local"
        free_tag = " (free)" if info.free_tier else ""
        return f"{provider_tag} {key} — {info.size}, {info.speed}{free_tag}"

    selected_idx = (
        model_options.index(st.session_state.selected_model)
        if st.session_state.selected_model in model_options
        else 0
    )

    selected_model = st.sidebar.selectbox(
        "Select Model",
        options=model_options,
        format_func=_model_label,
        index=selected_idx,
    )
    st.session_state.selected_model = selected_model

    model_info = LLMConfig.MODELS[selected_model]

    if model_info.provider == "ollama":
        st.sidebar.info(f"""
**Backend:** Ollama (local)
**VRAM Required:** {model_info.vram}
**Quality:** {model_info.quality}
**Speed:** {model_info.speed}
**Use Case:** {model_info.recommended_for}
        """)
    elif model_info.provider == "huggingface":
        import os
        hf_token_set = bool(os.environ.get(model_info.api_key_env))
        token_status = "✅ HF_TOKEN found" if hf_token_set else "⚠️ Set `HF_TOKEN` env var (free at huggingface.co/settings/tokens)"
        st.sidebar.info(f"""
**Backend:** HuggingFace Inference API (free tier)
**Model:** {model_info.ollama_name}
**Quality:** {model_info.quality}
**Speed:** {model_info.speed}
**Use Case:** {model_info.recommended_for}
**Token:** {token_status}
        """)
    else:
        import os
        api_key_set = bool(os.environ.get(model_info.api_key_env))
        key_status = "✅ API key found" if api_key_set else f"⚠️ Set `{model_info.api_key_env}` env var"
        free_note = "Free tier available" if model_info.free_tier else "Paid API"
        st.sidebar.info(f"""
**Backend:** {model_info.provider.upper()} API ({free_note})
**Quality:** {model_info.quality}
**Speed:** {model_info.speed}
**Use Case:** {model_info.recommended_for}
**API Key:** {key_status}
        """)

    st.sidebar.subheader("📚 Load Example")
    examples = load_examples()
    example_names = ["None"] + list(examples.keys())
    selected_example = st.sidebar.selectbox("Choose Example Circuit", example_names)
    if selected_example != "None" and selected_example in examples:
        if st.sidebar.button("Load Example"):
            st.session_state.mlir_input = examples[selected_example]
            st.rerun()

    st.sidebar.subheader("🔧 Settings")
    max_iterations = st.sidebar.selectbox(
        "Max Iterations",
        options=[1, 2, 3, 4, 5, 7, 10],
        index=4,  # default = 5
        help="Maximum number of LLM repair iterations. Higher values give the agent more attempts but take longer.",
    )
    verbose = st.sidebar.checkbox("Verbose Output", value=True)
    force_agentic = st.sidebar.checkbox(
        "Force LLM (skip deterministic)",
        value=False,
        help=(
            "Always use the LLM agent even for known dialects (Catalyst/Quake). "
            "Skips the deterministic parser. Useful for benchmarking LLM "
            "translation time and iteration count."
        ),
    )

    return {
        'model': selected_model,
        'max_iterations': max_iterations,
        'verbose': verbose,
        'force_agentic': force_agentic,
    }


# ------------------------------------------------------------------ #
#  Translation helpers                                                #
# ------------------------------------------------------------------ #

def _extract_circuit_info(mlir_code: str, qir_code: str) -> dict:
    """Best-effort circuit info from MLIR (or QIR fallback)."""
    try:
        from src.parsers.mlir_parser import MLIRParser
        from src.dialects.base_dialect import UnsupportedDialectError
        circuit = MLIRParser().parse(mlir_code)
        return {
            'num_qubits': circuit.num_qubits,
            'num_gates': len(circuit.gates),
            'gate_types': [g.name for g in circuit.gates],
        }
    except Exception:
        pass
    # Fallback: count qubits from QIR qubit pointer patterns
    import re
    qubits = set(re.findall(r'inttoptr\s*\(\s*i64\s+(\d+)', qir_code or ""))
    qubits.add("0")
    gates = re.findall(r'@__quantum__qis__(\w+)__body', qir_code or "")
    return {
        'num_qubits': len(qubits),
        'num_gates': len(gates),
        'gate_types': gates,
    }


def _run_deterministic_translation(
    mlir_input: str,
    detected_dialect: str,
    t0: float,
    run_info_file: str | None = None,
) -> None:
    """Fast deterministic-only path. Stores result in session_state."""
    from src.parsers.mlir_parser import MLIRParser
    from src.generators.qir_generator import QIRGenerator

    parser = MLIRParser()
    circuit = parser.parse(mlir_input)
    generator = QIRGenerator()
    qir_code = generator.generate(circuit, module_id="translated-circuit")
    elapsed = time.time() - t0

    st.session_state.translation_result = {
        'qir_code': qir_code,
        'dialect': detected_dialect,
        'circuit_info': {
            'num_qubits': circuit.num_qubits,
            'num_gates': len(circuit.gates),
            'gate_types': [g.name for g in circuit.gates],
        },
        'timestamp': datetime.now().isoformat(),
        'translation_time_s': elapsed,
        'iterations': 1,
        'translation_path': 'deterministic',
        'verification_result': None,
        'verification_ran': False,
    }
    _log_translation(
        st.session_state.session_id,
        mlir_input,
        st.session_state.translation_result,
        model="deterministic",
        run_info_file=run_info_file,
        force_agentic=False,
    )
    st.success(f"✓ Translation complete! Detected dialect: {detected_dialect}")


def _run_agentic_pipeline(
    mlir_input: str,
    detected_dialect,
    config: dict,
    t0: float,
    run_info_file: str | None = None,
) -> None:
    """Agentic pipeline: deterministic first pass + verification + agent repair/translation.

    Falls back to deterministic-only when Ollama is unavailable.
    Stores result in session_state.
    """
    from src.config.settings import settings
    from src.config.llm_config import LLMConfig
    from crewai.llm import LLM

    model_key = config['model']
    model_info = LLMConfig.get_model_info(model_key)

    try:
        if model_info and model_info.provider == "huggingface":
            # ── HuggingFace Inference API ─────────────────────────────────────
            import os
            hf_token = os.environ.get(model_info.api_key_env, "")
            if not hf_token:
                st.error(
                    "HF_TOKEN not set. Get a free token at "
                    "https://huggingface.co/settings/tokens then run: "
                    "`export HF_TOKEN=hf_...` and restart the app."
                )
                return
            llm = LLM(
                model=model_info.get_litellm_model(),   # "huggingface/openai/gpt-oss-20b"
                api_key=hf_token,
                temperature=settings.LLM_TEMPERATURE,
            )
        elif model_info and model_info.provider == "openai":
            # ── OpenAI API model ──────────────────────────────────────────────
            import os
            api_key = os.environ.get(model_info.api_key_env, "")
            if not api_key:
                st.error(
                    f"API key not set. Please export `{model_info.api_key_env}` "
                    "in your environment and restart the app."
                )
                return
            llm = LLM(
                model=model_info.get_litellm_model(),
                api_key=api_key,
                temperature=settings.LLM_TEMPERATURE,
            )
        else:
            # ── Ollama local model ────────────────────────────────────────────
            import ollama as _ollama
            _ollama.list()   # raises if server is down
            llm = LLM(
                model=LLMConfig.get_litellm_model(model_key),
                base_url=settings.LLM_BASE_URL,
                temperature=settings.LLM_TEMPERATURE,
            )
    except Exception as e:
        st.warning(f"LLM unavailable ({e}). Falling back to deterministic translation.")
        if detected_dialect is not None:
            _run_deterministic_translation(mlir_input, detected_dialect, t0)
        else:
            st.error(
                "Cannot translate: dialect is unrecognized and LLM is unavailable. "
                "Please ensure Ollama is running (`ollama serve`) or set the API key."
            )
        return

    from src.agents.crew_manager import CrewManager

    manager = CrewManager(
        llm=llm,
        max_iterations=config['max_iterations'],
        verbose=config['verbose'],
    )

    result = manager.translate_with_verification(
        mlir_input, shots=1000, force_agentic=config.get('force_agentic', False)
    )
    elapsed = time.time() - t0

    circuit_info = _extract_circuit_info(mlir_input, result.qir_code or "")

    st.session_state.translation_result = {
        'qir_code': result.qir_code or "",
        'dialect': result.dialect or detected_dialect or "unknown",
        'circuit_info': circuit_info,
        'timestamp': datetime.now().isoformat(),
        'translation_time_s': elapsed,
        'iterations': result.iterations,
        'translation_path': result.translation_path,
        'verification_result': result.verification_result,
        'verification_ran': result.verification_result is not None,
    }
    _log_translation(
        st.session_state.session_id,
        mlir_input,
        st.session_state.translation_result,
        model=config.get("model", "unknown"),
        run_info_file=run_info_file,
        force_agentic=config.get("force_agentic", False),
    )

    if result.success:
        st.success(
            f"✓ Translation verified! "
            f"Dialect: {result.dialect or 'unknown'} | "
            f"Path: {result.translation_path} | "
            f"Iterations: {result.iterations}"
        )
    else:
        st.warning(
            f"Translation complete but verification did not fully pass. "
            f"Path: {result.translation_path} | Iterations: {result.iterations}"
        )
        if result.error_message:
            st.info(result.error_message)

        # ── Human-in-the-loop: offer doc links when unknown dialect fails ──
        if result.translation_path == "ai_agent":
            with st.expander("Need help? Provide documentation links for this dialect", expanded=True):
                st.markdown(
                    "The agent could not translate this dialect. "
                    "Paste official documentation URLs below (one per line). "
                    "The agent will fetch them, store them in its knowledge base, and retry."
                )
                hitl_urls = st.text_area(
                    "Documentation URLs (one per line)",
                    key="hitl_urls",
                    placeholder="https://mlir.llvm.org/docs/Dialects/MyDialect/\nhttps://github.com/org/repo/blob/main/docs/dialect.md",
                    height=100,
                )
                if st.button("Fetch Documentation & Retry", key="hitl_retry_btn"):
                    urls = [u.strip() for u in hitl_urls.splitlines() if u.strip()]
                    if not urls:
                        st.error("Please enter at least one URL.")
                    else:
                        from src.tools.web_fetch_tool import fetch_url_content
                        from src.rag.knowledge_base import KnowledgeBase
                        from pathlib import Path as _Path
                        _kb_dir = _Path("knowledge_base/mlir_docs")
                        _kb_dir.mkdir(parents=True, exist_ok=True)
                        fetched_texts, fetched_metas = [], []
                        for url in urls:
                            with st.spinner(f"Fetching {url} …"):
                                content = fetch_url_content(url)
                            if content.startswith("Error"):
                                st.warning(f"Could not fetch {url}: {content}")
                                continue
                            # Persist to disk so it survives session restart
                            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                            safe = url.replace('/', '_').replace(':', '')[:60]
                            (_kb_dir / f"user_{ts}_{safe}.md").write_text(
                                f"# User-provided documentation\nSource: {url}\n\n{content}"
                            )
                            fetched_texts.append(content)
                            fetched_metas.append({'source': url, 'category': 'user_provided'})
                            st.success(f"Fetched: {url} ({len(content):,} chars)")

                        if fetched_texts:
                            with st.spinner("Indexing into knowledge base …"):
                                try:
                                    kb = KnowledgeBase()
                                    kb.add_texts(fetched_texts, fetched_metas)
                                    st.success(f"Added {len(fetched_texts)} document(s) to knowledge base.")
                                except Exception as kb_err:
                                    st.warning(f"Knowledge base indexing failed: {kb_err}")

                            st.info("Retrying translation with updated knowledge base …")
                            _run_agentic_pipeline(
                                mlir_input, result.dialect or detected_dialect, config, time.time()
                            )


# ------------------------------------------------------------------ #
#  Input validation                                                   #
# ------------------------------------------------------------------ #

def _is_valid_mlir(text: str) -> bool:
    """Heuristic: require at least 2 MLIR structural indicators."""
    indicators = [
        'module', 'func.func', 'quantum.', 'quake.', '!quantum',
        'qnode', 'catalyst.', 'llvm.emit_c_interface',
        '@__quantum', 'quantum.alloc', 'quantum.custom',
    ]
    matched = sum(1 for s in indicators if s in text)
    return len(text.strip()) >= 30 and matched >= 2


# ------------------------------------------------------------------ #
#  Render: translation section                                        #
# ------------------------------------------------------------------ #

def render_translation_section(config):
    """Render translation input and execution."""
    st.header("⚛️ MLIR to QIR Quantum Circuit Translator")
    st.markdown("LLM-powered multi-agent translation with verification")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Input MLIR Code")

        mlir_input = st.text_area(
            "Paste MLIR circuit here (Catalyst, Quake, or other dialect)",
            value=st.session_state.mlir_input,
            height=600,
            key="mlir_text_area",
        )
        st.session_state.mlir_input = mlir_input

        col_a, col_b = st.columns([1, 1])
        with col_a:
            translate_btn = st.button(
                "🚀 Translate to QIR", type="primary", use_container_width=True
            )
        with col_b:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)

        if clear_btn:
            st.session_state.mlir_input = ""
            st.session_state.translation_result = None
            st.rerun()

    # Translation execution
    if translate_btn and mlir_input.strip():
        if not _is_valid_mlir(mlir_input):
            st.error(
                "Input does not appear to be a valid MLIR quantum circuit. "
                "Please paste MLIR code in Catalyst or Quake dialect."
            )
            st.info("Example: paste the contents of `examples/mlir/bell_state.mlir`")
            st.stop()

        with st.spinner("Translating... This may take a minute."):
            from src.utils.run_logger import capture_translation_log
            _error_dir = project_root / "example_run_info"
            with capture_translation_log(mlir_input, _error_dir) as _log_path:
                try:
                    from src.parsers.mlir_parser import MLIRParser
                    from src.dialects.base_dialect import UnsupportedDialectError

                    t0 = time.time()

                    # Detect dialect
                    try:
                        detected_dialect = MLIRParser().get_detected_dialect(mlir_input)
                        dialect_is_known = True
                    except UnsupportedDialectError:
                        detected_dialect = None
                        dialect_is_known = False

                    # Routing: fast deterministic path vs full agentic pipeline
                    use_deterministic = (
                        dialect_is_known
                        and config['max_iterations'] == 1
                        and not config.get('force_agentic', False)
                    )
                    if use_deterministic:
                        _run_deterministic_translation(mlir_input, detected_dialect, t0,
                                                       run_info_file=_log_path.name)
                    else:
                        _run_agentic_pipeline(mlir_input, detected_dialect, config, t0,
                                              run_info_file=_log_path.name)

                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
                    logger.exception("Translation failed")
                    import traceback
                    st.code(traceback.format_exc())
            st.caption(f"Run log saved → `example_run_info/{_log_path.name}`")

    # Display result
    with col2:
        st.subheader("💾 Generated QIR Code")

        if st.session_state.translation_result:
            qir_code = st.session_state.translation_result['qir_code']

            st.code(qir_code, language='llvm', line_numbers=True)

            st.download_button(
                label="⬇️ Download QIR",
                data=qir_code,
                file_name=f"circuit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ll",
                mime="text/plain",
            )

            # Metrics row: Translation Time | Iterations | Translation Path
            t_col1, t_col2, t_col3 = st.columns(3)
            with t_col1:
                elapsed = st.session_state.translation_result.get('translation_time_s', 0)
                time_str = f"{elapsed * 1000:.1f}ms" if elapsed < 1.0 else f"{elapsed:.2f}s"
                st.metric("Translation Time", time_str)
            with t_col2:
                iters = st.session_state.translation_result.get('iterations', 1)
                st.metric("Iterations", iters)
            with t_col3:
                path = st.session_state.translation_result.get('translation_path', 'deterministic')
                path_label = {
                    'deterministic': 'Deterministic',
                    'ai_agent': 'AI Agent',
                    'deterministic+repair': 'Det. + AI Repair',
                }.get(path, path)
                st.metric("Translation Path", path_label)

        else:
            st.info("Translation output will appear here")


# ------------------------------------------------------------------ #
#  Render: verification section                                       #
# ------------------------------------------------------------------ #

def _render_verification_data(vr: dict) -> None:
    """Render the full verification result dict into Streamlit widgets."""
    if not vr.get('success'):
        st.error(f"Verification pipeline error: {vr.get('error', 'unknown error')}")
        return

    overall_pass = vr['similarity_passes'] and vr['gate_comparison'].get('matches', False)
    if overall_pass:
        st.success("PASS — Gate counts match and distributions are similar (TVD similarity >= 95%)")
    else:
        st.warning("PARTIAL — See details below for mismatches")

    qir_label = "simulated (mock)" if vr['qir_is_mock'] else "real execution"
    cat_label = "simulated (mock)" if vr['catalyst_is_mock'] else "real execution"
    mlir_runner_label = vr.get('mlir_runner_label', 'MLIR runner')
    st.caption(
        f"QIR backend: {qir_label}  |  MLIR backend ({mlir_runner_label}): {cat_label}"
    )

    sim_pct = vr['similarity'] * 100
    delta_label = "PASS" if vr['similarity_passes'] else "FAIL"
    st.metric(
        label="Distribution Similarity (TVD-based)",
        value=f"{sim_pct:.1f}%",
        delta=delta_label,
        delta_color="normal" if vr['similarity_passes'] else "inverse",
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**QIR Execution Results**")
        if vr['qir_distribution']:
            rows = sorted(vr['qir_distribution'].items())
            df_qir = pd.DataFrame({'Outcome': [r[0] for r in rows], 'Count': [r[1] for r in rows]})
            fig_qir = px.bar(
                df_qir, x='Outcome', y='Count',
                title=f"QIR Distribution ({qir_label})",
                color_discrete_sequence=['#1f77b4'],
                text='Count',
            )
            fig_qir.update_traces(textposition='outside')
            qir_max = max(vr['qir_distribution'].values(), default=1)
            fig_qir.update_layout(
                xaxis_title="Measurement Outcome",
                xaxis_type='category',
                yaxis_title="Count (shots=1000)",
                yaxis_range=[0, qir_max * 1.25],
                showlegend=False,
                height=380,
                margin=dict(t=50, b=40),
            )
            st.plotly_chart(fig_qir, use_container_width=True)
        else:
            st.info("No QIR distribution data")

    with chart_col2:
        st.markdown(f"**{mlir_runner_label} Execution Results**")
        if vr['catalyst_distribution']:
            rows = sorted(vr['catalyst_distribution'].items())
            df_cat = pd.DataFrame({'Outcome': [r[0] for r in rows], 'Count': [r[1] for r in rows]})
            fig_cat = px.bar(
                df_cat, x='Outcome', y='Count',
                title=f"{mlir_runner_label} ({cat_label})",
                color_discrete_sequence=['#ff7f0e'],
                text='Count',
            )
            fig_cat.update_traces(textposition='outside')
            cat_max = max(vr['catalyst_distribution'].values(), default=1)
            fig_cat.update_layout(
                xaxis_title="Measurement Outcome",
                xaxis_type='category',
                yaxis_title="Count (shots=1000)",
                yaxis_range=[0, cat_max * 1.25],
                showlegend=False,
                height=380,
                margin=dict(t=50, b=40),
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No MLIR distribution data")

    st.markdown("**Gate Count Comparison**")
    gate_comp = vr['gate_comparison']
    gate_match_label = "MATCH" if gate_comp.get('matches') else "MISMATCH"
    gc_col1, gc_col2, gc_col3 = st.columns(3)
    with gc_col1:
        st.metric("MLIR Total Gates", gate_comp.get('mlir_total', 0))
    with gc_col2:
        st.metric("QIR Total Gates", gate_comp.get('qir_total', 0))
    with gc_col3:
        st.metric("Gate Match", gate_match_label)

    all_gate_names = sorted(
        set(gate_comp.get('mlir_gates', {}).keys()) |
        set(gate_comp.get('qir_gates', {}).keys())
    )
    if all_gate_names:
        table_data = []
        for g in all_gate_names:
            mlir_cnt = gate_comp.get('mlir_gates', {}).get(g, 0)
            qir_cnt = gate_comp.get('qir_gates', {}).get(g, 0)
            table_data.append({
                'Gate': g,
                'MLIR Count': mlir_cnt,
                'QIR Count': qir_cnt,
                'Status': 'MATCH' if mlir_cnt == qir_cnt else 'MISMATCH',
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

    discrepancies = gate_comp.get('discrepancies', [])
    if discrepancies:
        st.markdown(f"**Gate Discrepancies ({len(discrepancies)})**")
        for d in discrepancies:
            st.warning(
                f"Gate '{d['gate']}': "
                f"MLIR={d['mlir_count']}, QIR={d['qir_count']}, "
                f"diff={d['difference']:+d}"
            )


def render_verification_section():
    """Render circuit analysis and verification results."""
    if not st.session_state.translation_result:
        return

    result = st.session_state.translation_result
    info = result['circuit_info']

    # ---- Circuit Analysis ----
    st.subheader("✅ Circuit Analysis")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Qubits", info['num_qubits'])
    with col2:
        st.metric("Gates", info['num_gates'])
    with col3:
        st.metric("Unique Gates", len(set(info['gate_types'])))

    with st.expander("🔍 Gate Sequence"):
        for i, gate in enumerate(info['gate_types'], 1):
            st.text(f"{i}. {gate}")

    # ---- Verification Results ----
    with st.expander("🔬 Verification Results", expanded=True):
        if result.get('verification_ran') and result.get('verification_result'):
            # Pre-computed during agentic pipeline — just display
            _render_verification_data(result['verification_result'])
        else:
            # On-demand for fast deterministic path (max_iterations=1, known dialect)
            mlir_code = st.session_state.mlir_input
            qir_code = result['qir_code']
            with st.spinner("Running simulation verification..."):
                from src.verification.pipeline import run_verification_pipeline
                vr = run_verification_pipeline(mlir_code, qir_code, shots=1000)
            _render_verification_data(vr)


def render_footer():
    """Render footer with information."""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**🎯 Features:**")
        st.markdown("- Multi-dialect support")
        st.markdown("- RAG-enhanced translation")
        st.markdown("- Real-time verification")
    with col2:
        st.markdown("**📚 Supported Dialects:**")
        st.markdown("- PennyLane Catalyst")
        st.markdown("- NVIDIA CUDA Quantum")
        st.markdown("- Unknown dialects (AI Agent)")
    with col3:
        st.markdown("**🔗 Links:**")
        st.markdown("[QIR Specification](https://github.com/qir-alliance/qir-spec)")
        st.markdown("[PennyLane Catalyst](https://github.com/PennyLaneAI/catalyst)")


def main():
    """Main application entry point."""
    initialize_session_state()
    config = render_sidebar()
    render_translation_section(config)
    render_verification_section()
    render_footer()


if __name__ == "__main__":
    main()
