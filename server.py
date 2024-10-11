import asyncio
import views
from json import loads, dumps


vm_manager = views.VMManager()

# фабрика методов для обработчика запр-ов
actions = {
    '1': vm_manager.add_new_vm,
    '2': vm_manager.list_connected_vms,
    '3': vm_manager.list_authorized_vms,
    '4': vm_manager.list_ever_connected_vms,
    '5': vm_manager.logout_vm,
    '6': vm_manager.update_vm_data,
    '7': vm_manager.list_hard_drives
}


async def handle_requests(reader, writer):
    """
    Обработка запросов от клиентов
    и выполнение соответствующих
    методов.
    """
    address = writer.get_extra_info('peername')
    print(f'Connection from {address} was initialized')
    while True:
        request_coroutine = await reader.read(255)
        request = loads(request_coroutine)
        result = None
        if request['cmd'] in actions:
            if request['meth'] == 'POST':
                result = await actions[request['cmd']](**request['body'])
            elif request['meth'] == 'DELETE':
                result = await actions[request['cmd']](**request['id'])
            elif request['meth'] == 'PATCH':
                result = await actions[request['cmd']](**request['body'])
            elif request['meth'] == 'GET':
                result = await actions[request['cmd']]()
            else:
                result = dumps({'message': 'method not allowed'})
            writer.write(dumps(result).encode('utf8'))
        else:
            writer.write(dumps({'message': 'bad request'}).encode('utf8'))
            

async def run_server():
    """
    Поднятие сервера.
    """
    s = await asyncio.start_server(handle_requests, '127.0.0.1', 8000)
    addr = s.sockets[0].getsockname()
    print(f'server started on {addr}')
    print('Listening for other sockets...')

    async with s:
        await s.serve_forever()


if __name__ == '__main__':
    asyncio.run(run_server())