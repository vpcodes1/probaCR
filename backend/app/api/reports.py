"""Reports API endpoints."""
import logging
from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

from app.core.generators import PDFGenerator, WordGenerator
from app.core.orchestrator import ResearchOrchestrator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reports", tags=["reports"])

# In-memory storage for demo (replace with database in production)
reports_db = {}


class ReportRequest(BaseModel):
    """Report generation request."""

    prospect_name: str
    company_name: str
    additional_context: str = ""


class ReportResponse(BaseModel):
    """Report generation response."""

    report_id: str
    status: str
    message: str


class ReportData(BaseModel):
    """Complete report data."""

    report_id: str
    status: str
    prospect_name: str
    company_name: str
    data: Dict[str, Any] = {}
    pdf_path: str = ""
    docx_path: str = ""
    error_message: str = ""


@router.post("/generate", response_model=ReportResponse)
async def generate_report(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
) -> ReportResponse:
    """Generate a new prospect report.

    Args:
        request: Report generation request
        background_tasks: FastAPI background tasks

    Returns:
        Report generation response with report ID
    """
    logger.info(
        f"Received report request for {request.prospect_name} at {request.company_name}"
    )

    # Generate unique report ID
    import uuid

    report_id = str(uuid.uuid4())

    # Initialize report in database
    reports_db[report_id] = {
        "report_id": report_id,
        "status": "processing",
        "prospect_name": request.prospect_name,
        "company_name": request.company_name,
        "data": {},
        "pdf_path": "",
        "docx_path": "",
        "error_message": "",
    }

    # Start report generation in background
    background_tasks.add_task(
        _generate_report_task,
        report_id,
        request.prospect_name,
        request.company_name,
        request.additional_context,
    )

    return ReportResponse(
        report_id=report_id,
        status="processing",
        message="Report generation started. Check status using report ID.",
    )


@router.get("/{report_id}", response_model=ReportData)
async def get_report(report_id: str) -> ReportData:
    """Get report by ID.

    Args:
        report_id: Report ID

    Returns:
        Report data

    Raises:
        HTTPException: If report not found
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")

    report = reports_db[report_id]
    return ReportData(**report)


@router.get("/{report_id}/status")
async def get_report_status(report_id: str) -> Dict[str, str]:
    """Get report generation status.

    Args:
        report_id: Report ID

    Returns:
        Status information

    Raises:
        HTTPException: If report not found
    """
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")

    report = reports_db[report_id]
    return {
        "report_id": report_id,
        "status": report["status"],
        "message": report.get("error_message", ""),
    }


async def _generate_report_task(
    report_id: str,
    prospect_name: str,
    company_name: str,
    additional_context: str,
):
    """Background task to generate report.

    Args:
        report_id: Report ID
        prospect_name: Prospect name
        company_name: Company name
        additional_context: Additional context
    """
    try:
        logger.info(f"Starting report generation for report_id: {report_id}")

        # Generate report
        orchestrator = ResearchOrchestrator()
        report_data = await orchestrator.generate_report(
            prospect_name=prospect_name,
            company_name=company_name,
            additional_context=additional_context,
        )

        # Generate PDF
        pdf_generator = PDFGenerator()
        pdf_path = pdf_generator.generate(report_data)

        # Generate Word document
        word_generator = WordGenerator()
        docx_path = word_generator.generate(report_data)

        # Update report in database
        reports_db[report_id].update(
            {
                "status": "completed",
                "data": report_data,
                "pdf_path": pdf_path,
                "docx_path": docx_path,
            }
        )

        logger.info(f"Report generation completed for report_id: {report_id}")

    except Exception as e:
        logger.error(f"Error generating report {report_id}: {e}", exc_info=True)
        reports_db[report_id].update(
            {
                "status": "failed",
                "error_message": str(e),
            }
        )
