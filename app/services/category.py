from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategorySchema


class CategoryNotFound(Exception):
    pass


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def get_all_categories(self) -> list[CategorySchema]:
        categories = self.category_repository.get_all_categories()
        return [CategorySchema.model_validate(cat) for cat in categories]

    def create_category(self, payload: CategoryCreate) -> CategorySchema:
        category = self.category_repository.create_category(name=payload.name)
        self.db.commit()
        return CategorySchema.model_validate(category)

    def update_category(
        self, category_id: str, payload: CategoryCreate
    ) -> CategorySchema:
        category = self.category_repository.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFound("Категория не найдена")
        category.name = payload.name
        self.db.commit()
        return CategorySchema.model_validate(category)

    def delete_category(self, category_id: str) -> None:
        category = self.category_repository.get_category_by_id(category_id)
        if category is None:
            raise CategoryNotFound("Категория не найдена")
        self.category_repository.delete_category(category)
        self.db.commit()
