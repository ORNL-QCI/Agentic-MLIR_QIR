#!/usr/bin/env python3
"""Download and prepare knowledge base from official sources."""

import sys
import os
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from rag.fetcher import KnowledgeFetcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function to fetch knowledge."""
    print("=" * 60)
    print("MLIR to QIR Translator - Knowledge Base Fetcher")
    print("=" * 60)
    print()

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print(f"Project root: {project_root}")
    print()

    # Initialize fetcher
    fetcher = KnowledgeFetcher(base_dir=project_root)

    # Create manual documentation
    print("[1/3] Creating manual documentation...")
    fetcher.create_manual_docs()
    print()

    # Fetch from online sources
    print("[2/3] Fetching documentation from official sources...")
    print("This may take a few minutes...")
    print()

    fetcher.fetch_all()
    print()

    # Show status
    print("[3/3] Checking fetch status...")
    status = fetcher.get_status()

    for source, fetched in status.items():
        symbol = "✓" if fetched else "✗"
        print(f"  {symbol} {source}")

    print()
    print("=" * 60)
    print("✓ Knowledge base fetching complete!")
    print("=" * 60)
    print()
    print("Next step: Run 'python scripts/initialize_db.py' to index documents")


if __name__ == '__main__':
    main()
