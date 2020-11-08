import asyncio
import os
import asyncpg

from os.path import splitext
from fastapi import FastAPI, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, FileResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from auth import SECRET_KEY, POSTGRES_PASSWORD


app = FastAPI(redoc_url=None, docs_url=None)
app.token = None
app.db = None
image_folder = 'data/'
allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4', '.py', '.txt', '.xml', '.log', '.sh', '.exe', '.php', '.css', '.html']

templates = Jinja2Templates(directory="templates")


@app.on_event('startup')
async def on_ready():
    if not app.db:
        app.db = await asyncpg.connect(
            user='postgres',
            password=POSTGRES_PASSWORD,
            database='bulbgur',
            host='postgres',
        )


@app.on_event('shutdown')
async def cleanup():
    if app.db:
        await app.db.close()


@app.get('/')
async def index(request: Request):
    return "bulbe.rocks image API is active."


@app.post('/shorten')
async def create_short_url(request: Request):
    return "NOT YET IMPLEMENTED"


@app.get('/delete/{short_code:path}')
async def delete_short_url(request: Request, short_code: str = None):
    return "NOT YET IMPLEMENTED"


@app.get('/{short_code:path}')
async def redirect(request: Request, short_code: str = None):
    if not short_code or len(short_code) > 10:
        raise HTTPException(status_code=404)
    elif app.db:
        long_url = await app.db.fetchval('SELECT long_url FROM short_urls WHERE short_code=($1)', short_code)
        if not long_url:
            raise HTTPException(status_code=404)
        return RedirectResponse(long_url, status_code=301)
    else:
        raise HTTPException(status_code=500)



app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="strict", https_only=True, max_age=14*24*60*60)
