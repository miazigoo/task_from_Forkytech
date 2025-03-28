import pytest
from database import new_session
from models import WalletRequest


@pytest.fixture(scope="module")
def clean_database():
    # Очистка базы данных перед каждым тестом
    session = new_session()
    session.query(WalletRequest).delete()
    session.commit()
    session.close()


@pytest.mark.usefixtures("clean_database")
def test_save_request_to_db(clean_database):
    # Создаем фиктивные данные
    address = "TMw2jT3Zx2r9QghD4i6NqVMH8dKCPNQ7JD"

    # Открываем сессию базы данных
    session = new_session()

    # Создаем объект запроса
    request = WalletRequest(address=address)

    # Добавляем объект в сессию и сохраняем изменения
    session.add(request)
    session.commit()

    # Проверяем, что запись добавлена в базу данных
    saved_requests = session.query(WalletRequest).all()
    assert len(saved_requests) == 1
    saved_request = saved_requests[0]
    assert saved_request.address == address

    # Закрываем сессию
    session.close()