import asyncio
import random

import json


async def wait(sec: int):
    await asyncio.sleep(sec)


async def create_resp(req):
    resp = {'request_id': req['request_id']}
    data = req['data']
    data = data.split('%%')
    for d in data:
        d_splited = d.split('%')
        print(d_splited)
        d_key = d_splited[0]
        d_values = d_splited[1:]
        d_value = dict(zip(d_values[0::2], d_values[1::2]))
        resp[d_key] = d_value
    return resp


async def parce_req(req):
    get = str(req).split(' ')[1][2:].split('&')
    res = {rec.split('=')[0]: rec.split('=')[1] for rec in get}
    return res


async def echo_server(reader, writer):
    req = await reader.read(100)
    print(req)
    # await wait(random.randint(1, 5))

    resp = await create_resp(await parce_req(req))

    writer.write(b'HTTP/1.1 200 OK\n\n' + json.dumps(resp).encode())
    await writer.drain()
    writer.close()


async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()


asyncio.run(main('127.0.0.1', 5000))
