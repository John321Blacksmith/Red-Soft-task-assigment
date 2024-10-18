import sys
sys.path.append('../')
from typing import List
from functools import wraps
from db.transactions import DBManager
from .models import HardDrive, VirtualMachine, Profile, Connection
from db.exceptions import DBError


class VMManager:
    """
    Даный менеджер содержит
    методы, по которым сторонний
    socket-клиент взаимодействует с 
    хранилищем.
    Менеджер возвращает
    сериализуемые объекты.
    """
    def __init__(self, **conf):
        self.db_manager = DBManager(**conf)
        self.authorized_profiles: dict[str, Profile] = {}

    def mutation(funct):
        @wraps(funct)
        async def wrapper(self, *args, **kwargs):
            try:
                result = await funct(self, *args, **kwargs)
            except DBError:
                return {'status': '400'}
            else:
                return {'status': '201', 'result': result}
        return wrapper

    def query(funct):
        @wraps(funct)
        async def wrapper(self, *args, **kwargs):
            try:
                result = await funct(self, *args, **kwargs)
            except DBError:
                return {'status': '404'}
            else:
                return {'status': '200', 'results': result}
        return wrapper
            
    @query
    async def list_vms(self) -> List[VirtualMachine]:
        """
        Сериализация списка всех ВМ.
        """
        queryset = await self.db_manager.select_vms()
        results = [
                    {
                        'id': r['vm_id'],
                        'ram_vol': r['ram_vol'],
                        'cpu': r['cpu_cores_amount'],
                        'overall_hd_space': r['overall_hd_space']
                    } for r in queryset
                ]
        return results

    @query
    async def list_authorized_vms(self) -> List[VirtualMachine]:
        """
        Сериализация списка авторизированных ВМ.
        """
        queryset = await self.db_manager.select_authorized_vms()
        results = [
                {
                    'vm_id': r['vm_id'],
                    'ram_vol': r['ram_vol'],
                    'cpu_cores_amount': r['cpu_cores_amount'],
                    'overall_hd_space': r['overall_hd_space']
                } for r in queryset
            ]
        return results

    @query
    async def list_connected_vms(self)-> List[VirtualMachine]:
        """
        Сериализация списка подключненных ВМ
        """
        queryset = await self.db_manager.select_connected_vms()
        result = [
                    {
                        'vm_id': r['vm_id'],
                        'ram_vol': r['ram_vol'],
                        'cpu_cores_amount': r['cpu_cores_amount'],
                        'overall_hd_space': r['overall_hd_space']
                    } for r in queryset
                ]
        return result

    @query
    async def list_connectable_vms(self) -> List[VirtualMachine]:
        """
        Сериализация списка подключаемых ВМ.
        """
        queryset = await self.db_manager.select_connectable_vms()
        
        result = [
                    {
                        'vm_id': r['vm_id'],
                        'ram_vol': r['ram_vol'],
                        'cpu_cores_amount': r['cpu_cores_amount'],
                        'overall_hd_space': r['overall_hd_space']
                    } for r in queryset
                ]
        return result

    @mutation
    async def logout_vm(self, **body) -> bool:
        """
        Процесс выхода ВМ из списка подключенных.
        """
        result = await self.db_manager.logout_vm(**body)
        return result
    
    @query
    async def list_hard_drives(self) -> List[HardDrive]:
        """
        Сериализация списка всех ЖД.
        """
        queryset = await self.db_manager.select_hard_drives()
        result = [
                {
                    'hd_id': r['hd_id'],
                    'vm_id': r['vm_id'],
                    'memory_space': r['memory_space']

                } for r in queryset
            ]
        return result

    async def authentificate(self, **body):
        """
        Процесс верификации профиля
        """
        if body['login'] not in self.authorized_profiles:
            obj = await self.db_manager.select_profile(body['login'])
            if obj:
                result = dict(obj)
                if body['password'] == result['password']:
                    await self.db_manager.set_connection_state(**{'state': 'active', 'prof_id': result['prof_id']})
                    self.authorized_profiles[body['login']] = result
                    return {
                        'status': '200',
                        'credentials': {
                            'prof_id': result['prof_id'],
                            'login': result['login'],
                            'password': result['password']
                            }
                        }
                return {'status': '404'}
            return {'status': '404'} # redirect to profile creation
        else:
            if body['password'] != self.authorized_profiles[body['login']]['password']:
                return {'status': '401'}
        return {'status': '200', 'credentials': self.authorized_profiles[body['login']]}
        
    @mutation
    async def setup_storage(self):
        """
        Процесс создания базы данных
        на Postgres сервере.
        """
        result = await self.db_manager.create_db()
        return result
    
    @mutation
    async def create_tables(self):
        """
        Процесс создания всех таблиц.
        """
        result = await self.db_manager.create_tables()
        return result

    @mutation
    async def add_new_vm(self, **body):
        """
        Процесс добавления новой ВМ.
        """
        result = await self.db_manager.create_vm(**body)
        return result

    @mutation
    async def add_new_hd(self, **body):
        """
        Процесс добавления нового ЖД
        с привязкой к ВМ.
        """
        result = await self.db_manager.create_hd(**body)
        return result
        
    @mutation
    async def update_vm_data(self, vm_id: int, **body):
        """
        Процесс обновления авторизированной
        ВМ.
        """
        result = await self.db_manager.update_vm(vm_id, **body)
        return result
        
    @mutation
    async def add_profile(self, **body):
        """
        Процесс создания нового
        профиля.
        """
        result = await self.db_manager.create_profile(**body)
        return result
    
    