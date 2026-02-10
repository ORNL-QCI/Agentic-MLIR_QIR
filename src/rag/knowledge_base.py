"""ChromaDB-based knowledge base for RAG system."""

import os
import logging
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

logger = logging.getLogger(__name__)


class Document:
    """Represents a document chunk."""

    def __init__(self, content: str, metadata: Optional[Dict] = None):
        self.content = content
        self.metadata = metadata or {}

    def __repr__(self):
        return f"Document(content_len={len(self.content)}, metadata={self.metadata})"


class KnowledgeBase:
    """ChromaDB-based knowledge base with HuggingFace embeddings."""

    def __init__(self, persist_directory: str = "data/chromadb",
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize knowledge base.

        Args:
            persist_directory: Directory to persist ChromaDB
            embedding_model: HuggingFace model for embeddings
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Setup embedding function
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="mlir_qir_knowledge",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )

        logger.info(f"Knowledge base initialized with {self.collection.count()} documents")

    def initialize(self, knowledge_dir: str = "knowledge_base", chunk_size: int = 1000,
                   chunk_overlap: int = 200):
        """Load and index all documents from knowledge base directory.

        Args:
            knowledge_dir: Directory containing knowledge base files
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        from .chunking import DocumentChunker

        knowledge_path = Path(knowledge_dir)

        if not knowledge_path.exists():
            logger.warning(f"Knowledge directory not found: {knowledge_dir}")
            return

        logger.info(f"Initializing knowledge base from {knowledge_dir}...")

        # Load all markdown files
        documents = []
        for file_path in knowledge_path.rglob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                relative_path = file_path.relative_to(knowledge_path)
                documents.append(Document(
                    content=content,
                    metadata={
                        'source': str(relative_path),
                        'type': 'markdown',
                        'category': relative_path.parts[0] if relative_path.parts else 'other'
                    }
                ))

                logger.debug(f"Loaded {file_path}")

            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {str(e)}")

        if not documents:
            logger.warning("No documents found in knowledge base")
            return

        logger.info(f"Loaded {len(documents)} documents")

        # Chunk documents
        chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunked_docs = chunker.chunk_documents(documents)

        logger.info(f"Created {len(chunked_docs)} chunks")

        # Add to collection
        self.add_documents(chunked_docs)

        logger.info(f"✓ Knowledge base initialized with {self.collection.count()} chunks")

    def add_documents(self, documents: List[Document], batch_size: int = 100):
        """Add documents to the knowledge base.

        Args:
            documents: List of Document objects
            batch_size: Batch size for adding documents
        """
        if not documents:
            return

        # Prepare data for ChromaDB
        ids = []
        contents = []
        metadatas = []

        for i, doc in enumerate(documents):
            doc_id = f"doc_{self.collection.count() + i}"
            ids.append(doc_id)
            contents.append(doc.content)
            metadatas.append(doc.metadata)

        # Add in batches
        for i in range(0, len(documents), batch_size):
            batch_ids = ids[i:i + batch_size]
            batch_contents = contents[i:i + batch_size]
            batch_metadatas = metadatas[i:i + batch_size]

            self.collection.add(
                ids=batch_ids,
                documents=batch_contents,
                metadatas=batch_metadatas
            )

            logger.debug(f"Added batch {i // batch_size + 1}/{(len(documents) - 1) // batch_size + 1}")

    def query(self, query: str, n_results: int = 5,
              where: Optional[Dict] = None) -> List[Document]:
        """Query the knowledge base.

        Args:
            query: Query string
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            List of Document objects
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where
        )

        documents = []
        if results['documents'] and results['documents'][0]:
            for content, metadata in zip(results['documents'][0], results['metadatas'][0]):
                documents.append(Document(
                    content=content,
                    metadata=metadata
                ))

        return documents

    def query_with_scores(self, query: str, n_results: int = 5) -> List[tuple]:
        """Query with similarity scores.

        Args:
            query: Query string
            n_results: Number of results to return

        Returns:
            List of (Document, score) tuples
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )

        documents_with_scores = []
        if results['documents'] and results['documents'][0]:
            for content, metadata, distance in zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
            ):
                doc = Document(content=content, metadata=metadata)
                # Convert distance to similarity (lower distance = higher similarity)
                similarity = 1.0 / (1.0 + distance)
                documents_with_scores.append((doc, similarity))

        return documents_with_scores

    def count(self) -> int:
        """Get number of documents in knowledge base."""
        return self.collection.count()

    def reset(self):
        """Reset the knowledge base (delete all documents)."""
        self.client.delete_collection("mlir_qir_knowledge")
        self.collection = self.client.create_collection(
            name="mlir_qir_knowledge",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Knowledge base reset")

    def get_statistics(self) -> Dict:
        """Get knowledge base statistics."""
        count = self.collection.count()

        # Get sample to determine categories
        if count > 0:
            sample_results = self.collection.get(limit=min(count, 1000))
            categories = {}
            sources = set()

            for metadata in sample_results['metadatas']:
                category = metadata.get('category', 'unknown')
                categories[category] = categories.get(category, 0) + 1
                sources.add(metadata.get('source', 'unknown'))

            return {
                'total_documents': count,
                'categories': categories,
                'unique_sources': len(sources)
            }

        return {'total_documents': 0, 'categories': {}, 'unique_sources': 0}
