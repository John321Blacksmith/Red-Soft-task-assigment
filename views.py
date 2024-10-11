from __future__ import annotations
from typing import List
from db.transactions import DBManager


class VMManager:
    """
    Даный менеджер содержит
    методы, по которым сторонний
    socket-клиент взаимодействует с 
    хранилищем.
    """
    def __init__(self):
        self.connected_vms: dict[str, int|list[dict]] = {}
        self.authorized_vms: dict[str, int|list[dict]]= {}

    async def add_new_vm(self, **body)->None:
        return body

    async def list_connected_vms(self):
        return 'Listing the connected vms'

    async def list_authorized_vms(self):
        return 'list_authorized_vms'

    async def list_ever_connected_vms(self):
        return 'list_ever_connected_vms'

    async def logout_vm(self, pk: str):
        del self.authorized_vms[pk]
        return pk in self.authorized_vms

    async def list_hard_drives(self):
        return 'list_hard_drives'

    async def update_vm_data(self):
        return 'update_vm_data'