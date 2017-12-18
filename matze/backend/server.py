from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/")
async def test(request):
    return json({"hello": "world"})


def run():
    app.run(host="0.0.0.0", port=8000)
