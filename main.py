from pysev.app import App
from wsgiref.simple_server import make_server
from pysev.middleware import LogMiddleware, Middleware

from pysev.request import Request
from pysev.response import JSONResponse, Response, TemplateResponse

app = App()


@app.route("^/$", "GET")
def hello(request: Request, **kwargs) -> Response:
    return JSONResponse({"a": "Hello, World"})


@app.route("^/user/$", "GET")
def create_user(request: Request, **kwargs) -> Response:
    print(request.path)
    users = [f"user{i}" for i in range(10)]
    return TemplateResponse("users.html", users=users)


@app.route(r"^/user/(?P<name>\w+)/$", "GET")
def user_detail(request: Request, name, **kwargs) -> Response:
    body = f"Hello, {name}"
    return Response(body)


if __name__ == "__main__":
    app = LogMiddleware(app)
    httpd = make_server("", 8000, app)
    httpd.serve_forever()
