from functools import wraps
from json import loads, dumps
from colorama import init as c_init
from colorama import Fore, Style

c_init(autoreset=True)


async def get_response(**kwargs):
    """
    Отправка не сервер тела зпроса
    и получение ответа.
    """
    kwargs['writer'].write(dumps(kwargs['request']).encode('utf8'))
    result = loads(await kwargs['reader'].read(4096))
    return result
    

async def create_vm(**kwargs):
    """
    Создать новую ВМ.
    """
    ram_vol = input('Объем памяти (Гб): ')
    cpu_cores = input('Количество ядер: ')
    hd_devices = []
    hd_devices_amount = input('Количество жестких дисков: ')
    if hd_devices_amount:
        for i in range(int(hd_devices_amount)):
            memory_space = input(f'Объем памяти {i+1}-го ЖД (Гб): ')
            hd_devices.append({'memory_space': memory_space})
    request = {
                'cmd': kwargs['command'],
                'meth': 'POST',
                'body': 
                        {   
                            'prof_id': kwargs['cache']['credentials']['prof_id'],
                            'ram_vol': ram_vol,
                            'cpu_cores_amount': cpu_cores,
                            'hd_devices': hd_devices
                    }
            }
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
    if result['status'] == '201':
        print(f'{Fore.YELLOW}ВМ успешно создана.')
    else:
        print(f'{Fore.RED}Возникли трудности с созданием ВМ.')
    await kwargs['writer'].drain()


async def authorized_vms(**kwargs):
    """
    Распечатать список авторизированных ВМ.
    """
    request = {'cmd': kwargs['command'], 'meth': 'GET'}
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
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
    await kwargs['writer'].drain()


async def connected_vms(**kwargs):
    """
    Распечатать список подключенных ВМ.
    """
    request = {'cmd': kwargs['command'], 'meth': 'GET'}
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
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

    await kwargs['writer'].drain()


async def connectable_vms(**kwargs):
    """
    Распечатать список подключаемых ВМ.
    """
    request = {'cmd': kwargs['command'], 'meth': 'GET'}
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
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
    await kwargs['writer'].drain()
    

async def deactivate_vms(**kwargs):
    """
    Выйти из авторизированной ВМ.
    """
    request = {'cmd': kwargs['command'], 'meth': 'POST', 'body': {'prof_id': kwargs['cache']['credentials']['prof_id']}}
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
    if result['status'] == '201':
        print(f'{Fore.LIGHTBLUE_EX}Ваша ВМ деактивирована')
    await kwargs['writer'].drain()


async def update_vms(**kwargs):
    """
    Обновить авторизированную ВМ.
    """
    vm_id = input('ID Виртуальной машины: ')
    ram_vol = input('Объем памяти: ')
    cpu_cores = input('Количество ядер: ')
    request = {
                'cmd': kwargs['command'],
                'meth': 'PATCH',
                'id': vm_id,
                'body': {
                        'prof_id': kwargs['cache']['credentials']['prof_id'],
                        'ram_vol': ram_vol,
                        'cpu_cores_amount': cpu_cores
                    }
            }
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
    if result:
        print(f'{Fore.YELLOW}Данные виртуальной машины #{vm_id} изменены')
    else:
        print(f'{Fore.RED}Возникли трудности при изменении ВМ')
    await kwargs['writer'].drain()


async def hd_devices(**kwargs):
    """
    Распечатать список ЖД устройств.
    """
    request = {'cmd': kwargs['command'], 'meth': 'GET'}
    result = await get_response(reader=kwargs['reader'], writer=kwargs['writer'], request=request)
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
    await kwargs['writer'].drain()


async def authenticate(**kwargs):
    """
    Данная функция отвечает за процесс
    аутентификации клиента и возвращает
    результат с сервера.
    """

    # проверка 'кэша' клиента(консоли).
    # если профиля в кэше нет, то запрос авторизации
    # на сервер
    if 'credentials' not in kwargs['cache']:
        login = input('введите Ваш логин: ')
        password = input('введите пароль: ')
        kwargs['writer'].write(dumps({'cmd': 'auth', 'meth': 'POST', 'body': {'login': login, 'password': password}}).encode('utf8'))
    else:
        kwargs['writer'].write(dumps({'cmd': 'auth', 'meth': 'POST', 'body': kwargs['cache']['credentials']}).encode('utf8'))

    result = loads(await kwargs['reader'].read(255))

    if result['status'] == '404':
        print(f'{Fore.RED}Неверный логин или пароль')
        answ = input('Создать новый профиль? [y/n]: ')
        if answ == 'y':
            login = input('Введите новый логин: ')
            password = input('Введите пароль: ')
            if login != '' and password != '':
                kwargs['writer'].write(dumps({'cmd': 'new_profile', 'meth': 'POST', 'body': {'login': login, 'password': password}}).encode('utf8'))
                creation_status = loads(await kwargs['reader'].read(255))
                if creation_status['status'] == '201':
                    # По мере создания нового профиля его данные поступают в кэш клиента
                    kwargs['cache']['credentials'] = {'prof_id': creation_status['prof_id'], 'login': login, 'password': password}
                    return 'success'
                elif creation_status['status'] == '400':
                    return 'not created'
        return 'rejected'
    
    elif result['status'] == '401':
        return 'unauthorized'
        
    elif result['status'] == '200':
        # если клиент в списке аутентифицированных,
        # сервер достаёт профиль из своего кэша
        kwargs['cache']['credentials'] = result['credentials']
        return 'success'
    

# фабрика команд
command_factory = {
    '1': create_vm,
    '2': connected_vms,
    '3': authorized_vms,
    '4': connectable_vms,
    '5': deactivate_vms,
    '6': update_vms,
    '7': hd_devices
}