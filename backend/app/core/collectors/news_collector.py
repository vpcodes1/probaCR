"""News and recent events collector."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

from .base_collector import BaseCollector

logger = logging.getLogger(__name__)


class NewsCollector(BaseCollector):
    """Collects recent news and events about a company or person."""

    async def collect(
        self,
        company_name: str = "",
        person_name: str = "",
        days_back: int = 90,
        **kwargs,
    ) -> Dict[str, Any]:
        """Collect news data.

        Args:
            company_name: Company name to search for
            person_name: Person name to search for
            days_back: How many days back to search for news

        Returns:
            Dictionary with news data
        """
        logger.info(f"Collecting news for: {company_name or person_name}")

        data = {
            "company_news": [],
            "person_news": [],
            "industry_news": [],
            "recent_events": [],
        }

        # Collect company news
        if company_name:
            company_news = await self._collect_company_news(company_name, days_back)
            data["company_news"] = company_news

        # Collect person news
        if person_name:
            person_news = await self._collect_person_news(person_name, days_back)
            data["person_news"] = person_news

        logger.info("News collection completed")
        return data

    async def _collect_company_news(
        self, company_name: str, days_back: int
    ) -> List[Dict[str, str]]:
        """Collect recent company news.

        Args:
            company_name: Company name
            days_back: Days to look back

        Returns:
            List of news items
        """
        news = []

        # Search for recent news
        queries = [
            f"{company_name} news",
            f"{company_name} announcement",
            f"{company_name} press release",
            f"{company_name} funding",
            f"{company_name} expansion",
        ]

        for query in queries:
            results = await self.google_search(query, num_results=3)
            for result in results:
                news_item = {
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "url": result.get("link", ""),
                    "source": self._extract_domain(result.get("link", "")),
                }

                # Avoid duplicates
                if news_item not in news:
                    news.append(news_item)

        return news[:10]  # Return top 10 news items

    async def _collect_person_news(
        self, person_name: str, days_back: int
    ) -> List[Dict[str, str]]:
        """Collect recent news about a person.

        Args:
            person_name: Person name
            days_back: Days to look back

        Returns:
            List of news items
        """
        news = []

        # Search for person mentions
        queries = [
            f"{person_name} news",
            f"{person_name} interview",
            f"{person_name} speaking",
            f"{person_name} announcement",
        ]

        for query in queries:
            results = await self.google_search(query, num_results=2)
            for result in results:
                news_item = {
                    "title": result.get("title", ""),
                    "snippet": result.get("snippet", ""),
                    "url": result.get("link", ""),
                    "source": self._extract_domain(result.get("link", "")),
                }

                if news_item not in news:
                    news.append(news_item)

        return news[:5]  # Return top 5 news items

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL.

        Args:
            url: Full URL

        Returns:
            Domain name
        """
        try:
            from urllib.parse import urlparse

            parsed = urlparse(url)
            domain = parsed.netloc
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except Exception:
            return "Unknown"

    def _is_recent(self, date_str: str, days_back: int) -> bool:
        """Check if a date string is within the specified days back.

        Args:
            date_str: Date string to check
            days_back: Number of days to look back

        Returns:
            True if date is recent
        """
        try:
            # Try to parse various date formats
            date_formats = ["%Y-%m-%d", "%B %d, %Y", "%b %d, %Y", "%d %B %Y"]

            for fmt in date_formats:
                try:
                    date = datetime.strptime(date_str, fmt)
                    cutoff = datetime.now() - timedelta(days=days_back)
                    return date >= cutoff
                except ValueError:
                    continue

            return False
        except Exception:
            return False
