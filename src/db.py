import asyncpg

from auth import POSTGRES_PASSWORD


class Database:
    def __init__(self):
        self.conn: asyncpg.Connection or None = None
        self.cache = {}  # short_code: long_url

    async def connect(self):
        if self.conn:
            raise Exception("Already connected to the database.")
        self.conn = await asyncpg.connect(
            user='postgres',
            password=POSTGRES_PASSWORD,
            database='bulbgur',
            host='postgres'
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
        long_url = await self.conn.fetchval('SELECT long_url FROM short_urls WHERE short_code=($1)', short_code)
        if long_url:
            self.cache[short_code] = long_url
        return long_url

