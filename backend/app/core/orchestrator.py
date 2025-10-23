"""Research orchestrator - coordinates all data collection and analysis."""
import asyncio
import logging
import time
from typing import Any, Dict

from app.config import get_settings
from app.core.analyzers import AIAnalyzer
from app.core.collectors import CompanyCollector, NewsCollector, PersonCollector

logger = logging.getLogger(__name__)


class ResearchOrchestrator:
    """Orchestrates the entire research and analysis process."""

    def __init__(self):
        """Initialize orchestrator."""
        self.settings = get_settings()

    async def generate_report(
        self,
        prospect_name: str,
        company_name: str,
        additional_context: str = "",
    ) -> Dict[str, Any]:
        """Generate complete prospect report.

        This is the main entry point that coordinates all research and analysis.

        Args:
            prospect_name: Name of the prospect
            company_name: Company they work for
            additional_context: Any additional context provided by user

        Returns:
            Complete report data dictionary
        """
        start_time = time.time()
        logger.info(
            f"Starting report generation for {prospect_name} at {company_name}"
        )

        try:
            # Step 1: Collect data in parallel
            logger.info("Step 1/3: Collecting data from multiple sources...")
            person_data, company_data, news_data = await self._collect_all_data(
                prospect_name, company_name
            )

            # Step 2: AI Analysis
            logger.info("Step 2/3: Analyzing data with AI...")
            ai_insights = await self._analyze_data(person_data, company_data, news_data)

            # Step 3: Compile report
            logger.info("Step 3/3: Compiling final report...")
            report = self._compile_report(
                prospect_name=prospect_name,
                company_name=company_name,
                additional_context=additional_context,
                person_data=person_data,
                company_data=company_data,
                news_data=news_data,
                ai_insights=ai_insights,
            )

            generation_time = int(time.time() - start_time)
            report["generation_time_seconds"] = generation_time

            logger.info(
                f"Report generation completed in {generation_time} seconds"
            )
            return report

        except Exception as e:
            logger.error(f"Error generating report: {e}", exc_info=True)
            raise

    async def _collect_all_data(
        self, prospect_name: str, company_name: str
    ) -> tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        """Collect all data in parallel.

        Args:
            prospect_name: Name of the prospect
            company_name: Company name

        Returns:
            Tuple of (person_data, company_data, news_data)
        """
        # Create collectors as context managers
        async with PersonCollector() as person_collector, \
                   CompanyCollector() as company_collector, \
                   NewsCollector() as news_collector:

            # Run all collectors in parallel
            results = await asyncio.gather(
                person_collector.collect(
                    person_name=prospect_name, company_name=company_name
                ),
                company_collector.collect(company_name=company_name),
                news_collector.collect(
                    company_name=company_name, person_name=prospect_name
                ),
                return_exceptions=True,
            )

            # Handle any exceptions
            person_data = results[0] if not isinstance(results[0], Exception) else {}
            company_data = results[1] if not isinstance(results[1], Exception) else {}
            news_data = results[2] if not isinstance(results[2], Exception) else {}

            return person_data, company_data, news_data

    async def _analyze_data(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        news_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze collected data with AI.

        Args:
            person_data: Personal information
            company_data: Company information
            news_data: Recent news

        Returns:
            AI-generated insights
        """
        if not self.settings.anthropic_api_key:
            logger.warning("Anthropic API key not configured, skipping AI analysis")
            return {
                "talking_points": ["No AI analysis available"],
                "conversation_starters": ["No AI analysis available"],
                "personality_analysis": "AI analysis not configured",
                "recommended_approach": "AI analysis not configured",
                "key_insights": [],
            }

        analyzer = AIAnalyzer(
            api_key=self.settings.anthropic_api_key,
            model=self.settings.default_ai_model,
        )

        return await analyzer.analyze_prospect(person_data, company_data, news_data)

    def _compile_report(
        self,
        prospect_name: str,
        company_name: str,
        additional_context: str,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        news_data: Dict[str, Any],
        ai_insights: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Compile final report from all collected and analyzed data.

        Args:
            prospect_name: Prospect name
            company_name: Company name
            additional_context: Additional context
            person_data: Personal data
            company_data: Company data
            news_data: News data
            ai_insights: AI-generated insights

        Returns:
            Complete report dictionary
        """
        report = {
            # Input data
            "prospect_name": prospect_name,
            "company_name": company_name,
            "additional_context": additional_context,
            # Collected data
            "person_data": person_data,
            "company_data": company_data,
            "news_data": news_data,
            # AI insights
            "ai_insights": ai_insights,
            "talking_points": ai_insights.get("talking_points", []),
            "conversation_starters": ai_insights.get("conversation_starters", []),
            "personality_analysis": ai_insights.get("personality_analysis", ""),
            "recommended_approach": ai_insights.get("recommended_approach", ""),
            "key_insights": ai_insights.get("key_insights", []),
            # Summary sections
            "executive_summary": self._generate_executive_summary(
                person_data, company_data, ai_insights
            ),
            "quick_facts": self._generate_quick_facts(person_data, company_data),
        }

        return report

    def _generate_executive_summary(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        ai_insights: Dict[str, Any],
    ) -> str:
        """Generate executive summary.

        Args:
            person_data: Personal data
            company_data: Company data
            ai_insights: AI insights

        Returns:
            Executive summary text
        """
        summary_parts = []

        # Person summary
        name = person_data.get("name", "Prospect")
        title = person_data.get("title", "Unknown title")
        company = company_data.get("company_name", "the company")

        summary_parts.append(
            f"{name} is {title} at {company}."
        )

        # Company summary
        if company_data.get("description"):
            summary_parts.append(company_data["description"])

        # Key insight
        key_insights = ai_insights.get("key_insights", [])
        if key_insights:
            summary_parts.append(f"Key insight: {key_insights[0]}")

        return " ".join(summary_parts)

    def _generate_quick_facts(
        self, person_data: Dict[str, Any], company_data: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate quick facts section.

        Args:
            person_data: Personal data
            company_data: Company data

        Returns:
            Dictionary of quick facts
        """
        facts = {}

        # Person facts
        if person_data.get("title"):
            facts["Title"] = person_data["title"]

        if person_data.get("location"):
            facts["Location"] = person_data["location"]

        if person_data.get("linkedin_url"):
            facts["LinkedIn"] = person_data["linkedin_url"]

        # Company facts
        if company_data.get("industry"):
            facts["Industry"] = company_data["industry"]

        if company_data.get("size"):
            facts["Company Size"] = company_data["size"]

        if company_data.get("website"):
            facts["Website"] = company_data["website"]

        return facts
