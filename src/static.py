from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


app = FastAPI(redoc_url=None, docs_url=None)
app.token = None
image_folder = 'data/'


@app.route('/')
async def redirect():
    return RedirectResponse("https://bulbe.rocks")


app.mount('/', StaticFiles(directory=image_folder), name='images')
