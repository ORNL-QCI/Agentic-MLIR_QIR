"""Automatically fetch documentation from official sources."""

import os
import requests
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class KnowledgeFetcher:
    """Fetch knowledge base content from official sources."""

    # Configuration for knowledge sources
    SOURCES = {
        'qir_spec': {
            'type': 'github_raw',
            'repo': 'qir-alliance/qir-spec',
            'branch': 'main',
            'files': [
                'specification/under_development/2_Data_Types.md',
                'specification/under_development/3_Callables.md',
                'specification/under_development/profiles/Base_Profile.md',
            ],
            'dest': 'knowledge_base/qir_specs/'
        },
        'qir_examples': {
            'type': 'web',
            'urls': [
                'https://raw.githubusercontent.com/qir-alliance/qir-spec/main/specification/under_development/examples/simple_circuit.ll',
            ],
            'dest': 'knowledge_base/examples/'
        },
        'catalyst_docs': {
            'type': 'github_raw',
            'repo': 'PennyLaneAI/catalyst',
            'branch': 'main',
            'files': [
                'doc/dev/dialects/quantum.md',
                'doc/dev/dialects/catalyst.md',
            ],
            'dest': 'knowledge_base/mlir_docs/'
        },
        'cudaq_docs': {
            'type': 'web',
            'urls': [
                'https://raw.githubusercontent.com/NVIDIA/cuda-quantum/main/docs/sphinx/using/advanced/cudaq_ir.rst',
            ],
            'dest': 'knowledge_base/mlir_docs/'
        },
        'arxiv_papers': {
            'type': 'arxiv',
            'papers': [
                '2101.11365',  # MLIR Dialect for Quantum
                '2303.14500',  # Formalization of QIR
            ],
            'dest': 'knowledge_base/research/'
        }
    }

    def __init__(self, base_dir: str = '.'):
        """Initialize knowledge fetcher.

        Args:
            base_dir: Base directory for the project
        """
        self.base_dir = Path(base_dir)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MLIR-QIR-Translator/1.0'
        })

    def fetch_all(self, sources: Optional[List[str]] = None):
        """Fetch all or specified knowledge sources.

        Args:
            sources: List of source names to fetch. If None, fetch all.
        """
        if sources is None:
            sources = list(self.SOURCES.keys())

        logger.info(f"Fetching {len(sources)} knowledge sources...")

        for source_name in sources:
            if source_name not in self.SOURCES:
                logger.warning(f"Unknown source: {source_name}")
                continue

            try:
                logger.info(f"Fetching {source_name}...")
                self.fetch_source(source_name)
                logger.info(f"✓ {source_name} fetched successfully")
            except Exception as e:
                logger.error(f"✗ Failed to fetch {source_name}: {str(e)}")

    def fetch_source(self, name: str):
        """Fetch a single knowledge source.

        Args:
            name: Source name from SOURCES dict
        """
        config = self.SOURCES[name]
        source_type = config['type']

        if source_type == 'github_raw':
            self._fetch_github_raw(config)
        elif source_type == 'web':
            self._fetch_web(config)
        elif source_type == 'arxiv':
            self._fetch_arxiv(config)
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    def _fetch_github_raw(self, config: Dict):
        """Fetch files from GitHub raw content.

        Args:
            config: Source configuration dict
        """
        repo = config['repo']
        branch = config.get('branch', 'main')
        files = config['files']
        dest = self.base_dir / config['dest']

        dest.mkdir(parents=True, exist_ok=True)

        for file_path in files:
            url = f"https://raw.githubusercontent.com/{repo}/{branch}/{file_path}"
            filename = Path(file_path).name
            dest_path = dest / filename

            logger.debug(f"Downloading {url}...")

            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                with open(dest_path, 'wb') as f:
                    f.write(response.content)

                logger.debug(f"Saved to {dest_path}")

            except requests.RequestException as e:
                logger.warning(f"Failed to fetch {url}: {str(e)}")

    def _fetch_web(self, config: Dict):
        """Fetch files from direct URLs.

        Args:
            config: Source configuration dict
        """
        urls = config['urls']
        dest = self.base_dir / config['dest']

        dest.mkdir(parents=True, exist_ok=True)

        for url in urls:
            parsed = urlparse(url)
            filename = Path(parsed.path).name
            dest_path = dest / filename

            logger.debug(f"Downloading {url}...")

            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                with open(dest_path, 'wb') as f:
                    f.write(response.content)

                logger.debug(f"Saved to {dest_path}")

            except requests.RequestException as e:
                logger.warning(f"Failed to fetch {url}: {str(e)}")

    def _fetch_arxiv(self, config: Dict):
        """Fetch papers from arXiv.

        Args:
            config: Source configuration dict
        """
        try:
            import arxiv
        except ImportError:
            logger.warning("arxiv package not installed. Skipping arXiv papers.")
            logger.info("Install with: pip install arxiv")
            return

        papers = config['papers']
        dest = self.base_dir / config['dest']

        dest.mkdir(parents=True, exist_ok=True)

        for paper_id in papers:
            try:
                logger.debug(f"Fetching arXiv paper {paper_id}...")

                # Search for paper
                search = arxiv.Search(id_list=[paper_id])
                paper = next(search.results())

                # Download PDF
                pdf_path = dest / f"{paper_id}.pdf"
                paper.download_pdf(filename=str(pdf_path))

                # Save metadata as text
                metadata_path = dest / f"{paper_id}_metadata.txt"
                with open(metadata_path, 'w') as f:
                    f.write(f"Title: {paper.title}\n")
                    f.write(f"Authors: {', '.join([a.name for a in paper.authors])}\n")
                    f.write(f"Published: {paper.published}\n")
                    f.write(f"Summary: {paper.summary}\n")
                    f.write(f"arXiv ID: {paper_id}\n")
                    f.write(f"URL: {paper.entry_id}\n")

                logger.debug(f"Saved paper to {pdf_path}")

            except Exception as e:
                logger.warning(f"Failed to fetch paper {paper_id}: {str(e)}")

    def create_manual_docs(self):
        """Create manual documentation files for core concepts."""
        logger.info("Creating manual documentation files...")

        # Gate mappings reference
        gate_mappings_content = """# MLIR to QIR Gate Mappings

## Single-Qubit Gates

| MLIR Gate (Catalyst) | QIR Function | Parameters |
|---------------------|--------------|------------|
| Hadamard | `__quantum__qis__h__body` | `%Qubit*` |
| PauliX | `__quantum__qis__x__body` | `%Qubit*` |
| PauliY | `__quantum__qis__y__body` | `%Qubit*` |
| PauliZ | `__quantum__qis__z__body` | `%Qubit*` |
| S | `__quantum__qis__s__body` | `%Qubit*` |
| T | `__quantum__qis__t__body` | `%Qubit*` |

## Parameterized Gates

| MLIR Gate | QIR Function | Parameters |
|-----------|--------------|------------|
| RX | `__quantum__qis__rx__body` | `double, %Qubit*` |
| RY | `__quantum__qis__ry__body` | `double, %Qubit*` |
| RZ | `__quantum__qis__rz__body` | `double, %Qubit*` |

## Two-Qubit Gates

| MLIR Gate | QIR Function | Parameters |
|-----------|--------------|------------|
| CNOT | `__quantum__qis__cnot__body` | `%Qubit*, %Qubit*` |
| CZ | `__quantum__qis__cz__body` | `%Qubit*, %Qubit*` |
| SWAP | `__quantum__qis__swap__body` | `%Qubit*, %Qubit*` |

## Measurements

| MLIR Operation | QIR Function | Parameters |
|----------------|--------------|------------|
| quantum.measure | `__quantum__qis__mz__body` | `%Qubit*, %Result*` |

## Qubit Pointers

In QIR, qubits are represented as pointers:
- Qubit 0: `null`
- Qubit 1: `inttoptr (i64 1 to %Qubit*)`
- Qubit n: `inttoptr (i64 n to %Qubit*)`

## Examples

### Hadamard Gate

**MLIR (Catalyst):**
```mlir
%out_qubits = quantum.custom "Hadamard"() %1 : !quantum.bit
```

**QIR:**
```llvm
call void @__quantum__qis__h__body(%Qubit* null)
```

### CNOT Gate

**MLIR (Catalyst):**
```mlir
%out_qubits:2 = quantum.custom "CNOT"() %control, %target : !quantum.bit, !quantum.bit
```

**QIR:**
```llvm
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
```
"""

        examples_dir = self.base_dir / 'knowledge_base' / 'examples'
        examples_dir.mkdir(parents=True, exist_ok=True)

        with open(examples_dir / 'gate_mappings.md', 'w') as f:
            f.write(gate_mappings_content)

        logger.info("✓ Created gate_mappings.md")

        # Translation patterns
        translation_patterns = """# Common Translation Patterns

## Pattern 1: Qubit Allocation

### MLIR (Catalyst)
```mlir
%0 = quantum.alloc( 2) : !quantum.reg
%1 = quantum.extract %0[ 0] : !quantum.reg -> !quantum.bit
%2 = quantum.extract %0[ 1] : !quantum.reg -> !quantum.bit
```

### QIR
```llvm
; Qubits are statically allocated
; Qubit 0: null
; Qubit 1: inttoptr (i64 1 to %Qubit*)
```

## Pattern 2: Gate Sequencing

### MLIR (Catalyst)
```mlir
%out1 = quantum.custom "Hadamard"() %qubit0 : !quantum.bit
%out2:2 = quantum.custom "CNOT"() %out1, %qubit1 : !quantum.bit, !quantum.bit
```

### QIR
```llvm
call void @__quantum__qis__h__body(%Qubit* null)
call void @__quantum__qis__cnot__body(%Qubit* null, %Qubit* inttoptr (i64 1 to %Qubit*))
```

## Pattern 3: Measurements

### MLIR (Catalyst)
```mlir
%mres, %out_qubit = quantum.measure %qubit : i1, !quantum.bit
```

### QIR
```llvm
call void @__quantum__qis__mz__body(%Qubit* null, %Result* null)
```

## Pattern 4: Conditional Operations

### MLIR (Catalyst)
```mlir
%extracted = tensor.extract %condition[] : tensor<i1>
%result = scf.if %extracted -> (!quantum.reg) {
  %gate = quantum.custom "PauliZ"() %qubit : !quantum.bit
  scf.yield %new_reg : !quantum.reg
}
```

### QIR
```llvm
%0 = call i1 @__quantum__qis__read_result__body(%Result* null)
br i1 %0, label %then, label %else

then:
  call void @__quantum__qis__z__body(%Qubit* inttoptr (i64 2 to %Qubit*))
  br label %continue

else:
  br label %continue

continue:
  ; Continue execution
```
"""

        with open(examples_dir / 'translation_patterns.md', 'w') as f:
            f.write(translation_patterns)

        logger.info("✓ Created translation_patterns.md")

    def get_status(self) -> Dict[str, bool]:
        """Check which sources have been fetched.

        Returns:
            Dict mapping source names to fetch status (True if fetched)
        """
        status = {}

        for name, config in self.SOURCES.items():
            dest = self.base_dir / config['dest']
            # Check if destination has files
            status[name] = dest.exists() and any(dest.iterdir())

        return status
