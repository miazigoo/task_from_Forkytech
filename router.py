from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import LimitOffsetPage, Page
from fastapi_pagination.ext.async_sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session
from tronpy import Tron

from database import engine, new_session
from models import Base, WalletRequest
from schemas import AddressInput, InfoOutput, WalletOutput
from fastapi_pagination.ext.sqlalchemy import paginate

router = APIRouter()

Base.metadata.create_all(bind=engine)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()
        print("Выключение DB")


async def get_wallet_info(tron: Tron, address: str) -> dict:
    bandwidth = tron.get_bandwidth(address)
    account = tron.get_account(address)
    return {
        'bandwidth': bandwidth,
        'balance': Decimal(account['balance']) / 1_000_000,
        'energy': Decimal(account['net_window_size']) / 1_000_000
    }


@router.post("/wallet_info", response_model=InfoOutput)
async def wallet_info(
        task_in: AddressInput, db: Session = Depends(get_db)
):
    """
    Делаем запись запроса в БД.
    Записываются id, адрес кошелька и дата запроса.
    Возвращаем информацию с кошелька:
    bandwidth, balance, energy
    """
    address = task_in.address
    tron = Tron(network='nile')
    if not Tron.is_address(address):
        raise HTTPException(status_code=400, detail="Не верный адрес кошелька")
    info = await get_wallet_info(tron, address)

    task = WalletRequest(address=address)
    db.add(task)
    db.commit()
    return InfoOutput(**info)


@router.get("/wallet_info/limit-offset", response_model=LimitOffsetPage[WalletOutput])
@router.get("/wallet_info/default", response_model=Page[WalletOutput])
async def list_requests(
        db: Session = Depends(get_db)
) -> Any:
    """
    Получение списка последних запросов к кошелькам с пагинацией.
    Представленны 2 варианта пагинации
    """
    query = select(WalletRequest).order_by(WalletRequest.created_at)
    return paginate(db, query)