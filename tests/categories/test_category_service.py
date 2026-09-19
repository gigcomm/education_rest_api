from unittest.mock import Mock

import pytest

from app.models.category import CategoryORM
from app.schemas.category import CategoryCreate, CategorySchema
from app.services.category import CategoryService


def test_list_categories_pydantic_model(
    category_service: CategoryService, category_repository_mock: Mock
) -> None:
    # Имитируем, что метод get_all_categories репозитория вернет эти категории
    category_repository_mock.get_all_categories.return_value = [
        CategoryORM(id="category-1", name="Категория 1"),
        CategoryORM(id="category-2", name="Категория 2"),
    ]

    result = category_service.get_all_categories()

    assert result == [
        CategorySchema(id="category-1", name="Категория 1"),
        CategorySchema(id="category-2", name="Категория 2"),
    ]


def test_create_category_commits_created_category(
    category_service: CategoryService, db_mock: Mock, category_repository_mock: Mock
) -> None:
    created_category = CategoryORM(id="category-1", name="Новая категория")
    category_repository_mock.create_category.return_value = created_category

    result = category_service.create_category(CategoryCreate(name="Новая категория"))

    category_repository_mock.create_category.assert_called_once_with(
        name="Новая категория"
    )
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новая категория",
    }


@pytest.mark.parametrize(
    ("payload", "expected_title"),
    [
        pytest.param(
            CategoryCreate(name="Обновить название"),  # payload
            "Обновить название",  # expected_title
        ),
        pytest.param(
            CategoryCreate(name="Старая категория"),  # payload
            "Старая категория",  # expected_title
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    payload: CategoryCreate,
    expected_title: str,
) -> None:
    existing_category = CategoryORM(id="category-1", name="Старая категория")
    category_repository_mock.get_category_by_id.return_value = existing_category

    result = category_service.update_category("category-1", payload)

    assert result.name == expected_title
    db_mock.commit.assert_called_once_with()
