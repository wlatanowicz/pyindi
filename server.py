import asyncio
import logging

from devices import *
from indi.device.pool import DevicePool
from indi.routing import Router
from indi.transport.server import TCP as TCPServer

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

router = Router()

DevicePool.init(router)

server = TCPServer(router=router)

loop = asyncio.get_event_loop()
loop.create_task(server.start())
loop.run_forever()
