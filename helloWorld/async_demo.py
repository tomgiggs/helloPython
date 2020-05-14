#encoding=utf8
import httpx#相当异步requests
import asyncio
# async def demo():# async 这个关键字在Python3.6就可以使用，但是await需要在3.7版本才有
#     print('hello')
# asyncio.run(demo())
# async def demo2():
#     r = await httpx.get('https://www.baidu.com/')
#     print(r)# SyntaxError: 'await' outside function
#
# # asyncio.run(demo2())#使用async/await后就没法直接启动函数了，需要这样才能启动不然会报错SyntaxError: 'await' outside function
# loop = asyncio.get_event_loop()
# loop.run_until_complete(demo2())


# import starlette #异步flask
import uvicorn #asgi库

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

async def homepage(request):
    return JSONResponse({'hello': 'world'})

routes = [
    Route("/", endpoint=homepage)
]

app = Starlette(debug=True, routes=routes)

uvicorn.run(app,http='h11', loop='asyncio',port=8888)