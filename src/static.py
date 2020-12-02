from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


app = FastAPI(redoc_url=None, docs_url=None)
app.token = None
image_folder = 'data/'

app.mount('/css', StaticFiles(directory='css'), name='css')
app.mount('/js', StaticFiles(directory='js'), name='js')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')
# app.mount('/image', StaticFiles(directory='data'), name='images_legacy_support')
app.mount('/', StaticFiles(directory='data'), name='images')


@app.post('/')
async def redirect(request):
    return RedirectResponse("https://bulbe.rocks")
