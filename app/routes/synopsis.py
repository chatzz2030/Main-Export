"""API routes for synopsis export and download."""
import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from app.schemas import SynopsisInput
from app.db import _fetch_synopsis
from app.exporters.pdf_exporter import _render_pdf
from app.exporters.docx_exporter import _render_docx
from app.utils import _cleanup_file

router = APIRouter()

@router.get("/api/v1/synopsis/{synopsis_id}/download")
async def download_synopsis(synopsis_id: str, format: str, background_tasks: BackgroundTasks):
    if format not in ("pdf", "docx"):
        raise HTTPException(status_code=400, detail="format must be 'pdf' or 'docx'.")

    data = await _fetch_synopsis(synopsis_id)

    if format == "pdf":
        file_path = _render_pdf(data)
        media_type = "application/pdf"
    else:
        file_path = _render_docx(data)
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    background_tasks.add_task(_cleanup_file, file_path)
    return FileResponse(
        file_path,
        media_type=media_type,
        filename=os.path.basename(file_path),
        background=background_tasks,
    )

@router.post("/api/export/pdf")
def export_pdf(data: SynopsisInput, background_tasks: BackgroundTasks):
    file_path = _render_pdf(data)
    background_tasks.add_task(_cleanup_file, file_path)
    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=os.path.basename(file_path),
        background=background_tasks,
    )

@router.post("/api/export/docx")
def export_docx(data: SynopsisInput, background_tasks: BackgroundTasks):
    file_path = _render_docx(data)
    background_tasks.add_task(_cleanup_file, file_path)
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=os.path.basename(file_path),
        background=background_tasks,
    )
