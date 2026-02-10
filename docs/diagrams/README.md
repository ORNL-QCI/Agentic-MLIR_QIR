# MLIR to QIR Translator - System Diagrams

This directory contains PlantUML diagrams for the MLIR to QIR Quantum Circuit Translator system.

## Viewing the Diagrams

### Using VSCode
1. Install the PlantUML extension in VSCode
2. Open any `.puml` file
3. Press `Alt+D` (Windows/Linux) or `Option+D` (Mac) to preview

### Using PlantUML Online
Visit: http://www.plantuml.com/plantuml/uml/

## Available Diagrams

### 1. Class Diagram (`class_diagram.puml`)
Shows the complete object-oriented structure of the system including:
- **Dialect System**: Base classes and concrete implementations (Catalyst, Quake)
- **Data Models**: MLIRCircuit, GateOperation, QubitAllocation, etc.
- **Core Translation**: MLIRParser, QIRGenerator, templates
- **RAG System**: KnowledgeBase, document fetching, embeddings
- **Multi-Agent System**: CrewManager, TranslationAgent, VerificationAgent
- **Verification System**: BaseRunner implementations, metrics
- **UI Layer**: Streamlit components, configuration
- **Relationships**: Inheritance, composition, dependencies

### 2. Sequence Diagram (`sequence_diagram.puml`)
Illustrates the complete translation workflow with two flows:
- **Basic Translation Flow**: Direct MLIR parsing and QIR generation
  - User input → Parser → Dialect detection → QIR generation → Display
- **Multi-Agent Flow**: LLM-powered translation with verification
  - Translation agent with RAG context
  - Verification agent with gate counting and simulation
  - Iterative refinement (up to 3 iterations)
  - Statistical comparison and feedback

### 3. Architecture Overview (`architecture_overview.puml`)
High-level component diagram showing:
- **5 Main Layers**:
  1. User Interface Layer (Streamlit)
  2. Application Layer (Session, Config)
  3. Multi-Agent System (LLM-powered)
  4. Core Translation Engine
  5. Knowledge Base & RAG
  6. Verification & Execution
- **External Systems**: Ollama LLM, GitHub, arXiv, HuggingFace
- **Data Flow**: How information moves through the system
- **Component Interactions**: Ports, interfaces, dependencies

## Key Architectural Patterns

### 1. Plugin Architecture
The system uses extensible plugin patterns for:
- **Dialects**: New MLIR dialects can be added by implementing `BaseDialect`
- **Runners**: New execution backends via `BaseRunner`
- **Tools**: Agent tools can be registered dynamically

### 2. Multi-Agent Pattern
- **CrewManager**: Orchestrates multiple specialized agents
- **TranslationAgent**: Focuses on accurate MLIR→QIR conversion
- **VerificationAgent**: Validates translation correctness
- **Iterative Refinement**: Agents work together to improve quality

### 3. RAG (Retrieval-Augmented Generation)
- Vector database (ChromaDB) stores documentation and examples
- Semantic search retrieves relevant context for LLM
- Improves translation accuracy with real examples

### 4. Multi-Level Verification
- **Level 1**: Structural analysis (gate counts, depth)
- **Level 2**: QIR execution (qir-runner)
- **Level 3**: MLIR execution (dialect-specific)
- **Level 4**: Statistical comparison (similarity metrics)

## System Statistics

- **Total Code**: 3,766 lines
- **Modules**: 33 Python modules
- **Dialects**: 2 (Catalyst, Quake) + extensible
- **Verification Levels**: 4
- **LLM Models**: 3 supported (8B, 13B, 70B)
- **Knowledge Sources**: 5 (QIR specs, Catalyst, CUDA Quantum, papers, examples)

## Component Responsibilities

### Parser Layer
- Auto-detects MLIR dialect
- Extracts quantum operations
- Creates structured circuit representation

### Generator Layer
- Converts circuit to QIR format
- Uses templates for code generation
- Handles qubit/result pointer mapping

### Agent Layer
- Leverages LLM for intelligent translation
- Retrieves relevant examples via RAG
- Verifies correctness through multiple checks

### Verification Layer
- Executes both MLIR and QIR circuits
- Compares measurement distributions
- Provides statistical similarity metrics

## Technology Stack

- **UI**: Streamlit
- **LLM**: Ollama (Llama 3.1, CodeLlama)
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers (HuggingFace)
- **Quantum**: PennyLane Catalyst, CUDA Quantum, Qiskit
- **Framework**: CrewAI (multi-agent orchestration)

## Design Principles

1. **Extensibility**: Easy to add new dialects, runners, tools
2. **Modularity**: Clear separation of concerns
3. **Testability**: Each component can be tested independently
4. **Configurability**: Settings via environment variables
5. **Observability**: Comprehensive logging and metrics
6. **Robustness**: Multi-level validation and error handling

---

For more information, see the main README.md in the project root.
