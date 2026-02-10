#!/usr/bin/env python3
"""Initialize ChromaDB with knowledge base documents."""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from rag.knowledge_base import KnowledgeBase

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to initialize database."""
    print("=" * 60)
    print("MLIR to QIR Translator - Database Initialization")
    print("=" * 60)
    print()

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print(f"Project root: {project_root}")
    print()

    # Check if knowledge base exists
    kb_dir = project_root / 'knowledge_base'
    if not kb_dir.exists():
        print("⚠ Warning: knowledge_base directory not found!")
        print("Run 'python scripts/fetch_knowledge.py' first to download documentation.")
        return

    # Initialize knowledge base
    print("[1/2] Initializing ChromaDB...")
    kb = KnowledgeBase(
        persist_directory=str(project_root / 'data' / 'chromadb'),
        embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )
    print()

    # Load and index documents
    print("[2/2] Loading and indexing documents...")
    print("This may take a few minutes...")
    print()

    kb.initialize(
        knowledge_dir=str(kb_dir),
        chunk_size=1000,
        chunk_overlap=200
    )
    print()

    # Show statistics
    stats = kb.get_statistics()
    print("=" * 60)
    print("Database Statistics:")
    print("=" * 60)
    print(f"Total documents: {stats['total_documents']}")
    print(f"Unique sources: {stats['unique_sources']}")
    print()
    print("Categories:")
    for category, count in stats['categories'].items():
        print(f"  - {category}: {count} documents")
    print()

    # Test query
    print("=" * 60)
    print("Testing RAG retrieval...")
    print("=" * 60)
    print()

    test_query = "How to translate Hadamard gate from MLIR to QIR?"
    print(f"Query: {test_query}")
    print()

    results = kb.query(test_query, n_results=3)

    for i, doc in enumerate(results, 1):
        print(f"Result {i}:")
        print(f"  Source: {doc.metadata.get('source', 'unknown')}")
        print(f"  Preview: {doc.content[:200]}...")
        print()

    print("=" * 60)
    print("✓ Database initialization complete!")
    print("=" * 60)
    print()
    print("Knowledge base is ready for use!")


if __name__ == '__main__':
    main()
