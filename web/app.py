#!/usr/bin/env python3
import asyncio
import os
import aiohttp_jinja2
import jinja2
import aioredis
from aiohttp.web import (Application, Response, WebSocketResponse, WSMsgType,
                         run_app)

WS_FILE = os.path.join(os.path.dirname(__file__), 'websocket.html')

async def static_handler(request):
    response = aiohttp_jinja2.render_template('index.html',
                                              request,
                                              {})
    return response

async def index_handler(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return Response(text=text)

# websocket handler method
async def wshandler(request):
    resp = WebSocketResponse()
    ok, protocol = resp.can_prepare(request)
    if not ok:
        with open(WS_FILE, 'rb') as fp:
            return Response(body=fp.read(), content_type='text/html')

    await resp.prepare(request)

    try:
        print('Someone joined.')
        for ws in request.app['sockets']:
            ws.send_str('Someone joined')
        request.app['sockets'].append(resp)

        async for msg in resp:
            if msg.type == WSMsgType.TEXT:
                for ws in request.app['sockets']:
                    if ws is not resp:
                        ws.send_str(msg.data)
            else:
                return resp
        return resp

    finally:
        request.app['sockets'].remove(resp)
        print('Someone disconnected.')
        for ws in request.app['sockets']:
            ws.send_str('Someone disconnected.')

# asynchronous method to listen for messages from redis
async def listen_to_redis(app):
    try:
        sub = await aioredis.create_redis(('redis', 6379), loop=app.loop)
        ch, *_ = await sub.subscribe('news')
        async for msg in ch.iter(encoding='utf-8'):
            # Forward message to all connected websockets:
            for ws in app['sockets']:
                ws.send_str('{}'.format(msg))
    except asyncio.CancelledError:
        pass
    finally:
        await sub.unsubscribe(ch.name)
        await sub.quit()

async def on_shutdown(app):
    for ws in app['sockets']:
        await ws.close()

async def start_background_tasks(app):
    app['redis_listener'] = app.loop.create_task(listen_to_redis(app))

# application configuation
async def init(loop):

    # routing and global collection of connected websockets
    app = Application()
    app['sockets'] = []
    app.router.add_get('/', static_handler)
    app.router.add_get('/websocket', wshandler)

    # include background tasks and a graceful shutdown
    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(on_shutdown)           
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader('templates'))

    return app

# retrieve an instance of app, begin the event loop and run the app
loop = asyncio.get_event_loop()
app = loop.run_until_complete(init(loop))
run_app(app)
