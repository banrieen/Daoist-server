from sanic import Request, Websocket

async def feed(request: Request, ws: Websocket):
    pass

app.add_websocket_route(feed, "/feed")
