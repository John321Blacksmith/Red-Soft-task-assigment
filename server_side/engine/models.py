from typing import List


class HardDrive:
    """
    Модель представляет объект
    жесткого диска.
    """
    hd_id: int
    memory_space: int

class VirtualMachine:
    """
    Модель представляет объект
    Виртуальной Машины.
    """
    vm_id: int
    ram_vol: int
    cpu_cores: int
    hd_devices: List[HardDrive]


class Profile:
    """
    Модель представляет объект
    Профиля клиента.
    """
    prof_id: int
    login: str
    password: str


class Connection:
    """
    Модель представляет объект
    клиентского подключения.
    """
    conn_id: int
    v_machine: VirtualMachine
    profile: Profile
    status: str

