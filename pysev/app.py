import os
from typing import Callable, Optional

from jinja2 import Environment, FileSystemLoader
from pysev.pysev_func import PysevFunc
from pysev.request import Request
from pysev.response import TemplateResponse
from pysev.router import Router


class App:
    def __init__(self, templates=None) -> None:
        self.router = Router()
        if templates is None:
            templates = [os.path.join(os.path.abspath("."), "templates")]
        self.jinja2_environment = Environment(loader=FileSystemLoader(templates))

    def route(
        self,
        path: str = "/",
        method: str = "GET",
        callback: Optional[PysevFunc] = None,
    ):
        def decorator(callback_func: Callable) -> Callable:
            self.router.add(method, path, callback_func)
            return callback_func

        """
        @app.router(callback=func)
        def hello
        の場合は func をかわりに router.add する
        @app.router() なら hello を router.add する
        """
        return decorator(callback) if callback else decorator

    def __call__(self, env: dict, start_response: Callable) -> list[bytes]:
        request = Request(env)
        callback, kwargs = self.router.match(request.method, request.path)
        response = callback(request, **kwargs)
        start_response(response.status_code, response.header_list)
        if isinstance(response, TemplateResponse):
            return response.render_body(self.jinja2_environment)
        return response.body
