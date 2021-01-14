import os
import json
import html

from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth import LEADERBOARD_API_TOKEN


app = FastAPI(redoc_url=None, docs_url=None)
app.token = None

LEADERBOARD = 'leaderboard/leaderboard.json'


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LeaderboardCache:
    last_updated = None
    data = None

    @classmethod
    def ensure_file_exists(cls):
        if not os.path.exists(LEADERBOARD):
            with open(LEADERBOARD, 'w') as fp:
                fp.write('{}')

    @classmethod
    def load(cls):
        with open(LEADERBOARD, "r") as fp:
            cls.data = json.loads(fp.read())
            cls.last_updated = datetime.now()

    @classmethod
    def dump(cls, data: dict):
        with open(LEADERBOARD, "w") as fp:
            json.dump(data, fp)

    @classmethod
    def get(cls):
        if not cls.data:
            raise HTTPException(500, "Missing data.")
        return cls.data

    @classmethod
    def update(cls, data: str):
        data = json.loads(data)
        for _, user in data.items():
            user['username'] = html.escape(user['username'])
        cls.dump(data)
        cls.data = data


LeaderboardCache.ensure_file_exists()
LeaderboardCache.load()


@app.post('/leaderboard')
async def post_leaderboard(request: Request):
    if request.headers.get("X-Authorization") != LEADERBOARD_API_TOKEN:
        raise HTTPException(401)

    body = (await request.body()).decode()
    LeaderboardCache.update(body)
    return "OK"


@app.get('/leaderboard')
async def get_leaderboard():
    return JSONResponse(LeaderboardCache.get())
