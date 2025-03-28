from pydantic import BaseModel


class AddressInput(BaseModel):
    address: str