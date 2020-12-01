import aiohttp
import asyncio
import random


from auth import NASA_API_KEY as key


ROVERS = ['curiosity']#, 'opportunity', 'spirit']


class MarsRoverPhotos:
    def __init__(self):
        self.cache = None
        self.max_sol = None
    
    async def get_max_sols(self):
        self.max_sol = dict([(rover, 0) for rover in ROVERS])
        async with aiohttp.ClientSession() as session:
            for rover in ROVERS:
                async with session.get(f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover}?api_key={key}") as resp:
                    if resp.status != 200:
                        self.max_sol = None
                        return
                    data = await resp.json()
                    self.max_sol[rover] = data['photo_manifest']['max_sol']

    def cache_empty(self):
        return not bool(self.cache and self.max_sol)

    async def fill_cache(self):
        self.cache = []
        if not self.max_sol:
            await self.get_max_sols()

        async with aiohttp.ClientSession() as session:
            for rover in ROVERS:
                _max = self.max_sol[rover]
                async with session.get(f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos?sol={random.randint(1, _max)}&api_key={key}") as resp:
                    data = await resp.json()
                if not data['photos']:
                    continue
                for photo in data['photos']:
                    self.cache.append([photo['img_src'], photo['camera']['full_name']])
                random.shuffle(self.cache[rover])

    async def get_random_image(self):
        if self.cache_empty():
            await self.fill_cache()
        return self.cache.pop()

