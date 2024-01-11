import fastapi

from my_parser.api.handlers import get_coins

router = fastapi.APIRouter()

router.add_api_route(path='/coins', methods=["GET"], endpoint=get_coins)