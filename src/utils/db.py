import secrets
from typing import Optional

import asyncpg
from auth import POSTGRES_PASSWORD


class Database:
    def __init__(self):
        self.conn: Optional[asyncpg.Connection] = None
        self.cache = {}  # short_code: long_url

    async def connect(self):
        if self.conn:
            raise Exception("Already connected to the database.")
        self.conn = await asyncpg.connect(
            user="postgres",
            password=POSTGRES_PASSWORD,
            database="bulbgur",
            host="postgres",
        )

    async def close(self):
        if self.conn:
            await self.conn.close()
            self.conn = None

    @property
    def is_connected(self):
        return bool(self.conn)

    async def get_long_url(self, short_code):
        if not self.conn:
            await self.connect()
        if short_code in self.cache:
            return self.cache[short_code]
        long_url = await self.conn.fetchval(
            "SELECT long_url FROM short_urls WHERE short_code=($1)", short_code
        )
        if long_url:
            self.cache[short_code] = long_url
        return long_url

    async def new_short_url(self, long_url, short_code=None):
        if not self.conn:
            await self.connect()
        current_short_code = await self.conn.fetchval(
            "SELECT short_code FROM short_urls WHERE long_url=($1)", long_url
        )
        if current_short_code:
            return current_short_code
        if not short_code:
            short_code = secrets.token_hex(5)
        await self.conn.execute(
            "INSERT INTO short_urls (short_code, long_url, created_at) VALUES ($1, $2, now())",
            short_code,
            long_url,
        )
        self.cache[short_code] = long_url
        return short_code
