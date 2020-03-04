import asyncio
import logging

from indi.routing import Client
from indi.transport import Buffer
from indi.routing import Router

logger = logging.getLogger(__name__)


class ConnectionHandler(Client):
    connections = []

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, router: Router):
        self.buffer = Buffer()
        self.reader = reader
        self.writer = writer
        self.router = router
        self.sender_lock = asyncio.Lock()
        if self.router:
            self.router.register_client(self)

    @classmethod
    def handler(cls, router):
        async def handler_func(reader, writer):
            conn = cls(reader, writer, router)
            cls.connections.append(conn)
            try:
                await conn.wait_for_messages()
            except:
                pass

            conn.close()
            cls.connections.remove(conn)
        
        return handler_func

    async def wait_for_messages(self):
        while True:
            logger.debug(f"TCP: waiting for data")
            message = await self.reader.read(1024)
            if not message:
                logger.debug(f"TCP: no data, breaking")
                break
            logger.debug(f"TCP: got data: {message}")
            self.buffer.append(message.decode("latin1"))
            await self.buffer.process(self.message_from_client)

    async def message_from_client(self, message):
        if self.router:
            self.router.process_message(message, sender=self)
            await asyncio.sleep(0)

    async def message_from_device(self, message):
        data = message.to_string()
        async with self.sender_lock:
            logger.debug(f"TCP: sending data: {data}")
            self.writer.write(data)
            await self.writer.drain()

    def close(self):
        if self.writer:
            self.writer.close()
        if self.router:
            self.router.unregister_client(self)


class TCP:
    def __init__(self, address="0.0.0.0", port=7624, max_connections=5, router=None):
        self.address = address
        self.port = port
        self.max_connections = max_connections
        self.router = router

    async def start(self):
        logger.info("Starting TCP INDI server on %s:%s", self.address, self.port)
        await asyncio.start_server(
            ConnectionHandler.handler(self.router),
            host=self.address,
            port=self.port,
        )
