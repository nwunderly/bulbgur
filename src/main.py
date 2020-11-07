from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from auth import SECRET_KEY


app = FastAPI(redoc_url=None, docs_url=None)
app.token = None
image_folder = 'data/'
allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4', '.py', '.txt', '.xml', '.log', '.sh', '.exe', '.php', '.css', '.html']

templates = Jinja2Templates(directory="templates")


@app.get('/')
async def index(request: Request):
    return "bulbe.rocks image API is active."


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="strict", https_only=True, max_age=14*24*60*60)
