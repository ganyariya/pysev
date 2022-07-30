from http.client import responses as http_responses
import json
from typing import Optional
from wsgiref.headers import Headers

import jinja2


class Response:

    default_status = 200
    default_charset = "utf-8"
    default_content_type = "text/html; charset=UTF-8"

    def __init__(
        self,
        body: str = "",
        status: Optional[int] = None,
        headers: Optional[dict[str, str]] = None,
        charset: Optional[str] = None,
    ) -> None:
        self._body = body
        self.status = status or self.default_status
        self.headers = Headers()
        self.charset = charset or self.default_charset

        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)

    @property
    def status_code(self) -> str:
        return f"{self.status} {http_responses[self.status]}"

    @property
    def header_list(self) -> list[tuple[str, str]]:
        if "Content-Type" not in self.headers:
            self.headers.add_header("Content-Type", self.default_content_type)
        return self.headers.items()

    @property
    def body(self) -> list[bytes]:
        if isinstance(self._body, str):
            return [self._body.encode(self.charset)]
        return [self._body]


class JSONResponse(Response):
    default_content_type = "text/json; charset=UTF-8"

    def __init__(
        self,
        dic,
        status: Optional[int] = None,
        headers: Optional[dict[str, str]] = None,
        charset: Optional[str] = None,
        **dump_args,
    ) -> None:
        super().__init__("", status, headers, charset)
        self.dic = dic
        self.json_dump_args = dump_args

    @property
    def body(self) -> list[bytes]:
        return [json.dumps(self.dic, **self.json_dump_args).encode(self.charset)]


class TemplateResponse(Response):
    default_content_type = "text/html; charset=UTF-8"

    def __init__(
        self,
        filename,
        status: Optional[int] = None,
        headers: Optional[dict[str, str]] = None,
        charset: Optional[str] = None,
        **tpl_args,
    ) -> None:
        super().__init__("", status, headers, charset)
        self.filename = filename
        self.tpl_args = tpl_args

    def render_body(self, jinja2_environment: jinja2.Environment):
        template = jinja2_environment.get_template(self.filename)
        return [template.render(**self.tpl_args).encode(self.charset)]
