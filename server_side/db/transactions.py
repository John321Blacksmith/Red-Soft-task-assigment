import asyncpg
from .queries import (
                        create_db, create_tables,
                        add_new_vm, add_hd_device,
                        select_vms, update_vm,
                        select_hds, select_connectable_vms, select_test
                    )


class DBManager:
    """
    Менеджер содержит API для
    работы с БД.
    """
    def __init__(self, **conf):
        self.conf = conf
        self.url = f'postgresql://{self.conf['user']}:{self.conf['password']}@{self.conf['host']}/{self.conf['db']}'

    async def create_db(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(create_db)
        await conn.close()
        return result

    async def create_tables(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(create_tables)
        await conn.close()
        return result

    async def create_vm(self, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(add_new_vm, body['vm_id'], body['ram_vol'], body['cpu_cores'])
        await conn.close()
        return result
            
    async def create_hd(self, vm_id: int, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(add_hd_device, body['hd_id'], vm_id, body['memory_space'])
        await conn.close()
        return result
    
    async def select_vms(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_vms)
        await conn.close()
        return result
        
    async def select_hard_drives(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_hds)
        await conn.close()
        return result
        
    async def update_vm(self, pk: int, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(update_vm, body['ram_vol'], body['cpu_cores_amount'], pk)
        await conn.close()
        return result

    async def select_connectable_vms(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_connectable_vms)
        await conn.close()
        return result
    
    async def select_test_data(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_test)
        return result