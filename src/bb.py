import asyncio
import os
import secrets

from os.path import splitext
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from auth import BB_UPLOAD_TOKEN
from auth import SECRET_KEY


allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4', '.py', '.txt', '.xml', '.log', '.sh', '.exe', '.php', '.css', '.html']

app = FastAPI(redoc_url=None, docs_url=None)
image_folder = 'bb-data/'
app.mount('/img', StaticFiles(directory='bb'), name='images')
templates = Jinja2Templates(directory="templates")


@app.get('/')
async def index(request: Request):
    session = request.session
    if len(session) != 0 and session.last_upload_status:
        last_upload_status = f"<p>Successfully uploaded <a href=/img/{session.last_upload_status}>{session.last_upload_status}</a></p>"
        request.session.last_upload_status = None
        return templates.TemplateResponse("bb_upload.html", {"request": request, "last_upload_status": last_upload_status})
    else:
        return templates.TemplateResponse("bb_upload.html", {"request": request, "last_upload_status": ""})


@app.post('/upload')
async def upload(request: Request):
    form = await request.form()

    token = form["password"]
    if token != BB_UPLOAD_TOKEN:
        raise HTTPException(status_code=401)

    filename = form["file"].filename
    extension = splitext(filename)[1]
    if extension not in allowed_extensions:
        raise HTTPException(status_code=415, detail=f"File type not supported, allowed extensions are {allowed_extensions}")
    filename = secrets.token_urlsafe(5)
    binary_file = open(f'{image_folder}{filename}{extension}', 'wb')
    binary_file.write(await form['file'].read())
    binary_file.close()
    request.session.last_upload_status = filename
    return RedirectResponse("/")


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="strict", https_only=True, max_age=3600)


