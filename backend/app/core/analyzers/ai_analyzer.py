"""AI-powered analysis engine."""
import json
import logging
from typing import Any, Dict, List, Optional

from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Uses AI to analyze prospect data and generate insights."""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """Initialize AI analyzer.

        Args:
            api_key: Anthropic API key
            model: Model to use for analysis
        """
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model

    async def analyze_prospect(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        news_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze prospect data and generate comprehensive insights.

        Args:
            person_data: Personal information
            company_data: Company information
            news_data: Recent news and events

        Returns:
            Dictionary with AI-generated insights
        """
        logger.info("Starting AI analysis of prospect data")

        # Generate comprehensive analysis
        analysis = {
            "talking_points": await self._generate_talking_points(
                person_data, company_data, news_data
            ),
            "conversation_starters": await self._generate_conversation_starters(
                person_data, company_data, news_data
            ),
            "personality_analysis": await self._analyze_personality(person_data),
            "recommended_approach": await self._recommend_approach(
                person_data, company_data
            ),
            "key_insights": await self._extract_key_insights(
                person_data, company_data, news_data
            ),
        }

        logger.info("AI analysis completed")
        return analysis

    async def _generate_talking_points(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        news_data: Dict[str, Any],
    ) -> List[str]:
        """Generate perfect talking points for the meeting.

        Args:
            person_data: Personal information
            company_data: Company information
            news_data: Recent news

        Returns:
            List of talking points
        """
        prompt = f"""You are a sales intelligence expert. Based on the following information about a prospect and their company, generate 8-10 perfect talking points for a sales meeting.

PROSPECT INFORMATION:
{json.dumps(person_data, indent=2)}

COMPANY INFORMATION:
{json.dumps(company_data, indent=2)}

RECENT NEWS:
{json.dumps(news_data, indent=2)}

Generate talking points that:
1. Reference specific, recent developments
2. Show deep understanding of their business
3. Connect to potential pain points or opportunities
4. Are natural conversation topics, not sales pitches
5. Build credibility and trust

Return ONLY a JSON array of strings, nothing else. Example format:
["Talking point 1", "Talking point 2", ...]
"""

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text.strip()
            # Parse JSON response
            talking_points = json.loads(content)
            return talking_points

        except Exception as e:
            logger.error(f"Error generating talking points: {e}")
            return [
                "Discuss their recent company developments",
                "Ask about their role and responsibilities",
                "Explore their industry challenges",
            ]

    async def _generate_conversation_starters(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        news_data: Dict[str, Any],
    ) -> List[str]:
        """Generate 3-5 perfect conversation starters.

        Args:
            person_data: Personal information
            company_data: Company information
            news_data: Recent news

        Returns:
            List of conversation starters
        """
        prompt = f"""You are a sales intelligence expert. Based on the following information, generate 3-5 perfect conversation starters for the beginning of a sales meeting.

PROSPECT INFORMATION:
{json.dumps(person_data, indent=2)}

COMPANY INFORMATION:
{json.dumps(company_data, indent=2)}

RECENT NEWS:
{json.dumps(news_data, indent=2)}

Generate conversation starters that:
1. Are natural and authentic (not forced or salesy)
2. Reference specific, recent information
3. Show you've done your homework
4. Create immediate connection and rapport
5. Are open-ended to encourage dialogue

Return ONLY a JSON array of strings, nothing else. Example:
["I saw that [company] just announced [specific event]...", "Your background in [field] is impressive..."]
"""

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text.strip()
            starters = json.loads(content)
            return starters[:5]  # Max 5

        except Exception as e:
            logger.error(f"Error generating conversation starters: {e}")
            return [
                f"I noticed your recent work at {company_data.get('company_name', 'the company')}",
                "I'd love to hear about your current priorities",
                "What's been your biggest challenge lately?",
            ]

    async def _analyze_personality(self, person_data: Dict[str, Any]) -> str:
        """Analyze personality and communication style.

        Args:
            person_data: Personal information

        Returns:
            Personality analysis text
        """
        prompt = f"""You are an expert in personality analysis for sales professionals. Based on the following information about a prospect, provide a brief personality analysis that will help in sales conversations.

PROSPECT INFORMATION:
{json.dumps(person_data, indent=2)}

Analyze:
1. Likely communication style (direct vs. relational, formal vs. casual)
2. Professional priorities and values
3. Decision-making style
4. Best approach for building rapport

Provide a concise 3-4 paragraph analysis that's actionable for a sales professional. Be specific but not stereotypical.
"""

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Error analyzing personality: {e}")
            return "Based on available information, approach this prospect professionally and focus on their business challenges."

    async def _recommend_approach(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
    ) -> str:
        """Recommend the best approach for this prospect.

        Args:
            person_data: Personal information
            company_data: Company information

        Returns:
            Recommended approach text
        """
        prompt = f"""You are a sales strategy expert. Based on this prospect and company information, recommend the best approach for the sales conversation.

PROSPECT:
{json.dumps(person_data, indent=2)}

COMPANY:
{json.dumps(company_data, indent=2)}

Provide specific recommendations on:
1. Meeting tone and style
2. Key value propositions to emphasize
3. Questions to ask
4. Things to avoid
5. Next steps strategy

Provide 3-4 paragraphs of actionable advice.
"""

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1200,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text.strip()

        except Exception as e:
            logger.error(f"Error recommending approach: {e}")
            return "Focus on understanding their needs first, then position your solution as a way to address their specific challenges."

    async def _extract_key_insights(
        self,
        person_data: Dict[str, Any],
        company_data: Dict[str, Any],
        news_data: Dict[str, Any],
    ) -> List[str]:
        """Extract 5-7 key insights from all data.

        Args:
            person_data: Personal information
            company_data: Company information
            news_data: Recent news

        Returns:
            List of key insights
        """
        prompt = f"""Extract 5-7 key insights from this prospect research that a sales professional should know before a meeting.

PROSPECT:
{json.dumps(person_data, indent=2)}

COMPANY:
{json.dumps(company_data, indent=2)}

NEWS:
{json.dumps(news_data, indent=2)}

Focus on:
- Recent changes or developments
- Potential pain points or opportunities
- Personal or professional interests
- Company priorities
- Timing considerations

Return ONLY a JSON array of strings with concise, actionable insights.
"""

        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )

            content = response.content[0].text.strip()
            insights = json.loads(content)
            return insights

        except Exception as e:
            logger.error(f"Error extracting key insights: {e}")
            return [
                "Review available information before the meeting",
                "Focus on their current business priorities",
            ]
