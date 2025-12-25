import uuid

from fastapi.testclient import TestClient

from app.app import app

client = TestClient(app)


def test_good_connection():
    """Тест подключения к API.
    Проверяет, что endpoint /recipes доступен и возвращает статус 200.
    """
    response = client.get("/recipes")
    assert response.status_code == 200


def test_error404_connection():
    """Тест обработки несуществующего пути.
    Приложение должно вернуть 404 для неизвестных маршрутов.
    """
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_get_all_recipes():
    """Тест получения списка всех рецептов.
    Проверяет: статус 200 и ответ - список рецептов"""
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_recipe_by_id():
    """Тест получения рецепта по ID с созданием тестового рецепта.
    1. Создает новый рецепт через POST /recipes/
    2. Получает созданный рецепт по recipe_id через GET /recipes/{id}
    3. Проверяет статус 200 и совпадение названия блюда
    """
    unique_name = f"Test Recipe {uuid.uuid4()}"
    new_recipe = {
        "dish_name": unique_name,
        "cooking_time_minutes": 20,
        "ingredients": "Test ingredients",
        "description": "Test description",
    }
    post_resp = client.post("/recipes/", json=new_recipe)
    assert post_resp.status_code == 200
    recipe_id = post_resp.json()["recipe_id"]

    get_resp = client.get(f"/recipes/{recipe_id}")
    assert get_resp.status_code == 200
    recipe_data = get_resp.json()
    assert recipe_data["dish_name"] == unique_name


def test_get_recipe_by_id_not_found():
    """Тест обработки несуществующего recipe_id.
    Проверяет, что endpoint возвращает 404 при запросе несуществующего ID.
    """
    response = client.get("/recipes/666")
    assert response.status_code == 404


def test_create_recipe():
    """Тест создания нового рецепта.
    - POST /recipes/ принимает валидные данные
    - Возвращает статус 200
    - Созданный рецепт содержит правильное название блюда
    """
    unique_name = f"CreateTest {uuid.uuid4()}"
    new_recipe = {
        "dish_name": unique_name,
        "cooking_time_minutes": 45,
        "ingredients": "Ingredients",
        "description": "Description",
    }
    response = client.post("/recipes/", json=new_recipe)
    assert response.status_code == 200
    data = response.json()
    assert data["dish_name"] == unique_name
