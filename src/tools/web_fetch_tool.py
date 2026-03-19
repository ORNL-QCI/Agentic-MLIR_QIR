"""Web fetching tool for CrewAI agents — used when researching unknown MLIR dialects."""

import logging
import os
import re

logger = logging.getLogger(__name__)

_MAX_CONTENT_CHARS = 8000


class WebFetchTool:
    """Fetch and return the text content of a URL.

    Uses BeautifulSoup when available, falls back to simple tag stripping.
    Registered as a crewai BaseTool so agents can call it by name.
    """

    name: str = "Read website content"
    description: str = (
        "Fetch the text content of a given URL. "
        "Use this to read MLIR dialect documentation, GitHub READMEs, or spec pages. "
        "Input: a full URL string (e.g. https://mlir.llvm.org/docs/Dialects/...)."
    )

    def _run(self, url: str) -> str:
        try:
            import requests
            r = requests.get(
                url, timeout=15,
                headers={"User-Agent": "mlir-qir-translator-agent/1.0"}
            )
            r.raise_for_status()
            try:
                from bs4 import BeautifulSoup
                text = BeautifulSoup(r.text, "html.parser").get_text(separator="\n")
            except ImportError:
                text = re.sub(r'<[^>]+>', '', r.text)
            # Collapse excessive blank lines
            text = re.sub(r'\n{3,}', '\n\n', text).strip()
            return text[:_MAX_CONTENT_CHARS]
        except Exception as e:
            return f"Error fetching {url}: {e}"


def fetch_url_content(url: str, max_chars: int = _MAX_CONTENT_CHARS) -> str:
    """Fetch and return stripped text content from a URL.

    Standalone helper for the HITL documentation feature (no CrewAI required).
    Returns an error string (never raises) so callers can display it in the UI.
    """
    tool = WebFetchTool()
    original_limit = _MAX_CONTENT_CHARS
    # Temporarily allow a larger fetch for full doc pages
    result = tool._run(url)
    if max_chars != original_limit and not result.startswith("Error"):
        result = result[:max_chars]
    return result


def get_web_tools() -> list:
    """Return available web tools. Never raises — returns empty list on failure."""
    tools = []
    try:
        # Try crewai_tools ScrapeWebsiteTool first (richer, handles JS-rendered pages)
        from crewai_tools import ScrapeWebsiteTool
        tools.append(ScrapeWebsiteTool())
        logger.debug("ScrapeWebsiteTool added")
    except Exception:
        # Fall back to our lightweight implementation
        try:
            from crewai.tools import BaseTool

            class _WebFetch(BaseTool):
                name: str = "Read website content"
                description: str = WebFetchTool.description

                def _run(self, url: str) -> str:
                    return WebFetchTool()._run(url)

            tools.append(_WebFetch())
            logger.debug("Fallback WebFetchTool added")
        except Exception as e:
            logger.warning(f"Could not create web fetch tool: {e}")

    try:
        if os.environ.get('SERPER_API_KEY'):
            from crewai_tools import SerperDevTool
            tools.append(SerperDevTool())
            logger.debug("SerperDevTool added")
    except Exception:
        pass

    return tools
