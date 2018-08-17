# routes.py
from views import Index
from handlers import websocket_handler
from settings import STATIC_DIR


def setup_routes(app):
    app.router.add_route(method='POST', path='/', handler=Index, name='index')
    app.router.add_route(method='GET', path='/', handler=Index, name='index')
    app.router.add_static('/static', path=STATIC_DIR, name='static')
    app.router.add_route(method='GET', path='/ws', handler=websocket_handler, name='ws')

    # <!--<script src="{{ app.router.static.url(filename='js/main.js') }}"></script>-->
