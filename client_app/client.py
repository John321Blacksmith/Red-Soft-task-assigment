import sys
import asyncio
from json import dumps, loads
from colorama import init as c_init
from colorama import Fore, Style


c_init(autoreset=True)

# объект содержит
# данные профиля клиента
cache = {}

BOARD = f"""
{Fore.LIGHTCYAN_EX}Панель управления виртуальных машин.
Для выполнения следующих действий,
используйте следующие команды:

    {Fore.YELLOW}1 - Добавление новой ВМ в храниище
    2 - Список подключенных ВМ
    3 - Список авторизованных ВМ
    4 - Список подключаемых ВМ
    5 - Выйти из авторизирванной ВМ
    6 - Обновить данные в авторизированной ВМ
    7 - Список всех жестких дисков

    {Fore.LIGHTYELLOW_EX}--help - {Fore.YELLOW}Справочник всех команд
            
    {Fore.MAGENTA}q - выйти
"""


async def administer_vms(reader, writer):
    """
    Данная функция отвечает за
    взаимодействие консоли с
    ВМ-менеджером.
    """
    while True:
        command = input('> ').strip()
        if command == '1':
            ram_vol = input('Объем памяти (Гб): ')
            cpu_cores = input('Количество ядер: ')
            hd_devices = []
            hd_devices_amount = input('Количество жестких дисков: ')
            if hd_devices_amount:
                for i in range(int(hd_devices_amount)):
                    memory_space = input(f'Объем памяти {i+1}-го ЖД (Гб): ')
                    hd_devices.append({'memory_space': memory_space})
            request = {
                        'cmd': command,
                        'meth': 'POST',
                        'body': 
                                {   
                                    'prof_id': cache['credentials']['prof_id'],
                                    'ram_vol': ram_vol,
                                    'cpu_cores_amount': cpu_cores,
                                    'hd_devices': hd_devices
                            }
                    }
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            if result['status'] == '201':
                print(f'{Fore.YELLOW}ВМ успешно создана.')
            else:
                print(f'{Fore.RED}Возникли трудности с созданием ВМ.')
            await writer.drain()

        # all connected virtual machines
        elif command == '2':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(10000))
            if result['status'] == '200':
                if len(result['results']):
                    print('------------------------------')
                    print(f'Найдено подключенных ВМ: {Fore.YELLOW}{len(result['results'])}')
                    print('------------------------------')
                    for i in range(len(result['results'])):
                        print()
                        print(result['results'][i])
            else:
                print(f'{Fore.LIGHTBLUE_EX}Список пока пуст.')

            await writer.drain()

        # all authorized virtual machines
        elif command == '3':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(10000))
            if result['status'] == '200':
                if len(result['results']):
                    print('------------------------------')
                    print(f'Найдено авторизированных ВМ: {Fore.YELLOW}{len(result['results'])}')
                    print('------------------------------')
                    for i in range(len(result['results'])):
                        print()
                        print(result['results'][i])
            else:
                print(f'{Fore.LIGHTBLUE_EX}Список пока пуст.')
            await writer.drain()

        # all connectable virtual machines
        elif command == '4':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(10000))
            if result['status'] == '200':
                if len(result['results']):
                    print('------------------------------')
                    print(f'Найдено подключаемых ВМ: {Fore.YELLOW}{len(result['results'])}')
                    print('------------------------------')
                    for i in range(len(result['results'])):
                        print()
                        print(result['results'][i])
            else:
                print(f'{Fore.LIGHTBLUE_EX}Список пока пуст.')
            await writer.drain()
    
        # logout virtual machine
        elif command == '5':
            request = {'cmd': command, 'meth': 'POST', 'body': {'prof_id': cache['credentials']['prof_id']}}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            if result['status'] == '201':
                print(f'{Fore.LIGHTBLUE_EX}Ваша ВМ деактивирована')
            await writer.drain()

        # update an authorized virtual machine
        elif command == '6':
            vm_id = input('ID Виртуальной машины: ')
            ram_vol = input('Объем памяти: ')
            cpu_cores = input('Количество ядер: ')
            request = {
                        'cmd': command,
                        'meth': 'PATCH',
                        'id': vm_id,
                        'body': {
                                'prof_id': cache['credentials']['prof_id'],
                                'ram_vol': ram_vol,
                                'cpu_cores_amount': cpu_cores
                            }
                    }
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(255))
            if result:
                print(f'{Fore.YELLOW}Данные виртуальной машины #{vm_id} изменены')
            else:
                print(f'{Fore.RED}Возникли трудности при изменении ВМ')
            await writer.drain()

        # get all hard drives
        elif command == '7':
            request = {'cmd': command, 'meth': 'GET'}
            writer.write(dumps(request).encode('utf8'))
            result = loads(await reader.read(10000))
            if result['status'] == '200':
                if len(result['results']):
                    print('------------------------------')
                    print(f'Найдено HD-дисков: {Fore.YELLOW}{len(result['results'])}')
                    print('------------------------------')
                    for i in range(len(result['results'])):
                        print()
                        print(result['results'][i])
            else:
                print(f'{Fore.LIGHTBLUE_EX}Список пока пуст.')
            await writer.drain()
        
        # print all commands
        elif command == '--help':
            print(BOARD)

        # exit the console
        elif command == 'q':
            print(f'{Fore.MAGENTA}Exiting...')
            return 'exit'
        else:
            print(f'{Fore.RED}\'{command}\' {Style.RESET_ALL}не является командой.')
            print(f'Используйте {Fore.LIGHTYELLOW_EX}\'--help\' {Style.RESET_ALL}для просмотра команд.')


async def authenticate(reader, writer):
    """
    Данная функция отвечает за процесс
    аутентификации клиента и возвращает
    результат с сервера.
    """

    # проверка 'кэша' клиента(консоли).
    # если профиля в кэше нет, то запрос авторизации
    # на сервер
    if 'credentials' not in cache:
        login = input('введите Ваш логин: ')
        password = input('введите пароль: ')
        writer.write(dumps({'cmd': 'auth', 'meth': 'POST', 'body': {'login': login, 'password': password}}).encode('utf8'))
    else:
        writer.write(dumps({'cmd': 'auth', 'meth': 'POST', 'body': cache['credentials']}).encode('utf8'))

    result = loads(await reader.read(255))

    if result['status'] == '404':
        print(f'{Fore.RED}Неверный логин или пароль')
        answ = input('Создать новый профиль? [y/n]: ')
        if answ == 'y':
            login = input('Введите новый логин: ')
            password = input('Введите пароль: ')
            if login != '' and password != '':
                writer.write(dumps({'cmd': 'new_profile', 'meth': 'POST', 'body': {'login': login, 'password': password}}).encode('utf8'))
                creation_status = loads(await reader.read(255))
                if creation_status['status'] == '201':
                    # По мере создания нового профиля его данные поступают в кэш клиента
                    cache['credentials'] = {'prof_id': creation_status['prof_id'], 'login': login, 'password': password}
                    return 'success'
                elif creation_status['status'] == '400':
                    return 'not created'
        return 'rejected'
    
    elif result['status'] == '401':
        return 'unauthorized'
        
    elif result['status'] == '200':
        # если клиент в списке аутентифицированных,
        # сервер достаёт профиль из своего кэша
        cache['credentials'] = result['credentials']
        return 'success'


async def run_client():
    """
    Запуск клиента и взаимодействие
    с серверным API через консоль.
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8000)

    login_result = await authenticate(reader, writer)
    if login_result == 'success':
        print(f'{Fore.GREEN}Здравствуйте, {Fore.YELLOW}{cache['credentials']['login']}')
        print(BOARD)
        log = await administer_vms(reader, writer)
        if log == 'exit':
            sys.exit()
    else:
        if login_result == 'rejected':
            print(f'{Fore.RED}Процесс входа не был выполнен.')
        elif login_result == 'unauthorized':
            print(f'{Fore.RED}Ваши учётные данные были изменены.')
        elif login_result == 'not created':
            print(f'{Fore.RED}Возникли трудности с созданием профиля.')
        sys.exit()


if __name__ == '__main__':
    asyncio.run(run_client())
