from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.models import Specification
from app.services.export_service import (
    generate_docx,
    generate_pdf,
    generate_trello_json,
)

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/{spec_id}/docx")
async def export_docx(spec_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()

    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")

    content = dict(spec.content) if spec.content else {}
    title = str(spec.title) if spec.title else "ТЗ"
    docx_data = generate_docx(content, title)

    return StreamingResponse(
        iter([docx_data]),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename={title}.docx"},
    )


@router.get("/{spec_id}/pdf")
async def export_pdf(spec_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()

    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")

    content = dict(spec.content) if spec.content else {}
    title = str(spec.title) if spec.title else "ТЗ"
    pdf_data = generate_pdf(content, title)

    return StreamingResponse(
        iter([pdf_data]),
        media_type="text/html",
        headers={"Content-Disposition": f"attachment; filename={title}.html"},
    )


@router.get("/{spec_id}/trello")
async def export_trello(spec_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()

    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")

    content = dict(spec.content) if spec.content else {}
    title = str(spec.title) if spec.title else "ТЗ"
    trello_data = generate_trello_json(content, title)
    return trello_data
