import asyncio

from service import method_give, method_write, method_delete

QUERY = ['ЗОПИШИ', 'УДОЛИ', 'ОТДОВАЙ', 'АМОЖНА?']

QUERY_FUNCTION = {
    'ЗОПИШИ': method_write,
    'УДОЛИ': method_delete,
    'ОТДОВАЙ': method_give
}

count = 0


async def check_access_request(request: str, count):
    # reader, writer = await asyncio.open_connection(
    #     'vragi-vezde.to.digital', 51624)
    # writer.write(request)
    # data = await reader.read(100)
    # writer.close()
    # if data.decode() == "МОЖНА РКСОК / 1.0":
    #     return True, ''.encode()
    # else:
    #     return False, data
    print(request.decode())
    return True, ''


async def check_request(request: str):
    line_massege = request.split('\r\n')
    first_line = line_massege[0].split(' ')
    name = ' '.join(first_line[1:-1])
    command = first_line[0]
    if len(first_line) >= 2 and command in QUERY and first_line[-1] == 'РКСОК/1.0' and len(name) <= 30:
        body = '\r\n'.join(line_massege[1:])
        return await QUERY_FUNCTION[command](name=name, body=body)
    else:
        return "НИПОНЯЛ РКСОК/1.0\r\n\r\n".encode("utf-8")


async def handle_echo(reader, writer):
    data = await reader.read(100)
    status_access, data_answer_access = await check_access_request(data)
    if status_access:
        request = data.decode()
        response = await check_request(request)
        writer.write(response)
        await writer.drain()
        print("Close the connection")
        writer.close()
    else:
        writer.write(data_answer_access)
        await writer.drain()
        print('access bad')
        print("Close the connection")
        writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '0.0.0.0', 8888)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())


