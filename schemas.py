from pydantic import BaseModel


class AddressInput(BaseModel):
    address: str

class InfoOutput(BaseModel):
    bandwidth: int
    balance: float
    energy: float