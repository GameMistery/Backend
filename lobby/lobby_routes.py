from fastapi import APIRouter
from fastapi.responses import JSONResponse
from extensions import lobbyservice
from config import settings

router = APIRouter()


@router.get('/get-lobbies')
async def get_lobbies():
    lobbies = lobbyservice.get_lobbies()
    return JSONResponse(content={'lobbies': [lobby.to_dict() for lobby in lobbies]},
                        status_code=200, headers={"Access-Control-Allow-Origin": settings.ENDPOINT_CORS})
