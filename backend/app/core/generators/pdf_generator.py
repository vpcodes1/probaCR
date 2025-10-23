"""PDF report generator."""
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)


class PDFGenerator:
    """Generates PDF reports from prospect data."""

    def __init__(self, output_dir: str = "./reports"):
        """Initialize PDF generator.

        Args:
            output_dir: Directory to save PDF files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Set up custom paragraph styles."""
        # Title style
        self.title_style = ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Heading1"],
            fontSize=24,
            textColor=colors.HexColor("#1a1a1a"),
            spaceAfter=30,
            alignment=1,  # Center
        )

        # Heading style
        self.heading_style = ParagraphStyle(
            "CustomHeading",
            parent=self.styles["Heading2"],
            fontSize=16,
            textColor=colors.HexColor("#2563eb"),
            spaceAfter=12,
            spaceBefore=12,
        )

        # Body style
        self.body_style = ParagraphStyle(
            "CustomBody",
            parent=self.styles["Normal"],
            fontSize=11,
            leading=16,
            spaceAfter=10,
        )

    def generate(self, report_data: Dict[str, Any]) -> str:
        """Generate PDF report.

        Args:
            report_data: Complete report data dictionary

        Returns:
            Path to generated PDF file
        """
        logger.info("Generating PDF report")

        # Create filename
        prospect_name = report_data.get("prospect_name", "prospect").replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{prospect_name}_report_{timestamp}.pdf"
        filepath = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Build content
        story = []

        # Title page
        story.extend(self._create_title_page(report_data))
        story.append(PageBreak())

        # Executive summary
        story.extend(self._create_executive_summary(report_data))

        # Quick facts
        story.extend(self._create_quick_facts(report_data))

        # Talking points
        story.extend(self._create_talking_points(report_data))

        # Conversation starters
        story.extend(self._create_conversation_starters(report_data))

        # Personality analysis
        story.extend(self._create_personality_analysis(report_data))

        # Recommended approach
        story.extend(self._create_recommended_approach(report_data))

        # Company information
        story.extend(self._create_company_info(report_data))

        # News and recent events
        story.extend(self._create_news_section(report_data))

        # Build PDF
        doc.build(story)

        logger.info(f"PDF report generated: {filepath}")
        return str(filepath)

    def _create_title_page(self, report_data: Dict[str, Any]) -> list:
        """Create title page."""
        elements = []

        elements.append(Spacer(1, 2 * inch))

        # Title
        title = Paragraph("PROSPECT INTELLIGENCE REPORT", self.title_style)
        elements.append(title)

        elements.append(Spacer(1, 0.5 * inch))

        # Prospect info
        prospect_name = report_data.get("prospect_name", "Unknown")
        company_name = report_data.get("company_name", "Unknown")

        info_text = f"<b>{prospect_name}</b><br/>{company_name}"
        info = Paragraph(info_text, self.body_style)
        elements.append(info)

        elements.append(Spacer(1, 0.5 * inch))

        # Date
        date_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
        date = Paragraph(date_text, self.body_style)
        elements.append(date)

        elements.append(Spacer(1, 0.3 * inch))

        # Branding
        branding = Paragraph(
            "Powered by <b>YUSEARCH</b> - AI-Powered Prospect Research",
            self.body_style,
        )
        elements.append(branding)

        return elements

    def _create_executive_summary(self, report_data: Dict[str, Any]) -> list:
        """Create executive summary section."""
        elements = []

        elements.append(Paragraph("Executive Summary", self.heading_style))

        summary = report_data.get("executive_summary", "No summary available")
        elements.append(Paragraph(summary, self.body_style))

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_quick_facts(self, report_data: Dict[str, Any]) -> list:
        """Create quick facts section."""
        elements = []

        elements.append(Paragraph("Quick Facts", self.heading_style))

        facts = report_data.get("quick_facts", {})

        if facts:
            data = [[k, v] for k, v in facts.items()]
            table = Table(data, colWidths=[2 * inch, 4 * inch])
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f3f4f6")),
                        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 8),
                        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                    ]
                )
            )
            elements.append(table)
        else:
            elements.append(Paragraph("No quick facts available", self.body_style))

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_talking_points(self, report_data: Dict[str, Any]) -> list:
        """Create talking points section."""
        elements = []

        elements.append(Paragraph("Perfect Talking Points", self.heading_style))

        talking_points = report_data.get("talking_points", [])

        if talking_points:
            for i, point in enumerate(talking_points, 1):
                text = f"{i}. {point}"
                elements.append(Paragraph(text, self.body_style))
        else:
            elements.append(Paragraph("No talking points available", self.body_style))

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_conversation_starters(self, report_data: Dict[str, Any]) -> list:
        """Create conversation starters section."""
        elements = []

        elements.append(Paragraph("Conversation Starters", self.heading_style))

        starters = report_data.get("conversation_starters", [])

        if starters:
            for starter in starters:
                text = f"• {starter}"
                elements.append(Paragraph(text, self.body_style))
        else:
            elements.append(
                Paragraph("No conversation starters available", self.body_style)
            )

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_personality_analysis(self, report_data: Dict[str, Any]) -> list:
        """Create personality analysis section."""
        elements = []

        elements.append(Paragraph("Personality Insights", self.heading_style))

        analysis = report_data.get("personality_analysis", "No analysis available")

        # Split into paragraphs
        for para in analysis.split("\n\n"):
            if para.strip():
                elements.append(Paragraph(para.strip(), self.body_style))

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_recommended_approach(self, report_data: Dict[str, Any]) -> list:
        """Create recommended approach section."""
        elements = []

        elements.append(Paragraph("Recommended Approach", self.heading_style))

        approach = report_data.get("recommended_approach", "No recommendations available")

        for para in approach.split("\n\n"):
            if para.strip():
                elements.append(Paragraph(para.strip(), self.body_style))

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_company_info(self, report_data: Dict[str, Any]) -> list:
        """Create company information section."""
        elements = []

        elements.append(Paragraph("Company Background", self.heading_style))

        company_data = report_data.get("company_data", {})

        if company_data.get("description"):
            elements.append(Paragraph(company_data["description"], self.body_style))

        if company_data.get("funding"):
            elements.append(
                Paragraph(f"<b>Funding:</b> {company_data['funding']}", self.body_style)
            )

        elements.append(Spacer(1, 0.3 * inch))

        return elements

    def _create_news_section(self, report_data: Dict[str, Any]) -> list:
        """Create recent news section."""
        elements = []

        elements.append(Paragraph("Recent News & Events", self.heading_style))

        news_data = report_data.get("news_data", {})
        company_news = news_data.get("company_news", [])

        if company_news:
            for news in company_news[:5]:  # Top 5 news items
                title = news.get("title", "")
                snippet = news.get("snippet", "")
                text = f"<b>{title}</b><br/>{snippet}"
                elements.append(Paragraph(text, self.body_style))
                elements.append(Spacer(1, 0.1 * inch))
        else:
            elements.append(Paragraph("No recent news available", self.body_style))

        return elements
