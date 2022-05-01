from fastapi import FastAPI
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

app = FastAPI(redoc_url=None, docs_url=None)
app.token = None
image_folder = "data/"


@app.route("/")
async def redirect(request):
    return RedirectResponse("https://bulbe.rocks")


app.mount("/", StaticFiles(directory=image_folder), name="images")
