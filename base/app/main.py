import jinja2
import aiohttp_jinja2
from aiohttp import web
from routes import setup_routes
from settings import close_pg, on_startup
from middlewares import setup_middlewares


app = web.Application()

setup_routes(app)

aiohttp_jinja2.setup(
    app, loader=jinja2.PackageLoader('main', 'templates'))
on_startup(app)
app.on_cleanup.append(close_pg)
setup_middlewares(app)

web.run_app(app)
