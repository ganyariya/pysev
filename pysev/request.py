import cgi
import json
from typing import Optional
from urllib.parse import parse_qs


class Request:
    def __init__(self, environ: dict, charset="utf-8") -> None:
        self.environ = environ
        self.charset = charset
        self._body: Optional[bytes] = None

    @property
    def path(self) -> str:
        return self.environ["PATH_INFO"] or "/"

    @property
    def method(self) -> str:
        return self.environ["REQUEST_METHOD"].upper()

    @property
    def body(self) -> bytes:
        if self._body is None:
            content_length = int(self.environ.get("CONTENT_LENGTH", 0))
            self._body = self.environ["wsgi.input"].read(content_length)
        return self._body

    @property
    def query(self):
        return parse_qs(self.environ["QUERY_STRING"])

    @property
    def text(self) -> str:
        return self.body.decode(self.charset)

    @property
    def json(self) -> object:
        return json.loads(self.body)

    @property
    def forms(self):
        form = cgi.FieldStorage(
            fp=self.environ["wsgi.input"],
            environ=self.environ,
            keep_blank_values=True,
        )
        params = {k: form[k].value for k in form}
        return params
