from dataclasses import dataclass
import re
from typing import Callable, Pattern, Tuple
from pysev.request import Request
from pysev.response import Response

from pysev.pysev_func import PysevFunc


@dataclass
class Route:
    method: str
    path: str
    callback: PysevFunc
    compiled: Pattern


def http404(request: Request):
    return Response(status=404)


def http405(request: Request):
    return Response(status=405)


class Router:
    def __init__(self) -> None:
        self.routes: list[Route] = []

    def add(self, method: str, path: str, pysev_func: PysevFunc) -> None:
        self.routes.append(Route(method, path, pysev_func, re.compile(path)))

    def match(self, method: str, path: str) -> Tuple[PysevFunc, dict]:
        error_callback = http404
        for route in self.routes:
            matched = route.compiled.match(path)
            if not matched:
                continue
            error_callback = http405
            kwargs = matched.groupdict()
            if method == route.method:
                return route.callback, kwargs
        return error_callback, {}
