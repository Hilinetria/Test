import asyncio
import json
from aiohttp import web, WSMsgType
from models import activation
from datetime import datetime


async def check_activation(conn):
    res = await conn.execute(activation.select())
    result = [r for r in res]
    return result[0] if result else None


async def start_handler(request, service):
    text = 'Service started!'
    success = False

    async with request.app['db'].acquire() as conn:
        record = await check_activation(conn)
        app_service = request.app['services'].get(service)
        config = request.app['config']['services'].get(service)
        # если активировано управление
        if record and record[1]:
            # не запущен нужный сервис
            if not app_service:
                try:
                    proc = await asyncio.create_subprocess_exec(config['command'], config['path'])
                    request.app['services'][service] = proc
                    success = True
                except Exception:
                    text = 'Something gone wrong!'
            # уже запущен нужный сервис
            else:
                text = 'Service already started!'

    return {'service': service, 'text': text, 'success': success, 'status': 1}


async def stop_handler(request, service):
    text = None
    success = False
    not_started_msg = 'Service not started!'
    async with request.app['db'].acquire() as conn:
        record = await check_activation(conn)
        app_service = request.app['services'].get(service)
        # если активировано управление
        if record and record[1]:
            # запущен нужный сервис
            if app_service:
                try:
                    if app_service.returncode:
                        text = not_started_msg
                    else:
                        app_service.terminate()
                        success = True
                        text = 'Service stopped!'
                except Exception:
                    text = 'Something gone wrong!'
                else:
                    del request.app['services'][service]
            # не запущен нужный сервис
            else:
                text = not_started_msg

    return {'service': service, 'text': text, 'success': success, 'status': 0}


async def restart_handler(request, service):
    text = 'Service restarted!'
    success = False
    restarted = {'text': text, 'success': success}
    try:
        await stop_handler(request, service)
        restarted = await start_handler(request, service)
    except Exception:
        text = 'Something gone wrong!'

    restarted['text'] = text
    return restarted


async def activate_handler(request, checked=True):
    success = True
    checked = int(checked)
    async with request.app['db'].acquire() as conn:
        try:
            record = await check_activation(conn)
            if not record:
                await conn.execute(activation.insert().values(is_activated=checked, pub_date=datetime.now()))
            else:
                await conn.execute(activation.update().
                                   where(activation.c.id == record[0]).
                                   values(is_activated=checked))
            text = 'Service activated!' if checked else 'Service deactivated'
        except Exception:
            text = 'Something gone wrong!'
            success = False

    return {'text': text, 'success': success, 'disable': not checked}


async def check_activation_on_start(request):
    success = True
    disabled = False
    text = 'Service activated!'
    async with request.app['db'].acquire() as conn:
        try:
            record = await check_activation(conn)
            if record:
                disabled = not record[1]
                text = 'Service activated!' if not disabled else 'Service deactivated'
        except Exception:
            text = 'Something gone wrong!'
            success = False

        return {'text': text, 'success': success, 'disable': disabled, 'checked': not disabled}


async def websocket_handler(request):

    __handler_map = {
        'start': (start_handler, 'service'),
        'stop': (stop_handler, 'service'),
        'restart': (restart_handler, 'service'),
        'activate': (activate_handler, 'checked'),
    }
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    request.app['websockets'].append(ws)
    result = await check_activation_on_start(request)
    await ws.send_json(result)

    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            json_data = json.loads(msg.data)
            handler = __handler_map.get(json_data.get('type'))
            if msg.data == 'close':
                await ws.close()
                if request.app['websockets'].get(ws):
                    del request.app['websockets'][ws]
            elif handler:
                result = await handler[0](request, *[json_data.get(param) for param in handler[1:]])
                await ws.send_json(result)

        elif msg.type == WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws



