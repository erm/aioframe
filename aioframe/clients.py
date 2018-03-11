import aiohttp


async def get_request(session, url):
    try:
        async with session.get(url) as resp:
            assert 200 == resp.status, ('Request failed.')
            result = await resp.text()
            return result
    except aiohttp.client_exceptions.ClientConnectorError:
        print('Session connection error.')
        return None
