import os
import json

from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth import LEADERBOARD_API_TOKEN


app = FastAPI(redoc_url=None, docs_url=None)
app.token = None

LEADERBOARD = 'leaderboard/leaderboard.json'


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
    def dump(cls, data: str):
        with open(LEADERBOARD, "w") as fp:
            fp.write(json)
            fp.write(data)
            cls.data = json.loads(data)

    @classmethod
    def get(cls):
        if not cls.data:
            raise HTTPException(500, "Missing data.")
        return cls.data


LeaderboardCache.ensure_file_exists()
LeaderboardCache.load()


@app.post('/leaderboard')
async def post_leaderboard(request: Request):
    if request.headers.get("X-Authorization") != LEADERBOARD_API_TOKEN:
        raise HTTPException(401)

    body = (await request.body()).decode()
    LeaderboardCache.dump(body)
    return "OK"


@app.get('/leaderboard')
async def get_leaderboard():
    return JSONResponse(LeaderboardCache.get())
