from aiohttp import web


# @middleware
# async def middleware(request, handler):
#     resp = await handler(request)
#     resp.text = resp.text + ' wink'
#     return resp


@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status != 404:
            return response
        message = response.message
    except web.HTTPException as e:
        if e.status != 404:
            raise
        message = ex.reason
    return web.json_response({'error': message})



# def error_pages(overrides):
#     async def middleware(app, handler):
#         async def middleware_handler(request):
#             try:
#                 response = await handler(request)
#                 override = overrides.get(response.status)
#                 if override is None:
#                     return response
#                 else:
#                     return await override(request, response)
#             except web.HTTPException as ex:
#                 override = overrides.get(ex.status)
#                 if override is None:
#                     raise
#                 else:
#                     return await override(request, ex)
#         return middleware_handler
#     return middleware
