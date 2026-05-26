from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_payload, require_admin
from app.db.database import get_db
from app.schemas.request import RequestCreate, RequestRead, RequestUpdate
from app.services.request_service import (
    create_request_service,
    get_all_requests_service,
    get_my_requests_service,
    get_request_by_id_service,
    update_request_service,
    delete_request_service,
)


router = APIRouter(
    prefix="/requests",
    tags=["requests"],
)


@router.post("/", response_model=RequestRead)
async def create_request(
    request_data: RequestCreate,
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await create_request_service(
        db=db,
        request_data=request_data,
        author_id=int(payload["sub"]),
    )


@router.get("/my", response_model=list[RequestRead])
async def get_my_requests(
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await get_my_requests_service(
        db=db,
        author_id=int(payload["sub"]),
    )


@router.get("/", response_model=list[RequestRead])
async def get_all_requests(
    db: AsyncSession = Depends(get_db),
    admin_payload: dict = Depends(require_admin),
):
    return await get_all_requests_service(db=db)


@router.get("/{request_id}", response_model=RequestRead)
async def get_request_by_id(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await get_request_by_id_service(
        db=db,
        request_id=request_id,
        payload=payload,
    )


@router.patch("/{request_id}", response_model=RequestRead)
async def update_request(
    request_id: int,
    request_data: RequestUpdate,
    db: AsyncSession = Depends(get_db),
    admin_payload: dict = Depends(require_admin),
):
    return await update_request_service(
        db=db,
        request_id=request_id,
        request_data=request_data,
    )


@router.delete("/{request_id}")
async def delete_request(
    request_id: int,
    db: AsyncSession = Depends(get_db),
    admin_payload: dict = Depends(require_admin),
):
    return await delete_request_service(
        db=db,
        request_id=request_id,
    )
