from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI(redoc_url=None, docs_url=None)
app.token = None
image_folder = 'data/'

app.mount('/css', StaticFiles(directory='css'), name='css')
app.mount('/assets', StaticFiles(directory='assets'), name='site_assets')
# app.mount('/image', StaticFiles(directory='data'), name='images_legacy_support')
app.mount('/', StaticFiles(directory='data'), name='images')
