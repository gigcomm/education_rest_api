from fastapi import Depends, APIRouter
from fastapi import Response
from starlette import status

from api.dependencies import get_category_services
from schemas.category import CategorySchema, CategoryCreate
from services.category import CategoryService

category_router = APIRouter(prefix="/categories", tags=["categories"])

@category_router.get("")
def get_categories(category_service: CategoryService = Depends(get_category_services)) -> list[CategorySchema]:
    return category_service.get_all_categories()



@category_router.post("", status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, category_service: CategoryService = Depends(get_category_services)) -> CategorySchema:
    return category_service.create_category(data)



@category_router.patch("/{category_id}")
def update_category(
    category_id: str, data: CategoryCreate, category_service: CategoryService = Depends(get_category_services)) -> CategorySchema:
    return category_service.update_category(category_id, data)


@category_router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_category(category_id: str, category_service: CategoryService = Depends(get_category_services)):
    category_service.delete_category(category_id)