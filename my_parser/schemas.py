from pydantic import BaseModel


class CoinData(BaseModel):
    name: str
    price: float