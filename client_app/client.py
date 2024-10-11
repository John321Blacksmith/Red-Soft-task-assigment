import asyncio
from json import dumps, loads


async def run_client():
    """
    Запуск клиента и взаимодействие
    с серверным API через консоль.
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8000)
    while True:
        print(
            """
                Панель управления виртуальных машин\n.
                Для выполнения следующих действий\n,
                используйте следующие команды:\n

                1 - добавление новой ВМ в храниище\n
                2 - список подключенных ВМ\n
                3 - список авторизованных ВМ\n
                4 - история подключений ВМ\n
                5 - выйти из авторизирванной ВМ\n
                6 - обновить данные в авторизированной ВМ\n
                7 - список всех жестких дисков\n
                q - выйти
            """
        )
        command = input('> ').strip()

        if command == '1':
            ram_vol = input('Объем памяти: ')
            cpu_cores = input('Количество ядер: ')
            hd_devices = []
            hd_devices_amount = input('Количество жестких дисков: ')
            if hd_devices_amount:
                for i in range(int(hd_devices_amount)):
                    memory_space = input(f'Объем памяти {i+1}-го ЖД: ')
                    hd_devices.append({'mem_space': memory_space})
            request = {
                        'cmd': command,
                        'meth': 'POST',
                        'body': 
                                {
                                    'ram_vol': ram_vol,
                                    'cpu_cores': cpu_cores,
                                    'hd_devices': hd_devices
                            }
                    }
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()

        elif command == '2':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()

        elif command == '3':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()

        elif command == '4':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()

        elif command == '5':
            request = {'cmd': command, 'meth': 'DELETE'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()

        elif command == '6':
            vm_id = input('ID Виртуальной машины: ')
            ram_vol = input('Объем памяти: ')
            cpu_cores = input('Количество ядер: ')
            hd_devices = []
            hd_devices_amount = input('Количество жестких дисков: ')
            if hd_devices_amount:
                for i in range(int(hd_devices_amount)):
                    memory_space = input(f'Объем памяти {i+1}-го ЖД: ')
                    hd_devices.append({'mem_space': memory_space})

            request = {
                        'cmd': command,
                        'meth': 'PATCH',
                        'id': vm_id,
                        'body': {
                                'ram_vol': ram_vol,
                                'cpu_cores': cpu_cores,
                                'hd_devices': hd_devices,
                            }
                    }
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()

        elif command == '7':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            print(f'Server response: {result}')
            await writer.drain()
        
        elif command == 'q':
            print('Exiting...')
            break
        else:
            print('Invalid command')



if __name__ == '__main__':
    asyncio.run(run_client())
