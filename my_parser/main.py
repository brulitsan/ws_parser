import fastapi
from my_parser.api import router as api_router

app = fastapi.FastAPI()

app.include_router(api_router, prefix="/api")