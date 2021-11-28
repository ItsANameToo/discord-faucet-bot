
import aiohttp
import json


class API:
    async def get(self, endpoint: str, headers: dict = {}):
        """ Perform an async GET request and return a JSON response """
        async with aiohttp.ClientSession(headers=headers) as session:
            request = await session.get(f"{endpoint}")
            response = await request.read()
            response_to_json = json.loads(response)
            return response_to_json

    async def post_raw(self, endpoint: str, data: dict = {},  headers: dict = {}):
        """ Perform an async POST request with raw data and return its response """
        async with aiohttp.ClientSession(headers=headers) as session:
            request = await session.post(f"{endpoint}", data=data, headers=headers)
            return request

    async def post(self, endpoint: str, data: dict = {},  headers: dict = {}):
        """ Perform an async POST request and return its response """
        async with aiohttp.ClientSession(headers=headers) as session:
            request = await session.post(f"{endpoint}", json=data, headers=headers)
            return request