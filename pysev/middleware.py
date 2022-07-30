from asyncio.log import logger
from typing import Callable
from pysev.app import App


class Middleware:
    def __init__(self, app: App) -> None:
        self.app = app

    def __call__(self, env: dict, start_response: Callable) -> list[bytes]:
        return self.app(env, start_response)


class LogMiddleware(Middleware):
    def __init__(self, app: App) -> None:
        super().__init__(app)

    def __call__(self, env: dict, start_response: Callable) -> list[bytes]:
        logger.info(env)
        return super().__call__(env, start_response)
