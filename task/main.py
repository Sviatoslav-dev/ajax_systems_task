import asyncio
import random

import json


async def wait(sec: int):
    await asyncio.sleep(sec)


async def create_resp(req):
    resp = {'request_id': req['request_id']}
    data = req['data']
    data = data.split('%%')
    for entity in data:
        entity_splited = entity.split('%')
        print(entity_splited)
        entity_key = entity_splited[0]
        d_value = entity_splited[1:]
        d_value = dict(zip(d_value[0::2], d_value[1::2]))
        resp[entity_key] = d_value
    return resp


async def parce_req(req):
    get = str(req).split(' ')[1][2:].split('&')
    return {rec.split('=')[0]: rec.split('=')[1] for rec in get}


async def echo_server(reader, writer):
    req = await reader.read(100)
    print(req)
    await wait(random.randint(1, 5))

    resp = await create_resp(await parce_req(req))

    writer.write(b'HTTP/1.1 200 OK\n\n' + json.dumps(resp).encode())
    await writer.drain()
    writer.close()


async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()


asyncio.run(main('127.0.0.1', 5000))
