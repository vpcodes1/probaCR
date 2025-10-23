"""Person/prospect data collector."""
import logging
import re
from typing import Any, Dict, List

from .base_collector import BaseCollector

logger = logging.getLogger(__name__)


class PersonCollector(BaseCollector):
    """Collects information about a specific person."""

    async def collect(
        self, person_name: str, company_name: str = "", **kwargs
    ) -> Dict[str, Any]:
        """Collect person data.

        Args:
            person_name: Name of the person
            company_name: Company they work for (optional but recommended)

        Returns:
            Dictionary with person data
        """
        logger.info(f"Collecting data for person: {person_name}")

        data = {
            "name": person_name,
            "company": company_name,
            "title": None,
            "location": None,
            "education": [],
            "experience": [],
            "skills": [],
            "interests": [],
            "achievements": [],
            "linkedin_url": None,
            "twitter_url": None,
            "personal_website": None,
        }

        # Search for person + company
        search_query = f"{person_name}"
        if company_name:
            search_query += f" {company_name}"

        search_results = await self.google_search(search_query, num_results=10)

        # Extract LinkedIn profile
        for result in search_results:
            link = result.get("link", "")
            if "linkedin.com/in/" in link:
                data["linkedin_url"] = link
                # Try to extract title from snippet
                snippet = result.get("snippet", "")
                title_match = re.search(
                    r"(?:Title|Position|Role):\s*([^|•\n]+)", snippet, re.I
                )
                if title_match:
                    data["title"] = title_match.group(1).strip()
                break

        # Search for educational background
        edu_results = await self.google_search(
            f"{person_name} education university degree", num_results=3
        )
        data["education"] = self._extract_education(edu_results)

        # Search for achievements and awards
        achievement_results = await self.google_search(
            f"{person_name} achievement award recognition", num_results=3
        )
        data["achievements"] = self._extract_achievements(achievement_results)

        # Search for interests and publications
        interest_results = await self.google_search(
            f"{person_name} interests hobbies", num_results=3
        )
        data["interests"] = self._extract_interests(interest_results)

        # Search for Twitter/X profile
        twitter_results = await self.google_search(
            f"{person_name} twitter OR X.com", num_results=3
        )
        for result in twitter_results:
            link = result.get("link", "")
            if "twitter.com" in link or "x.com" in link:
                data["twitter_url"] = link
                break

        logger.info(f"Person data collection completed for: {person_name}")
        return data

    def _extract_education(self, search_results: list) -> List[Dict[str, str]]:
        """Extract education information from search results.

        Args:
            search_results: List of search result dictionaries

        Returns:
            List of education entries
        """
        education = []
        university_keywords = [
            "university",
            "college",
            "institute",
            "school",
            "MBA",
            "bachelor",
            "master",
            "phd",
            "degree",
        ]

        for result in search_results:
            snippet = result.get("snippet", "")

            # Look for university names
            for keyword in university_keywords:
                if keyword.lower() in snippet.lower():
                    # Try to extract the institution name
                    lines = snippet.split(".")
                    for line in lines:
                        if keyword.lower() in line.lower():
                            education.append({"description": line.strip()})
                            break
                    break

        return education[:3]  # Return top 3

    def _extract_achievements(self, search_results: list) -> List[str]:
        """Extract achievements from search results.

        Args:
            search_results: List of search result dictionaries

        Returns:
            List of achievement strings
        """
        achievements = []
        achievement_keywords = ["award", "recognition", "winner", "honored", "recipient"]

        for result in search_results:
            snippet = result.get("snippet", "")
            if any(keyword in snippet.lower() for keyword in achievement_keywords):
                achievements.append(snippet)

        return achievements[:5]  # Return top 5

    def _extract_interests(self, search_results: list) -> List[str]:
        """Extract interests and hobbies from search results.

        Args:
            search_results: List of search result dictionaries

        Returns:
            List of interest strings
        """
        interests = []

        common_interests = [
            "technology",
            "AI",
            "machine learning",
            "entrepreneurship",
            "innovation",
            "leadership",
            "sports",
            "music",
            "travel",
            "photography",
            "reading",
            "writing",
            "speaking",
            "mentoring",
        ]

        for result in search_results:
            snippet = result.get("snippet", "").lower()
            for interest in common_interests:
                if interest.lower() in snippet and interest not in interests:
                    interests.append(interest)

        return interests[:5]  # Return top 5
