"""Document chunking for RAG system."""

from typing import List
import re


class DocumentChunker:
    """Chunk documents into smaller pieces for embedding."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize document chunker.

        Args:
            chunk_size: Target size of chunks in characters
            chunk_overlap: Overlap between consecutive chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Separators in order of preference
        self.separators = [
            "\n\n\n",  # Triple newline (section breaks)
            "\n\n",    # Double newline (paragraph breaks)
            "\n",      # Single newline
            ". ",      # Sentence end
            "! ",      # Exclamation
            "? ",      # Question
            "; ",      # Semicolon
            ", ",      # Comma
            " ",       # Space
            ""         # Character-level (last resort)
        ]

    def chunk_documents(self, documents: List) -> List:
        """Chunk a list of documents.

        Args:
            documents: List of Document objects

        Returns:
            List of chunked Document objects
        """
        chunked_docs = []

        for doc in documents:
            chunks = self.chunk_text(doc.content)

            for i, chunk_text in enumerate(chunks):
                # Create new document with chunk metadata
                chunk_metadata = doc.metadata.copy()
                chunk_metadata.update({
                    'chunk_index': i,
                    'total_chunks': len(chunks),
                    'chunk_size': len(chunk_text)
                })

                from .knowledge_base import Document
                chunked_docs.append(Document(
                    content=chunk_text,
                    metadata=chunk_metadata
                ))

        return chunked_docs

    def chunk_text(self, text: str) -> List[str]:
        """Chunk a single text into smaller pieces.

        Args:
            text: Text to chunk

        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        current_chunk = ""

        # Split by separators recursively
        splits = self._split_text_recursive(text, self.separators)

        for split in splits:
            # If adding this split would exceed chunk size, save current chunk
            if len(current_chunk) + len(split) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())

                # Start new chunk with overlap from previous
                if self.chunk_overlap > 0:
                    overlap_text = current_chunk[-self.chunk_overlap:]
                    current_chunk = overlap_text + split
                else:
                    current_chunk = split
            else:
                current_chunk += split

        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    def _split_text_recursive(self, text: str, separators: List[str]) -> List[str]:
        """Recursively split text by separators.

        Args:
            text: Text to split
            separators: List of separators in order of preference

        Returns:
            List of text splits
        """
        if not separators:
            # No more separators, return as-is
            return [text]

        separator = separators[0]
        remaining_separators = separators[1:]

        if separator == "":
            # Character-level split
            return list(text)

        # Split by current separator
        if separator in text:
            splits = text.split(separator)

            # Keep separator with the text (except for last split)
            result = []
            for i, split in enumerate(splits[:-1]):
                result.append(split + separator)

            # Add last split without separator
            if splits[-1]:
                result.append(splits[-1])

            return result
        else:
            # Separator not found, try next separator
            return self._split_text_recursive(text, remaining_separators)


class MarkdownChunker(DocumentChunker):
    """Specialized chunker for Markdown documents."""

    def chunk_text(self, text: str) -> List[str]:
        """Chunk markdown text while preserving structure.

        Args:
            text: Markdown text to chunk

        Returns:
            List of text chunks
        """
        # Try to chunk by headers first
        chunks = self._chunk_by_headers(text)

        # If chunks are too large, further split them
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size:
                # Use parent class method for further splitting
                sub_chunks = super().chunk_text(chunk)
                final_chunks.extend(sub_chunks)
            else:
                final_chunks.append(chunk)

        return final_chunks

    def _chunk_by_headers(self, text: str) -> List[str]:
        """Split markdown by headers.

        Args:
            text: Markdown text

        Returns:
            List of sections
        """
        # Pattern for markdown headers (# through ####)
        header_pattern = r'^(#{1,4})\s+(.+)$'

        lines = text.split('\n')
        chunks = []
        current_chunk = []
        current_header_level = 0

        for line in lines:
            match = re.match(header_pattern, line)

            if match:
                header_level = len(match.group(1))

                # If new section at same or higher level, start new chunk
                if current_chunk and header_level <= current_header_level:
                    chunks.append('\n'.join(current_chunk))
                    current_chunk = []

                current_header_level = header_level

            current_chunk.append(line)

        # Add final chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks
