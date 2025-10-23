"""Base collector class."""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class BaseCollector(ABC):
    """Base class for all data collectors."""

    def __init__(self, timeout: int = 30):
        """Initialize collector.

        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Create async context."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Clean up async context."""
        if self.session:
            await self.session.close()

    async def fetch_url(
        self, url: str, return_soup: bool = True
    ) -> Optional[BeautifulSoup | str]:
        """Fetch URL content.

        Args:
            url: URL to fetch
            return_soup: Whether to return BeautifulSoup object or raw HTML

        Returns:
            BeautifulSoup object or raw HTML string, None if failed
        """
        try:
            if not self.session:
                raise RuntimeError("Collector must be used as async context manager")

            async with self.session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    if return_soup:
                        return BeautifulSoup(html, "lxml")
                    return html
                else:
                    logger.warning(f"Failed to fetch {url}: HTTP {response.status}")
                    return None

        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    async def google_search(self, query: str, num_results: int = 5) -> list[Dict[str, str]]:
        """Perform Google search using Serper API.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results with title, link, snippet
        """
        from app.config import get_settings

        settings = get_settings()

        if not settings.serper_api_key:
            logger.warning("Serper API key not configured, returning empty results")
            return []

        try:
            url = "https://google.serper.dev/search"
            payload = {"q": query, "num": num_results}
            headers = {
                "X-API-KEY": settings.serper_api_key,
                "Content-Type": "application/json",
            }

            if not self.session:
                raise RuntimeError("Collector must be used as async context manager")

            async with self.session.post(url, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    results = []
                    for item in data.get("organic", [])[:num_results]:
                        results.append(
                            {
                                "title": item.get("title", ""),
                                "link": item.get("link", ""),
                                "snippet": item.get("snippet", ""),
                            }
                        )
                    return results
                else:
                    logger.error(f"Serper API error: HTTP {response.status}")
                    return []

        except Exception as e:
            logger.error(f"Error performing Google search: {e}")
            return []

    @abstractmethod
    async def collect(self, **kwargs) -> Dict[str, Any]:
        """Collect data.

        Args:
            **kwargs: Collector-specific parameters

        Returns:
            Collected data dictionary
        """
        pass
