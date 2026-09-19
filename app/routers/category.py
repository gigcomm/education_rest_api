from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException

from app.api.dependencies import get_category_services
from app.schemas.category import CategoryCreate, CategorySchema
from app.services.category import CategoryNotFound, CategoryService

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.get("")
def get_categories(
    category_service: CategoryService = Depends(get_category_services),
) -> list[CategorySchema]:
    return category_service.get_all_categories()


@category_router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_services),
) -> CategorySchema:
    return category_service.create_category(data)


@category_router.patch("/{category_id}")
def update_category(
    category_id: str,
    data: CategoryCreate,
    category_service: CategoryService = Depends(get_category_services),
) -> CategorySchema:
    try:
        return category_service.update_category(category_id, data)
    except CategoryNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc


@category_router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_services),
) -> None:
    try:
        category_service.delete_category(category_id)
    except CategoryNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
