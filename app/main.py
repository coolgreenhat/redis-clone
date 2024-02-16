import asyncio
from app.response import redis_response

async def handle_client(reader, writer):
    while True:
        received_data = await reader.read(1024)
        decoded_data = received_data.decode()
        if not decoded_data:
            break

        response = None
        if "ping" in decoded_data.lower():
            response = "PONG"
        if response is None:
            decoded_data_list = decoded_data.split("\r\n")
            response = redis_response(decoded_data_list)
        if response:
            if not response.startswith("$-"):
                response = "+" + response + "\r\n"
            writer.write(response.encode())
        await writer.drain()
 
    writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 6379) 
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
