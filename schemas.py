from datetime import datetime

from pydantic import BaseModel


class AddressInput(BaseModel):
    address: str

class InfoOutput(BaseModel):
    bandwidth: int
    balance: float
    energy: float

class WalletOutput(BaseModel):
    id: int
    address: str
    created_at: datetime