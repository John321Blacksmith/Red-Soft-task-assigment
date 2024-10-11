import sys
sys.path.append('../')
from typing import List
from db.transactions import DBManager
from models import HardDrive, VirtualMachine


class VMManager:
    """
    Даный менеджер содержит
    методы, по которым сторонний
    socket-клиент взаимодействует с 
    хранилищем.
    """
    def __init__(self, **conf):
        self.db_manager = DBManager(**conf)
        self.connected_vms: dict[str, VirtualMachine] = {}
        self.authorized_vms: dict[str, VirtualMachine]= {}

    async def setup_storage(self):
        result = await self.db_manager.create_db()
        if result:
            result = await self.db_manager.create_tables()
            return result

    async def add_new_vm(self, **body) -> bool:
        return await self.db_manager.create_vm(**body)
    
    async def add_new_hd(self, vm_id: int, **body) -> bool:
        return await self.db_manager.create_hd(vm_id, **body)

    async def list_vms(self) -> List[VirtualMachine]:
        return await self.db_manager.select_vms()

    async def list_authorized_vms(self) -> List[VirtualMachine]:
        return self.authorized_vms

    async def list_connectable_vms(self) -> List[VirtualMachine]:
        return await self.db_manager.select_connectable_vms()

    async def logout_vm(self, pk: str) -> bool:
        if pk in self.authorized_vms:
            del self.authorized_vms[pk]
        return pk in self.authorized_vms

    async def list_hard_drives(self) -> List[HardDrive]:
        return await self.db_manager.select_hard_drives()

    async def update_vm_data(self, vm_id: int, **body) -> VirtualMachine:
        return await self.db_manager.update_vm(vm_id, **body)
    
    async def list_test_data(self):
        result = await self.db_manager.select_test_data()
        return [{'f_name': dict(r)['first_name']} for r in result]