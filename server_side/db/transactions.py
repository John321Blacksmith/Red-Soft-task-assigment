import asyncpg
from .queries import (
                        create_db, create_tables,
                        create_new_vm, create_hd_device,
                        select_authorized_vms, update_vm,
                        select_hds, select_connectable_vms,
                        create_profile, select_profile,
                        select_vms, select_connected_vms,
                        set_conn_state, create_connection
                    )

class DBManager:
    """
    Менеджер содержит API для
    работы с БД.
    """
    def __init__(self, **conf):
        self.conf = conf
        self.url = f'postgresql://{self.conf['user']}:{self.conf['password']}@{self.conf['host']}:{self.conf['port']}/{self.conf['db']}'

    async def create_db(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(create_db)
        await conn.close()
        return result

    async def create_profile(self, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetchrow(create_profile, body['login'], body['password'])
        await conn.close()
        return result

    async def create_tables(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(create_tables)
        await conn.close()
        return result

    async def create_vm(self, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = []
        new_vm = await conn.fetchrow(create_new_vm, int(body['ram_vol']), int(body['cpu_cores_amount']))
        if new_vm:
            for i in range(len(body['hd_devices'])):
                r = await conn.execute(create_hd_device, int(new_vm['vm_id']), int(body['hd_devices'][i]['memory_space']))
                if r:
                    result.append(r)
            await conn.execute(create_connection, int(new_vm['vm_id']), int(body['prof_id']))
        await conn.close()
        return result
    
    async def set_connection_state(self, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(set_conn_state, body['state'], int(body['prof_id']))
        await conn.close()
        return result

            
    async def create_hd(self, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(create_hd_device, int(body['vm_id']), int(body['hd_id']), int(body['memory_space']))
        await conn.close()
        return result
    
    async def update_vm(self, vm_id: int, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(update_vm, int(body['ram_vol']), int(body['cpu_cores_amount']), int(vm_id))
        await conn.close()
        return result
        
    async def logout_vm(self, **body):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.execute(set_conn_state, 'inactive', int(body['prof_id']))
        await conn.close()
        return result
    
    async def select_vms(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_vms)
        await conn.close()
        return result
    
    async def select_authorized_vms(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_authorized_vms)
        await conn.close()
        return result
        
    async def select_hard_drives(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_hds)
        await conn.close()
        return result

    async def select_connectable_vms(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_connectable_vms)
        await conn.close()
        return result
    
    async def select_connected_vms(self):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetch(select_connected_vms)
        await conn.close()
        return result
    
    async def select_profile(self, login: str):
        conn = await asyncpg.connect(dsn=self.url)
        result = await conn.fetchrow(select_profile, login)
        await conn.close()
        return result