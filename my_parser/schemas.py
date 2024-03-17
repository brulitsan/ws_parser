from pydantic import BaseModel
from pydantic.v1 import BaseSettings


class CoinData(BaseModel):
    name: str
    price: float


class DbSettings(BaseSettings):
    mongo_url: str
    db_name: str
    collection_name: str

    class Config:
        env_file = ".env"


class ParserSettings(BaseSettings):
    parser_url: str

    class Config:
        env_file = ".env"
