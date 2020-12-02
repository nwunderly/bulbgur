import datetime

import aiohttp
from fastapi import FastAPI, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from auth import SECRET_KEY
from src.utils.db import Database
from src.utils.mars import MarsRoverPhotos


#############
# APP SETUP #
#############


started_at = datetime.datetime.now()

app = FastAPI(redoc_url=None, docs_url=None)
db = Database()
mars = MarsRoverPhotos()

app.token = None
image_folder = 'data/'
allowed_extensions = ['.png', '.jpeg', '.jpg', '.gif', '.webm', '.mp4', '.py', '.txt', '.xml', '.log', '.sh', '.exe', '.php', '.css', '.html']

templates = Jinja2Templates(directory="templates")

app.mount('/css', StaticFiles(directory='css'), name='css')
app.mount('/js', StaticFiles(directory='js'), name='js')
app.mount('/assets', StaticFiles(directory='assets'), name='assets')


@app.on_event('startup')
async def startup():
    if not db.is_connected:
        await db.connect()


@app.on_event('shutdown')
async def cleanup():
    if db.is_connected:
        await db.close()


#####################
# USER-FACING PATHS #
#####################


@app.route('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.route('/mars')
async def mars_rover_photo(request: Request):
    url, rover, camera, earth_date = await mars.get_random_image()
    return templates.TemplateResponse(
        'mars.html', 
        {'request': request, 'rover_photo': url, 'rover': rover, 'camera': camera, 'earth_date': earth_date}
    )


@app.route('/bounce')
async def bounce(request: Request):
    return templates.TemplateResponse('bounce.html', {'request': request})


@app.route('/status')
async def server_status(request: Request):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://i.bulbe.rocks/poggies.png") as resp:
            image_server_status = resp.status == 200
    return PlainTextResponse(f"API is online.\n"
                             f"Runtime {datetime.datetime.now() - started_at}\n"
                             f"Database: {'ONLINE' if db.is_connected else 'OFFLINE'}\n"
                             f"Image Server: {'ONLINE' if image_server_status else 'OFFLINE'}")


@app.get('/login')
async def login_screen(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/authenticate')
async def authenticate_user(request: Request):
    # TODO: this
    return PlainTextResponse("NOT YET IMPLEMENTED")


#######################
# API : URL SHORTENER #
#######################


@app.post('/short_url/new/')
async def new_short_url(request: Request):
    # TODO: This
    return PlainTextResponse("NOT YET IMPLEMENTED")


@app.route('/short_url/del/{short_code}', methods=['GET', 'DELETE'])
async def del_short_url(request: Request, short_code: str = None):
    # TODO: This
    return PlainTextResponse("NOT YET IMPLEMENTED")


######################
# API : IMAGE SERVER #
######################


@app.post('/file_upload/new/')
async def new_file_upload(request: Request):
    # TODO: This
    return PlainTextResponse("NOT YET IMPLEMENTED")


@app.route('/file_upload/del/{image_name}', methods=['GET', 'DELETE'])
async def del_file_upload(request: Request, image_name: str = None):
    # TODO: This
    return PlainTextResponse("NOT YET IMPLEMENTED")


#####################################
# CATCH-ALL : HANDLE SHORTENED URLS #
#####################################


@app.get('/{short_code}')
async def redirect(request: Request, short_code: str = None):
    if not short_code or len(short_code) > 10:
        raise HTTPException(status_code=404)
    long_url = await db.get_long_url(short_code)
    if not long_url:
        raise HTTPException(status_code=404)
    return RedirectResponse(long_url, status_code=301)


###################################################
# MIDDLEWARE FOR HANDLING LOGIN SESSIONS SECURELY #
###################################################


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="strict", https_only=True, max_age=14*24*60*60)
