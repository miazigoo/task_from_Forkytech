from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tronpy import Tron

from database import engine, new_session
from models import Base, WalletRequest
from schemas import AddressInput, InfoOutput

router = APIRouter()

Base.metadata.create_all(bind=engine)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()
        print("Выключение DB")


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
    if not Tron.is_address(address):
        raise HTTPException(status_code=400, detail="Не верный адрес кошелька")
    task = WalletRequest(address=address)
    db.add(task)
    db.commit()
    tron = Tron(network='nile')
    bandwidth = tron.get_bandwidth(address)
    account = tron.get_account(address)
    info = {
        'bandwidth': bandwidth,
        'balance': Decimal(account['balance']) / 1_000_000,
        'energy': Decimal(account['net_window_size']) / 1_000_000
    }
    return InfoOutput(**info)