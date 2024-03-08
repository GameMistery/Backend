from ranking.ranking_db import db_get_top_ten

async def ranking_endpoints(parsedjson, websocket):
    if parsedjson['action'] == 'ranking_get_top_ten':
        await get_top_ten(websocket)

async def get_top_ten(websocket):
    try:
        ranking = db_get_top_ten()
        await websocket.send_json({'action': 'top-ten', 'ranking': ranking})
        
    except Exception as e: 
        await websocket.send_json({'action': 'failed', 'info': str(e)})