"""PDF rendering export functionality."""
import os
import uuid
from datetime import datetime
from fastapi import HTTPException
from weasyprint import HTML

from app.schemas import SynopsisInput
from app.config import OUTPUT_DIR
from app.utils import _slugify
from app.templates.pdf_template import _pdf_template

def _render_pdf(data: SynopsisInput) -> str:
    html_content = _pdf_template.render(
        meta=data.video_metadata,
        summary=data.summary,
        generated_on=datetime.utcnow().strftime("%d %b %Y, %H:%M UTC"),
    )
    file_name = f"{_slugify(data.video_metadata.title)}-{uuid.uuid4().hex[:8]}.pdf"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    try:
        HTML(string=html_content).write_pdf(file_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {exc}")
    return file_path
