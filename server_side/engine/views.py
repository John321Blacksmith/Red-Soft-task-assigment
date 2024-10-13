import sys
sys.path.append('../')
from typing import List
from db.transactions import DBManager
from models import HardDrive, VirtualMachine, Profile, Connection


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

    async def list_vms(self) -> List[VirtualMachine]:
        queryset = await self.db_manager.select_vms()
        if queryset:
            return {
                'message': '200',
                'results': [
                        {
                            'id': r['vm_id'],
                            'ram_vol': r['ram_vol'],
                            'cpu': r['cpu_cores_amount']
                    }
                    for r in queryset
                ]}
        return {'message': '404'}

    async def list_authorized_vms(self) -> List[VirtualMachine]:
        queryset = await self.db_manager.select_authorized_vms()
        result = [
                {
                    'vm_id': r['vm_id'],
                    'ram_vol': r['ram_vol'],
                    'cpu_cores_amount': r['cpu_cores_amount']
                } for r in queryset
            ]
        return {'status': '200', 'results': result}

    async def list_connected_vms(self)-> List[VirtualMachine]:
        queryset = await self.db_manager.select_connected_vms()
        if queryset:
            result = [
                    {
                        'vm_id': r['vm_id'],
                        'ram_vol': r['ram_vol'],
                        'cpu_cores_amount': r['cpu_cores_amount']
                    } for r in queryset
                ]
            return {'status': '200', 'results': result}
        return {'status': '404'}

    async def list_connectable_vms(self) -> List[VirtualMachine]:
        queryset = await self.db_manager.select_connectable_vms()
        if queryset:
            result = [
                    {
                        'vm_id': r['vm_id'],
                        'ram_vol': r['ram_vol'],
                        'cpu_cores_amount': r['cpu_cores_amount']
                    } for r in queryset
                ]
            return {'status': '200', 'results': result}
        return {'status': '404'}

    async def logout_vm(self, **body) -> bool:
        result = await self.db_manager.logout_vm(**body)
        if result:
            return {'status': '201'}
        return {'status': '400'}

    async def list_hard_drives(self) -> List[HardDrive]:
        queryset = await self.db_manager.select_hard_drives()
        if queryset:
            result = [
                {
                    'hd_id': r['hd_id'],
                    'vm_id': r['vm_id'],
                    'memory_space': r['memory_space']

                } for r in queryset
            ]
            print(result)
            return {'status': '200', 'results': result}
        return {'status': '404'}

    async def authentificate(self, **body):
        if body['login'] not in self.authorized_profiles:
            obj = await self.db_manager.select_profile(body['login'])
            if obj:
                result = dict(obj)
                if body['password'] == result['password']:
                    await self.db_manager.set_connection_state(**{'state': 'active', 'prof_id': result['prof_id']})
                    self.authorized_profiles[body['login']] = result
                    return {'status': '200', 'credentials': {'prof_id': result['prof_id'], 'login': result['login'], 'password': result['password']}}
                return {'status': '404'}
            return {'status': '404'} # redirect to profile creation
        else:
            if body['password'] != self.authorized_profiles[body['login']]['password']:
                return {'status': '401'}
        return {'status': '200', 'credentials': self.authorized_profiles[body['login']]}
        
    async def setup_storage(self):
        result = await self.db_manager.create_db()
        if result:
            return {'status': '201'}
        return {'status': '400'}
    async def create_tables(self):
        result = await self.db_manager.create_tables()
        if result:
            return {'status': '201'}
        return {'status': '400'}

    async def add_new_vm(self, **body) -> bool:
        result = await self.db_manager.create_vm(**body)
        if result:
            return {'status': '201'}
        return {'status': '400'}

    async def add_new_hd(self, **body) -> bool:
        result = await self.db_manager.create_hd(**body)
        if result:
            return {'status': '201'}
        return {'status': '400'}
        
    async def update_vm_data(self, vm_id: int, **body):
        result = await self.db_manager.update_vm(vm_id, **body)
        if result:
            return {'status': '201'}
        return {'status': '400'}
        
    async def add_profile(self, **body):
        result = await self.db_manager.create_profile(**body)
        if result:
            return {'status': '201', 'prof_id': result['prof_id']}
        return {'status': '400'}