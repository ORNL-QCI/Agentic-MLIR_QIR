"""Streamlit app for MLIR to QIR translation."""

import streamlit as st
import sys
from pathlib import Path

# Add project root and src to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'src'))

import logging
import os
from datetime import datetime

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


def load_examples():
    """Load example MLIR circuits."""
    examples = {}
    examples_dir = Path("examples/mlir")

    if examples_dir.exists():
        for file_path in examples_dir.glob("*.mlir"):
            try:
                with open(file_path, 'r') as f:
                    name = file_path.stem.replace('code_', '').replace('_', ' ').title()
                    examples[name] = f.read()
            except Exception as e:
                logger.error(f"Error loading {file_path}: {e}")

    return examples


def render_sidebar():
    """Render sidebar with configuration."""
    st.sidebar.title("⚙️ Configuration")

    # Model selection
    st.sidebar.subheader("LLM Model")

    from src.config.llm_config import LLMConfig

    model_options = list(LLMConfig.MODELS.keys())
    model_labels = [
        f"{key} ({LLMConfig.MODELS[key].size}, {LLMConfig.MODELS[key].speed})"
        for key in model_options
    ]

    selected_idx = model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0

    selected_model = st.sidebar.selectbox(
        "Select Model",
        options=model_options,
        format_func=lambda x: model_labels[model_options.index(x)],
        index=selected_idx
    )

    st.session_state.selected_model = selected_model

    # Model info
    model_info = LLMConfig.MODELS[selected_model]
    st.sidebar.info(f"""
    **VRAM Required:** {model_info.vram}
    **Quality:** {model_info.quality}
    **Speed:** {model_info.speed}
    **Use Case:** {model_info.recommended_for}
    """)

    # Example loader
    st.sidebar.subheader("📚 Load Example")

    examples = load_examples()
    example_names = ["None"] + list(examples.keys())

    selected_example = st.sidebar.selectbox("Choose Example Circuit", example_names)

    if selected_example != "None" and selected_example in examples:
        if st.sidebar.button("Load Example"):
            st.session_state.mlir_input = examples[selected_example]
            st.rerun()

    # Settings
    st.sidebar.subheader("🔧 Settings")

    max_iterations = st.sidebar.slider("Max Iterations", 1, 5, 3)
    verbose = st.sidebar.checkbox("Verbose Output", value=True)

    return {
        'model': selected_model,
        'max_iterations': max_iterations,
        'verbose': verbose
    }


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
            key="mlir_text_area"
        )

        st.session_state.mlir_input = mlir_input

        col_a, col_b = st.columns([1, 1])

        with col_a:
            translate_btn = st.button("🚀 Translate to QIR", type="primary", use_container_width=True)

        with col_b:
            clear_btn = st.button("🗑️ Clear", use_container_width=True)

        if clear_btn:
            st.session_state.mlir_input = ""
            st.session_state.translation_result = None
            st.rerun()

    # Translation execution
    if translate_btn and mlir_input.strip():
        with st.spinner("Translating... This may take a minute."):
            try:
                # Import here to avoid early initialization
                from src.parsers.mlir_parser import MLIRParser
                from src.generators.qir_generator import QIRGenerator

                # Parse MLIR with auto-detect
                parser = MLIRParser()
                circuit = parser.parse(mlir_input)
                detected_dialect = parser.get_detected_dialect(mlir_input)

                # Generate QIR
                generator = QIRGenerator()
                qir_code = generator.generate(circuit, module_id="translated-circuit")

                # Store result
                st.session_state.translation_result = {
                    'qir_code': qir_code,
                    'dialect': detected_dialect,
                    'circuit_info': {
                        'num_qubits': circuit.num_qubits,
                        'num_gates': len(circuit.gates),
                        'gate_types': [g.name for g in circuit.gates]
                    },
                    'timestamp': datetime.now().isoformat()
                }

                st.success(f"✓ Translation complete! Detected dialect: {detected_dialect}")

            except Exception as e:
                st.error(f"Translation error: {str(e)}")
                logger.exception("Translation failed")
                import traceback
                st.code(traceback.format_exc())

    # Display result
    with col2:
        st.subheader("💾 Generated QIR Code")

        if st.session_state.translation_result:
            qir_code = st.session_state.translation_result['qir_code']

            st.code(qir_code, language='llvm', line_numbers=True)

            # Download button
            st.download_button(
                label="⬇️ Download QIR",
                data=qir_code,
                file_name=f"circuit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ll",
                mime="text/plain"
            )

        else:
            st.info("Translation output will appear here")


def render_verification_section():
    """Render verification results."""
    if st.session_state.translation_result:
        st.subheader("✅ Circuit Analysis")

        info = st.session_state.translation_result['circuit_info']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Qubits", info['num_qubits'])

        with col2:
            st.metric("Gates", info['num_gates'])

        with col3:
            unique_gates = len(set(info['gate_types']))
            st.metric("Unique Gates", unique_gates)

        # Gate sequence
        with st.expander("🔍 Gate Sequence"):
            for i, gate in enumerate(info['gate_types'], 1):
                st.text(f"{i}. {gate}")


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
        st.markdown("- Extensible framework")

    with col3:
        st.markdown("**🔗 Links:**")
        st.markdown("[QIR Specification](https://github.com/qir-alliance/qir-spec)")
        st.markdown("[PennyLane Catalyst](https://github.com/PennyLaneAI/catalyst)")


def main():
    """Main application entry point."""
    initialize_session_state()

    # Render sidebar
    config = render_sidebar()

    # Main content
    render_translation_section(config)

    # Verification
    render_verification_section()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
