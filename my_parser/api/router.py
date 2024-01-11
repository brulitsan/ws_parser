import fastapi

from my_parser.api.handlers import get_coins, trigger_parser

router = fastapi.APIRouter()

router.add_api_route(path='/coins', methods=["GET"], endpoint=get_coins)
router.add_api_route(path="/trigger_parses", methods=["GET"], endpoint=trigger_parser)