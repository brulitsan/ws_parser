from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class CoinData(BaseModel):
    name: str
    price: float


class Settings(BaseSettings):
    mongo_url: str
    db_name: str
    collection_name: str

    class Config:
        env_file = ".env"