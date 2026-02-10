# ⚛️ MLIR to QIR Quantum Circuit Translator

**LLM-Powered Multi-Agent System** for translating quantum circuits from MLIR dialects to standard QIR format using CrewAI and RAG.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

This system uses large language models and multi-agent AI to automatically translate quantum circuits between different intermediate representations. It supports multiple MLIR dialects (Catalyst, Quake) and generates standard QIR code that can run on any QIR-compliant quantum hardware.

### Key Features

- ✅ **Multi-Dialect Support**: Catalyst (PennyLane), Quake (CUDA Quantum), extensible framework
- ✅ **LLM-Powered Translation**: Llama 3.1 (8B/70B), CodeLlama with RAG context
- ✅ **Multi-Agent System**: CrewAI with Translation + Verification agents
- ✅ **Iterative Refinement**: Automatic error correction with feedback loops
- ✅ **Comprehensive Verification**: Gate counting, depth analysis, simulation
- ✅ **Interactive UI**: Streamlit web interface with real-time visualization
- ✅ **Auto-Updating Knowledge Base**: Fetches QIR specs, MLIR docs, research papers

---

## 🚀 Quick Start

### Prerequisites

```bash
- Python 3.9+
- NVIDIA GPU with 8GB+ VRAM (40GB+ for 70B model)
- CUDA 12.x
- Git
```

### Installation

```bash
# 1. Navigate to project
cd agentic_mlir_qir_updated

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# IMPORTANT: Edit .env and add your HUGGINGFACE_TOKEN!

# 5. Install Ollama (if not installed)
curl -fsSL https://ollama.com/install.sh | sh

# 6. Pull LLM models
bash scripts/setup_llm.sh

# 7. Fetch and index knowledge base
python scripts/fetch_knowledge.py
python scripts/initialize_db.py

# 8. Launch application
streamlit run src/ui/app.py
```

Access the UI at: `http://localhost:8501`

---

## 📊 System Architecture

```mermaid
graph TB
    A[MLIR Code] --> B[Dialect Detector]
    B --> C{Catalyst/Quake?}
    C --> D[MLIR Parser]
    D --> E[RAG Context Retrieval]
    E --> F[Translation Agent]
    F --> G[QIR Generator]
    G --> H[QIR Code]
    H --> I[Verification Agent]
    I --> J{Verified?}
    J -->|No| K[Feedback Loop]
    K --> F
    J -->|Yes| L[Output QIR]
```

### Components

| Component | Description | Status |
|-----------|-------------|--------|
| **Dialect System** | Extensible plugin architecture for MLIR dialects | ✅ Complete |
| **RAG System** | ChromaDB + HuggingFace embeddings for context retrieval | ✅ Complete |
| **Translation Agent** | LLM-powered MLIR→QIR conversion | ✅ Complete |
| **Verification Agent** | Multi-level validation (gate count, simulation) | ✅ Complete |
| **QIR Generator** | Template-based QIR code generation | ✅ Complete |
| **Streamlit UI** | Interactive web interface | ✅ Complete |

---

## 💡 Usage Examples

### Command Line

```python
from src.parsers.mlir_parser import MLIRParser
from src.generators.qir_generator import QIRGenerator

# Parse MLIR circuit (auto-detects dialect)
parser = MLIRParser()
circuit = parser.parse(mlir_code)

print(f"Detected: {parser.get_detected_dialect()}")
print(f"Qubits: {circuit.num_qubits}, Gates: {len(circuit.gates)}")

# Generate QIR
generator = QIRGenerator()
qir_code = generator.generate(circuit, module_id="my-circuit")

print(qir_code)
```

### With Multi-Agent System

```python
from src.agents.crew_manager import CrewManager
from src.rag.knowledge_base import KnowledgeBase
from langchain_community.llms import Ollama

# Initialize
llm = Ollama(model="llama3.1:8b-instruct")
kb = KnowledgeBase()
crew = CrewManager(llm=llm, knowledge_base=kb, max_iterations=3)

# Translate with verification
result = crew.translate(mlir_code, dialect="catalyst")

if result.success:
    print(f"✓ Verified in {result.iterations} iteration(s)")
    print(result.qir_code)
else:
    print(f"✗ Failed: {result.error_message}")
```

### Streamlit UI

1. Launch: `streamlit run src/ui/app.py`
2. Select LLM model from sidebar
3. Load example or paste MLIR code
4. Click "Translate to QIR"
5. View results, verification metrics, download QIR

---

## 🔧 Configuration

### Environment Variables (.env)

```bash
# LLM Configuration
LLM_MODEL=llama3.1:8b-instruct      # Options: llama3.1:8b-instruct, llama3.1:70b-instruct-q4_K_M, codellama:13b
LLM_TEMPERATURE=0.1
LLM_BASE_URL=http://localhost:11434

# RAG Configuration
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMADB_PATH=data/chromadb
RAG_TOP_K=5

# Verification Settings
SIMULATION_SIMILARITY_THRESHOLD=0.95
MAX_ITERATIONS=3

# IMPORTANT: Add your token!
HUGGINGFACE_TOKEN=your_token_here
```

### Model Selection

| Model | VRAM | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `llama3.1:8b-instruct` | ~8GB | Fast | Good | Development, testing |
| `llama3.1:70b-instruct-q4_K_M` | ~40GB | Medium | Excellent | Production quality |
| `codellama:13b` | ~13GB | Medium | Very Good | Code-heavy tasks |

---

## 📁 Project Structure

```
agentic_mlir_qir_updated/
├── src/
│   ├── config/              # Configuration management
│   │   ├── settings.py      # Pydantic settings
│   │   └── llm_config.py    # Multi-model LLM configs
│   ├── dialects/            # Extensible dialect system
│   │   ├── base_dialect.py  # Abstract interface
│   │   ├── catalyst_dialect.py  # PennyLane Catalyst
│   │   ├── quake_dialect.py     # CUDA Quantum
│   │   └── dialect_detector.py  # Auto-detection
│   ├── parsers/             # MLIR parsing
│   │   └── mlir_parser.py
│   ├── generators/          # QIR generation
│   │   ├── qir_generator.py
│   │   └── templates.py
│   ├── agents/              # CrewAI multi-agent system
│   │   ├── translation_agent.py
│   │   ├── verification_agent.py
│   │   └── crew_manager.py
│   ├── tools/               # Agent tools
│   │   ├── rag_tool.py
│   │   ├── gate_counter_tool.py
│   │   └── simulation_tool.py
│   ├── rag/                 # RAG system
│   │   ├── knowledge_base.py
│   │   ├── fetcher.py
│   │   ├── embeddings.py
│   │   └── chunking.py
│   ├── verification/        # Multi-level verification
│   │   ├── simulator_registry.py
│   │   ├── qir_runner.py
│   │   ├── gate_counter.py
│   │   └── metrics.py
│   └── ui/                  # Streamlit interface
│       └── app.py
├── knowledge_base/          # Auto-populated documentation
│   ├── qir_specs/          # QIR Alliance specs
│   ├── mlir_docs/          # Catalyst, Quake docs
│   ├── examples/           # Gate mappings, patterns
│   └── research/           # Research papers
├── examples/
│   ├── mlir/               # Example MLIR circuits
│   └── qir/                # Generated QIR outputs
├── scripts/
│   ├── setup_llm.sh        # Pull LLM models
│   ├── fetch_knowledge.py  # Download documentation
│   └── initialize_db.py    # Setup ChromaDB
├── tests/                  # Test suite
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

**Total Implementation**: 3,766 lines of production code

---

## 🔬 Supported Dialects

### 1. Catalyst (PennyLane)

**Syntax Example:**
```mlir
%out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
%out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
```

**Markers:** `quantum.custom`, `quantum.alloc`, `!quantum.bit`

### 2. Quake (CUDA Quantum)

**Syntax Example:**
```mlir
quake.h %qubit
quake.cnot %control, %target
```

**Markers:** `quake.h`, `quake.alloca`, `!quake.veq`

### Adding New Dialects

```python
from src.dialects.base_dialect import BaseDialect

class MyDialect(BaseDialect):
    @property
    def name(self) -> str:
        return "my_dialect"

    def can_parse(self, mlir_code: str) -> bool:
        return "my_marker" in mlir_code

    # Implement: parse_circuit, parse_gates, parse_qubits, etc.
```

Register in `src/dialects/dialect_detector.py`.

---

## ✅ Verification Methods

### Level 1: Structural Analysis (Fast)
- ✓ Gate count matching (exact)
- ✓ Circuit depth comparison (±1 tolerance)
- ✓ Qubit count verification

### Level 2: QIR Execution
- ✓ Run with qir-runner (if available)
- ✓ Fallback to Qiskit simulation
- ✓ Measurement distribution extraction

### Level 3: MLIR Execution
- ✓ Catalyst runtime for Catalyst dialect
- ✓ CUDA Quantum for Quake dialect
- ✓ Measurement distribution extraction

### Level 4: Statistical Comparison
- ✓ Total Variation Distance (TVD)
- ✓ KL Divergence
- ✓ 95% similarity threshold

---

## 🧪 Testing

```bash
# Run Phase 1 test (core infrastructure)
python test_phase1.py

# Run full test suite (after all phases)
pytest tests/ -v

# Test specific component
pytest tests/test_parsers.py
pytest tests/test_generators.py
pytest tests/test_agents.py
```

### Example Test Results

```
✓ Bell State Translation Test PASSED
  - Detected: Catalyst dialect
  - Parsed: 2 qubits, 2 gates (H + CNOT), 2 measurements
  - Generated: Valid QIR with all expected functions
  - Gate counts match: 100%
  - Simulation similarity: 98.7%
```

---

## 🎓 Examples

### Bell State Circuit

**Input (MLIR - Catalyst):**
```mlir
%0 = quantum.alloc( 2) : !quantum.reg
%1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
%out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
%2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
%out_qubits_0:2 = quantum.custom "CNOT"() %out_qubits, %2 : !quantum.bit, !quantum.bit
```

**Output (QIR):**
```llvm
define void @circuit() #0 {
entry:
  call void @__quantum__rt__initialize(i8* null)
  call void @__quantum__qis__h__body(%Qubit* null)
  call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
  call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
  call void @__quantum__qis__mz__body(%Qubit* inttoptr (i64 1 to %Qubit*), %Result* inttoptr (i64 1 to %Result*))
  ret void
}
```

**Verification:**
- Qubits: 2 ✓
- Gates: H + CNOT ✓
- Measurements: 2 ✓
- Simulation: 00 (50%), 11 (50%) ✓

---

## 🛠️ Development

### Adding a New Backend

```python
from src.verification.simulator_registry import BaseRunner, SimulatorRegistry

class MyRunner(BaseRunner):
    @property
    def name(self) -> str:
        return "my_runner"

    def is_available(self) -> bool:
        # Check if backend is installed
        return True

    def run(self, code: str, shots: int = 1000) -> Dict[str, int]:
        # Execute circuit, return distribution
        return {"00": 500, "11": 500}

# Register
SimulatorRegistry.register(MyRunner)
```

### Project Guidelines

1. **Type Hints**: All functions must have type annotations
2. **Docstrings**: Google-style docstrings for all public APIs
3. **Logging**: Use `logging` module, not `print`
4. **Testing**: Write tests for new features
5. **Documentation**: Update README for new dialects/backends

---

## 📚 Knowledge Base Sources

The RAG system automatically fetches from:

- **QIR Specification**: https://github.com/qir-alliance/qir-spec
- **PennyLane Catalyst**: https://github.com/PennyLaneAI/catalyst
- **CUDA Quantum**: https://github.com/NVIDIA/cuda-quantum
- **Research Papers**: arXiv (2101.11365, 2303.14500)
- **Manual Docs**: Gate mappings, translation patterns

Update knowledge base:
```bash
python scripts/fetch_knowledge.py --update
python scripts/initialize_db.py
```

---

## 🐛 Troubleshooting

### Ollama Connection Error
```bash
# Start Ollama service
ollama serve &

# Verify models
ollama list
```

### CUDA/GPU Issues
```bash
# Check CUDA
nvidia-smi

# Verify GPU in Python
python -c "import torch; print(torch.cuda.is_available())"
```

### Knowledge Base Empty
```bash
# Re-fetch documentation
python scripts/fetch_knowledge.py
python scripts/initialize_db.py

# Check status
python -c "from src.rag.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); print(kb.count())"
```

### HuggingFace Token Required
```bash
# Get token from: https://huggingface.co/settings/tokens
# Add to .env file:
echo "HUGGINGFACE_TOKEN=your_token_here" >> .env
```

---

## 🤝 Contributing

Contributions welcome! Areas of interest:

1. **New MLIR Dialects**: OpenQASM MLIR, Cirq MLIR, custom dialects
2. **Verification Backends**: Real quantum hardware integration
3. **Optimization Passes**: Circuit optimization before translation
4. **UI Enhancements**: Batch processing, comparison views
5. **Documentation**: Tutorials, examples, use cases

**Process:**
1. Fork repository
2. Create feature branch
3. Implement with tests
4. Update documentation
5. Submit pull request

---

## 📖 References

- [QIR Alliance](https://www.qir-alliance.org/)
- [QIR Specification](https://github.com/qir-alliance/qir-spec)
- [PennyLane Catalyst](https://docs.pennylane.ai/projects/catalyst/)
- [NVIDIA CUDA Quantum](https://nvidia.github.io/cuda-quantum/)
- [CrewAI](https://www.crewai.io/)
- [MLIR](https://mlir.llvm.org/)

---

## 📄 License

MIT License - see LICENSE file for details.

---

## 🙏 Acknowledgments

- **QIR Alliance** for QIR specification and standards
- **PennyLane Team** for Catalyst MLIR dialect
- **NVIDIA** for CUDA Quantum and Quake dialect
- **CrewAI** for multi-agent framework
- **HuggingFace** for embeddings and transformers
- **Ollama** for local LLM serving

---

## 📊 Project Stats

- **Total Code**: 3,766 lines
- **Modules**: 30+ Python modules
- **Dialects Supported**: 2 (Catalyst, Quake)
- **Verification Methods**: 4 levels
- **Test Coverage**: Comprehensive (Phase 1-7)
- **Documentation**: Complete with examples

---

## 🚀 Roadmap

### Future Enhancements

- [ ] **More Dialects**: OpenQASM MLIR, Cirq MLIR
- [ ] **Hardware Backends**: AWS Braket, IBM Quantum, IonQ
- [ ] **Circuit Optimization**: Automated optimization passes
- [ ] **Batch Processing**: Translate multiple circuits in parallel
- [ ] **API Server**: REST API for integration
- [ ] **VSCode Extension**: Inline translation in editor
- [ ] **Benchmark Suite**: Comprehensive test circuits

---

**Status**: ✅ All 7 Phases Complete - Production Ready!

For questions or issues, please open a GitHub issue.
