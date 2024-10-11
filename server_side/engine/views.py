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
    def __init__(self):
        self.connected_vms: dict[str, VirtualMachine] = {}
        self.authorized_vms: dict[str, VirtualMachine]= {}

    async def add_new_vm(self, **body) -> bool:
        return body

    async def list_connected_vms(self) -> List[VirtualMachine]:
        return 'Listing the connected vms'

    async def list_authorized_vms(self) -> List[VirtualMachine]:
        return 'list_authorized_vms'

    async def list_ever_connected_vms(self) -> List[VirtualMachine]:
        return 'list_ever_connected_vms'

    async def logout_vm(self, pk: str) -> bool:
        del self.authorized_vms[pk]
        return pk in self.authorized_vms

    async def list_hard_drives(self) -> List[HardDrive]:
        return 'list_hard_drives'

    async def update_vm_data(self) -> VirtualMachine:
        return 'update_vm_data'