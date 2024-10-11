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
