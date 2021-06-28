from aiohttp import web
from pathlib import Path
import sys
import json


file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass


async def test_index(aiohttp_client, loop):
    from app.handlers.index import IndexHandler
    index = IndexHandler()
    app = web.Application()
    app.router.add_route('GET', '/', index.handler)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello' in text


async def test_status(aiohttp_client, loop):
    from app.handlers import StatusHandler
    status = StatusHandler()
    app = web.Application()
    app.router.add_route('GET', '/status', status.handler)
    client = await aiohttp_client(app)
    resp = await client.get('/status')
    assert resp.status == 200
    text = await resp.text()
    response_data = json.loads(text)
    assert response_data.get('hostname')
