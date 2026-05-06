from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.models import Specification
from app.services.export_service import generate_docx, generate_pdf, generate_trello_json
from urllib.parse import quote
import uuid

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/{spec_id}/docx")
async def export_docx(
    spec_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    docx_data = generate_docx(spec.content, spec.title)
    
    safe_name = spec.title.replace(" ", "_").replace(":", "_").replace("/", "_")[:50]
    encoded_name = quote(safe_name)
    
    return StreamingResponse(
        iter([docx_data]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename=\"{safe_name}.docx\"; filename*=UTF-8''{encoded_name}.docx"
        }
    )


@router.get("/{spec_id}/pdf")
async def export_pdf(
    spec_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    pdf_data = generate_pdf(spec.content, spec.title)
    
    safe_name = spec.title.replace(" ", "_").replace(":", "_").replace("/", "_")[:50]
    encoded_name = quote(safe_name)
    
    return StreamingResponse(
        iter([pdf_data]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=\"{safe_name}.pdf\"; filename*=UTF-8''{encoded_name}.pdf"
        }
    )


@router.get("/{spec_id}/trello")
async def export_trello(
    spec_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    trello_data = generate_trello_json(spec.content, spec.title)
    return trello_data