import os
import aiohttp
import datetime
import secrets

from os.path import splitext
from fastapi import FastAPI, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from auth import SECRET_KEY, EMAIL, PASSWORD, API_KEY
from .utils.db import Database
from .utils.mars import MarsRoverPhotos


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
app.mount('/i', StaticFiles(directory=image_folder), name='images')


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


@app.route('/login')
async def login_screen(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


@app.post('/authenticate')
async def authenticate_user(request: Request):
    session = request.session
    form = await request.form()
    if form['email'] == EMAIL and form['password'] == PASSWORD:
        token = secrets.token_urlsafe()
        app.token = token
        session['token'] = token
        return RedirectResponse('/dash')
    else:
        raise HTTPException(status_code=401)


@app.route('/dash')
async def dash(request: Request):
    session = request.session
    if len(session) != 0:
        if session['token'] == app.token:
            images = os.listdir(image_folder)
            return templates.TemplateResponse("dash.html", {"request": request, "images": images})
        else:
            raise HTTPException(status_code=401)
    else:
        raise HTTPException(status_code=401)


#######################
# API : URL SHORTENER #
#######################


@app.post('/short_url/new/')
async def new_short_url(request: Request):
    if request.headers.get('x-authorization') == API_KEY or request.query_params.get('api_key') == API_KEY:
        long_url = request.query_params['long_url']
        short_code = request.query_params.get('short_code')
        short_code = await db.new_short_url(long_url, short_code)
        return PlainTextResponse("https://bulbe.rocks/"+short_code)
    else:
        raise HTTPException(status_code=401)


@app.get('/short_url/del/{short_code}')
async def del_short_url(request: Request, short_code: str = None):
    # TODO: This
    return PlainTextResponse("NOT YET IMPLEMENTED")


######################
# API : IMAGE SERVER #
######################


@app.post('/file_upload/new/')
async def new_file_upload(request: Request):
    if request.headers.get('x-authorization') == API_KEY:
        form = await request.form()
        filename = form["upload_file"].filename
        extension = splitext(filename)[1]
        if extension not in allowed_extensions:
            raise HTTPException(status_code=415, detail=f"File type not supported. Allowed extensions: {allowed_extensions}")
        filename = secrets.token_urlsafe(5)
        binary_file = open(f'{image_folder}{filename}{extension}', 'wb')
        binary_file.write(await form['upload_file'].read())
        binary_file.close()
        return {"filename": filename, "extension": extension}
    else:
        raise HTTPException(status_code=401)


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
