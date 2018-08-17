import aiohttp_jinja2
from aiohttp import web
from handlers import activate_handler

class Index(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):
        # result = await activate_handler(self.request)
        # return result
        return {}