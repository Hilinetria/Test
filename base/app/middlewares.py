import syslog
from settings import web_logger
from aiohttp import web


@web.middleware
async def error_middleware(request, handler):

    syslog.syslog(syslog.LOG_INFO, 'Request started')
    syslog.syslog(syslog.LOG_INFO, str(request))
    web_logger.info('Request started')
    web_logger.info(str(request))
    try:
        response = await handler(request)
        return response

    except Exception as ex:
        syslog.syslog(syslog.LOG_ERR, str(ex))
        web_logger.error(str(ex))
        raise


def setup_middlewares(app):
    app.middlewares.append(error_middleware)
