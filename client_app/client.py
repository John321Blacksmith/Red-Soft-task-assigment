import sys
import asyncio
from json import dumps, loads
from colorama import init as c_init
from colorama import Fore, Style
from commands import command_factory, authenticate


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
        if command in command_factory:
            await command_factory[command](reader=reader, writer=writer, command=command, cache=cache)
        
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


async def run_client():
    """
    Запуск клиента и взаимодействие
    с серверным API через консоль.
    """
    reader, writer = await asyncio.open_connection('127.0.0.1', 8000)

    login_result = await authenticate(reader=reader, writer=writer, cache=cache)
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
