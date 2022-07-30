from typing import Any, Callable

from pysev.request import Request
from pysev.response import Response

PysevFunc = Callable[[Request], Response]
