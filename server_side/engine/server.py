import asyncio
import views
from time import sleep
from json import loads, dumps
from colorama import init as c_init
from colorama import Fore

c_init(autoreset=True)

def get_env_vars() -> dict[str, str|None]:
    """
    Загрузка переменных среды
    для конфигурирования БД.
    """
    from os import getenv
    from dotenv import load_dotenv

    load_dotenv()

    db_configs = {
            'user': getenv('PGUSER'),
            'password': getenv('PGPASSWORD'),
            'host': getenv('PGHOST'),
            'port': getenv('PGPORT'),
            'db': getenv('PGDATABASE')
        }

    return db_configs


vm_manager = views.VMManager(**get_env_vars())

# фабрика методов для обработчика запр-ов
actions = {
    '1': vm_manager.add_new_vm,
    '2': vm_manager.list_vms,
    '3': vm_manager.list_authorized_vms,
    '4': vm_manager.list_connectable_vms,
    '5': vm_manager.logout_vm,
    '6': vm_manager.update_vm_data,
    '7': vm_manager.list_hard_drives,
    't': vm_manager.list_test_data
}


async def handle_requests(reader, writer):
    """
    Обработка запросов от клиентов
    и выполнение соответствующих
    методов.
    """
    addr = writer.get_extra_info('peername')
    print(f'{Fore.GREEN}Connection from {Fore.YELLOW}{addr[0]}:{addr[1]}' + ' ' + f'{Fore.GREEN}was initialized')
    while True:
        request_coroutine = await reader.read(255)
        request = loads(request_coroutine)
        result = None
        if request['cmd'] in actions:
            if request['meth'] == 'POST':
                result = await actions[request['cmd']](**request['body'])
            elif request['meth'] == 'DELETE':
                result = await actions[request['cmd']](**request['pk'])
            elif request['meth'] == 'PATCH':
                result = await actions[request['cmd']](**request['body'])
            elif request['meth'] == 'GET':
                result = await actions[request['cmd']]()
            else:
                result = dumps({'message': 'method not allowed'})
            writer.write(dumps(result).encode('utf8'))
            await writer.drain()
        else:
            writer.write(dumps({'message': 'bad request'}).encode('utf8'))
            await writer.drain()


async def run_server():
    """
    Поднятие сервера.
    """
    db_option = input('Do you need to set up DB? [y/n] ')
    if db_option == 'y':
        result = await vm_manager.setup_storage()
        if result:
            print(f'{Fore.LIGHTBLUE_EX}Database initialized...')
    sleep(1)
    s = await asyncio.start_server(handle_requests, '127.0.0.1', 8000)
    addr = s.sockets[0].getsockname()
    print(f'Server started on {Fore.YELLOW}{addr[0]}:{addr[1]}')
    sleep(1)
    print('Listening for other sockets...')

    async with s:
        await s.serve_forever()


if __name__ == '__main__':
    asyncio.run(run_server())