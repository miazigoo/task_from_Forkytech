from fastapi import APIRouter

from database import engine, new_session
from models import Base


router = APIRouter()

Base.metadata.create_all(bind=engine)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()
        print("Выключение DB")
