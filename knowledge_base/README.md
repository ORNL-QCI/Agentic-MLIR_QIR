# Knowledge Base

This directory contains all documents indexed by the RAG tool used by the Translation Agent.

## Directory Structure

```
knowledge_base/
├── examples/       # Gate mappings, circuit translation patterns
├── mlir_docs/      # MLIR dialect documentation (Catalyst, Quake, CUDA-Q)
├── qir_specs/      # QIR specification files
└── research/       # arXiv papers (PDF + metadata)
```

## How to Add New Knowledge

### Option 1 — Drop a file directly (simplest)

Place any `.md`, `.txt`, or `.rst` file in the appropriate subfolder:

| Content type | Folder |
|---|---|
| Gate mappings, circuit examples | `examples/` |
| Dialect docs (new MLIR dialects) | `mlir_docs/` |
| QIR spec updates | `qir_specs/` |
| Research papers (text) | `research/` |

Then re-index:

```bash
python scripts/initialize_db.py
```

### Option 2 — Add hand-written reference material

Edit `create_manual_docs()` in [src/rag/fetcher.py](../src/rag/fetcher.py) to add a new string block
and write it to a file. This is best for curated reference content like new gate mappings or
dialect translation patterns.

Then run:

```bash
python scripts/fetch_knowledge.py
python scripts/initialize_db.py
```

### Option 3 — Add an online source

Add an entry to the `SOURCES` dict in [src/rag/fetcher.py](../src/rag/fetcher.py). Three source
types are supported:

**GitHub raw files:**
```python
'my_dialect_docs': {
    'type': 'github_raw',
    'repo': 'owner/repo',
    'branch': 'main',
    'files': ['path/to/doc.md'],
    'dest': 'knowledge_base/mlir_docs/'
}
```

**Direct URLs:**
```python
'my_web_source': {
    'type': 'web',
    'urls': ['https://example.com/doc.md'],
    'dest': 'knowledge_base/mlir_docs/'
}
```

**arXiv papers:**
```python
'my_papers': {
    'type': 'arxiv',
    'papers': ['2101.11365'],   # arXiv ID
    'dest': 'knowledge_base/research/'
}
```

Then run:

```bash
python scripts/fetch_knowledge.py
python scripts/initialize_db.py
```

## Re-indexing

Any time you add or modify files, re-run `initialize_db.py` to rebuild the ChromaDB vector store:

```bash
python scripts/initialize_db.py
```

The script scans all files in this directory, chunks them, and stores embeddings in `chroma_db/`.
