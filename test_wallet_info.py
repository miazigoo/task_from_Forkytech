import pytest
from starlette.testclient import TestClient
from app import app
from models import WalletRequest
from database import new_session


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def clean_database():
    # Очистка базы данных перед каждым тестом
    session = new_session()
    session.query(WalletRequest).delete()
    session.commit()
    session.close()


@pytest.mark.usefixtures("clean_database")
def test_wallet_info_endpoint(test_client):
    # Подготовка входных данных
    data = {"address": "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"}

    # Отправляем POST-запрос на эндпоинт
    response = test_client.post("http://127.0.0.1:8000/wallet_info", json=data)

    # Проверяем статус-код ответа
    assert response.status_code == 200

    # Проверяем структуру возвращаемого JSON
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert set(response_data.keys()) == {'bandwidth', 'balance', 'energy'}