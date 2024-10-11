from typing import List


class HardDrive:
    """
    Модель представляет объект
    жесткого диска.
    """
    def __init__(self, hd_id: int, memory_space: float) -> None:
        self.hd_id = hd_id
        self.memory_space = memory_space

class VirtualMachine:
    """
    Модель представляет объект
    Виртуальной Машины.
    """
    def __init__(self, vm_id: int, ram_vol: float, cpu_cores: int)-> None:
        self.vm_id = vm_id
        self.ram_vol = ram_vol
        self.cpu_cores = cpu_cores
        self.hd_devices: List[HardDrive]
