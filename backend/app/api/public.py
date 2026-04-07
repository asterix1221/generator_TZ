from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.models import Specification, SharedLink
from app.schemas.schemas import SpecificationResponse

router = APIRouter(tags=["public"])


@router.get("/shared/{token}", response_model=SpecificationResponse)
async def get_shared_specification(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(SharedLink).where(SharedLink.token == token))
    shared_link = result.scalar_one_or_none()
    
    if not shared_link:
        raise HTTPException(status_code=404, detail="Ссылка недействительна")
    
    result = await db.execute(select(Specification).where(Specification.id == shared_link.spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    return spec