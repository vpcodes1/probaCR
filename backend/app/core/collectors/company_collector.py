"""Company data collector."""
import logging
import re
from typing import Any, Dict, Optional

from .base_collector import BaseCollector

logger = logging.getLogger(__name__)


class CompanyCollector(BaseCollector):
    """Collects company information from various sources."""

    async def collect(self, company_name: str, **kwargs) -> Dict[str, Any]:
        """Collect company data.

        Args:
            company_name: Name of the company

        Returns:
            Dictionary with company data
        """
        logger.info(f"Collecting data for company: {company_name}")

        data = {
            "company_name": company_name,
            "website": None,
            "description": None,
            "industry": None,
            "size": None,
            "founded": None,
            "headquarters": None,
            "funding": None,
            "key_people": [],
            "recent_news": [],
            "social_media": {},
        }

        # Search for company information
        search_results = await self.google_search(f"{company_name} company", num_results=5)

        if search_results:
            # Try to find company website
            for result in search_results:
                link = result.get("link", "")
                # Simple heuristic: website usually contains company name in domain
                if self._is_company_website(link, company_name):
                    data["website"] = link
                    break

            # Get description from search snippet
            if search_results:
                data["description"] = search_results[0].get("snippet", "")

        # Try to get more details from company website
        if data["website"]:
            website_data = await self._scrape_company_website(data["website"])
            data.update(website_data)

        # Search for funding information
        funding_results = await self.google_search(
            f"{company_name} funding round investment", num_results=3
        )
        data["funding"] = self._extract_funding_info(funding_results)

        # Search for company size and industry info
        about_results = await self.google_search(
            f"{company_name} company size employees industry", num_results=3
        )
        size_industry = self._extract_size_and_industry(about_results)
        data.update(size_industry)

        logger.info(f"Company data collection completed for: {company_name}")
        return data

    def _is_company_website(self, url: str, company_name: str) -> bool:
        """Check if URL is likely the company's official website.

        Args:
            url: URL to check
            company_name: Company name

        Returns:
            True if likely company website
        """
        # Remove common words and convert to lowercase
        clean_name = company_name.lower().replace(" ", "").replace("inc", "").replace("llc", "")
        clean_url = url.lower()

        # Check if company name is in domain
        return clean_name in clean_url and not any(
            x in clean_url for x in ["linkedin", "facebook", "twitter", "crunchbase", "wikipedia"]
        )

    async def _scrape_company_website(self, url: str) -> Dict[str, Any]:
        """Scrape company website for additional information.

        Args:
            url: Company website URL

        Returns:
            Dictionary with scraped data
        """
        data = {}

        try:
            soup = await self.fetch_url(url)
            if not soup:
                return data

            # Try to extract information from meta tags
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                data["meta_description"] = meta_desc.get("content")

            # Look for about page
            about_link = soup.find("a", href=re.compile(r"/(about|company|who-we-are)", re.I))
            if about_link:
                about_url = about_link.get("href")
                if about_url.startswith("/"):
                    about_url = url.rstrip("/") + about_url
                # Could scrape about page here for more details

            # Look for social media links
            social_patterns = {
                "linkedin": r"linkedin\.com/company/",
                "twitter": r"(twitter|x)\.com/",
                "facebook": r"facebook\.com/",
            }

            for platform, pattern in social_patterns.items():
                social_link = soup.find("a", href=re.compile(pattern))
                if social_link:
                    data.setdefault("social_media", {})[platform] = social_link.get("href")

        except Exception as e:
            logger.error(f"Error scraping company website {url}: {e}")

        return data

    def _extract_funding_info(self, search_results: list) -> Optional[str]:
        """Extract funding information from search results.

        Args:
            search_results: List of search result dictionaries

        Returns:
            Funding information string or None
        """
        funding_keywords = ["raised", "funding", "million", "billion", "series", "round"]

        for result in search_results:
            snippet = result.get("snippet", "").lower()
            if any(keyword in snippet for keyword in funding_keywords):
                return result.get("snippet")

        return None

    def _extract_size_and_industry(self, search_results: list) -> Dict[str, Optional[str]]:
        """Extract company size and industry from search results.

        Args:
            search_results: List of search result dictionaries

        Returns:
            Dictionary with size and industry info
        """
        data = {"size": None, "industry": None}

        for result in search_results:
            snippet = result.get("snippet", "")

            # Look for employee count
            if not data["size"]:
                employee_match = re.search(r"(\d+[\d,]*)\s*employees", snippet, re.I)
                if employee_match:
                    data["size"] = f"{employee_match.group(1)} employees"

            # Look for industry mentions
            if not data["industry"]:
                industry_keywords = [
                    "software",
                    "technology",
                    "healthcare",
                    "finance",
                    "retail",
                    "manufacturing",
                    "consulting",
                    "education",
                ]
                for keyword in industry_keywords:
                    if keyword in snippet.lower():
                        data["industry"] = keyword.title()
                        break

        return data
