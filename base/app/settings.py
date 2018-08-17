import logging
import pathlib
import yaml
import asyncio
from aiopg.sa import create_engine


BASE_DIR = pathlib.Path(__file__).parent.parent
STATIC_DIR = pathlib.Path(__file__).parent / 'static'
config_path = BASE_DIR / 'config' / 'app.yaml'


# logging.basicConfig(filename=BASE_DIR/"log/base.log", level=logging.INFO)

access_logger = logging.getLogger('aiohttp.access')
client_logger = logging.getLogger('aiohttp.client')
internal_logger = logging.getLogger('aiohttp.internal')
server_logger = logging.getLogger('aiohttp.server')
web_logger = logging.getLogger('aiohttp.web')
ws_logger = logging.getLogger('aiohttp.websocket')

async def init_pg(app):
    conf = app['config']['postgres']
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def get_config(path):
    with open(path) as f:
        config = yaml.load(f)
    return config


async def check_processes(app, seconds=10):
    services_status = {}
    while True:
        services = app['services'].copy()
        for ws in app['websockets']:
            for key, service in services.items():
                services_status['service'] = key
                services_status['success'] = True
                if service.returncode:
                    services_status['status'] = 0
                    services_status['text'] = 'Service stopped!'
                    del app['services'][key]
                else:
                    # print('123', services)
                    services_status['status'] = 1
                    services_status['text'] = 'Service started!'
            if services_status:
                await ws.send_json(services_status)
            services_status = {}
        await asyncio.sleep(seconds)


async def start_workers(app):
    asyncio.ensure_future(check_processes(app))


def on_startup(app):
    app['config'] = config
    app['services'] = {}
    app['websockets'] = []
    app.on_startup.append(start_workers)
    app.on_startup.append(init_pg)


config = get_config(config_path)
