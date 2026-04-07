from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db.database import get_db
from app.models.models import Specification, SharedLink, Template
from app.schemas.schemas import GenerateRequest, SpecificationCreate, SpecificationUpdate, SpecificationResponse, SharedLinkResponse
from app.services.generator_service import generate_specification, init_templates
from app.services.auth_service import decode_token
from typing import List
import uuid
import secrets

router = APIRouter(prefix="/specifications", tags=["specifications"])


def get_current_user(request: Request) -> dict | None:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    return decode_token(token)


@router.post("/generate", response_model=SpecificationResponse, status_code=status.HTTP_201_CREATED)
async def generate_spec(
    request_data: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    await init_templates(db)
    
    result = await db.execute(select(Template).where(
        Template.type == request_data.type,
        Template.complexity == request_data.complexity
    ))
    template = result.scalar_one_or_none()
    
    if not template:
        spec_data = generate_specification(request_data.type, request_data.complexity)
        spec_data["type"] = request_data.type
        spec_data["complexity"] = request_data.complexity
    else:
        spec_data = dict(template.structure)
        spec_data["type"] = template.type
        spec_data["complexity"] = template.complexity
    
    title = f"ТЗ: {request_data.type} (сложность {request_data.complexity})"
    
    user_uuid = uuid.UUID(current_user["sub"]) if current_user else None
    
    spec = Specification(
        user_id=user_uuid,
        template_id=template.id if template else None,
        title=title,
        content=spec_data,
        type=request_data.type,
        complexity=request_data.complexity
    )
    
    db.add(spec)
    await db.commit()
    await db.refresh(spec)
    
    return spec


@router.get("", response_model=List[SpecificationResponse])
async def list_specifications(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    user_uuid = uuid.UUID(current_user["sub"])
    result = await db.execute(
        select(Specification)
        .where(Specification.user_id == user_uuid)
        .order_by(desc(Specification.created_at))
    )
    
    return result.scalars().all()


@router.get("/{spec_id}", response_model=SpecificationResponse)
async def get_specification(
    spec_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    if spec.user_id and current_user:
        if str(spec.user_id) != current_user["sub"]:
            raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    return spec


@router.put("/{spec_id}", response_model=SpecificationResponse)
async def update_specification(
    spec_id: uuid.UUID,
    update_data: SpecificationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    if str(spec.user_id) != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    if update_data.title:
        spec.title = update_data.title
    if update_data.content:
        spec.content = {**spec.content, **update_data.content}
    
    await db.commit()
    await db.refresh(spec)
    
    return spec


@router.delete("/{spec_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specification(
    spec_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    if str(spec.user_id) != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    await db.delete(spec)
    await db.commit()


@router.post("/{spec_id}/share", response_model=SharedLinkResponse)
async def create_share_link(
    spec_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Требуется авторизация"
        )
    
    result = await db.execute(select(Specification).where(Specification.id == spec_id))
    spec = result.scalar_one_or_none()
    
    if not spec:
        raise HTTPException(status_code=404, detail="ТЗ не найдено")
    
    if str(spec.user_id) != current_user["sub"]:
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    
    result = await db.execute(select(SharedLink).where(SharedLink.spec_id == spec_id))
    existing_link = result.scalar_one_or_none()
    
    if existing_link:
        return SharedLinkResponse(
            token=existing_link.token,
            url=f"/shared/{existing_link.token}"
        )
    
    token = secrets.token_urlsafe(32)
    share_link = SharedLink(token=token, spec_id=spec_id)
    db.add(share_link)
    await db.commit()
    
    return SharedLinkResponse(token=token, url=f"/shared/{token}")