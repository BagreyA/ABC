import platform
import psutil
import socket
import subprocess

def get_os_info():
    os_name = platform.system()
    os_version = platform.version()
    print(f"ОС: {os_name}")
    print(f"Версия: {os_version}")

def get_kernel_info():
    kernel_version = platform.release()
    architecture = platform.architecture()[0]
    print(f"Версия ядра: {kernel_version}")
    print(f"Архитектура ядра: {architecture}")

def get_cpu_info():
    cpu_info = psutil.cpu_freq()
    num_cores = psutil.cpu_count(logical=False)
    model = platform.processor()
    print(f"Модель процессора: {model}")
    print(f"Частота: {cpu_info.max} MHz")
    print(f"Количество ядер: {num_cores}")

def get_cache_info():
    try:
        cache_info = subprocess.check_output("lscpu", text=True)
        cache_lines = [line for line in cache_info.splitlines() if "cache" in line and "vulnerable" not in line]

        if not cache_lines:
            print("Информация о кэшах не найдена или все строки содержат уязвимости.")
            return

        print("Размер кэш-памяти:")
        for line in cache_lines:
            print(line)

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении информации о кэшах: {e}")

def get_memory_info():
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 * 1024)  # MB
    available_memory = memory.available / (1024 * 1024)  # MB
    used_memory = memory.used / (1024 * 1024)  # MB
    print(f"Доступный размер: {available_memory:.2f} MB")
    print(f"Общий размер ОП: {total_memory:.2f} MB")
    print(f"Использованный размер: {used_memory:.2f} MB")

def get_network_info():
    for interface, addrs in psutil.net_if_addrs().items():
        ip_addr = None
        mac_addr = None
        for addr in addrs:
            if addr.family == socket.AF_INET:  # Используем socket.AF_INET вместо psutil.AF_INET
                ip_addr = addr.address
            elif addr.family == socket.AF_PACKET:  # Для MAC-адреса в Linux используем socket.AF_PACKET
                mac_addr = addr.address
        if ip_addr or mac_addr:
            print(f"Сетевой интерфейс: {interface}")
            print(f"IP адрес: {ip_addr if ip_addr else 'Неизвестно'}")
            print(f"MAC адрес: {mac_addr if mac_addr else 'Неизвестно'}")
            try:
                net_speed = psutil.net_if_stats()[interface].speed
                print(f"Скорость сети: {net_speed} Mбит/с\n")
            except KeyError:
                print("Скорость сети: Неизвестно\n")

def get_disk_info():
    for partition in psutil.disk_partitions():
        mountpoint = partition.mountpoint
        fs_type = partition.fstype
        try:
            usage = psutil.disk_usage(mountpoint)
            total_size = round(usage.total / (1024 * 1024 * 1024), 2)
            used_space = round(usage.used / (1024 * 1024 * 1024), 2)
            free_space = round(usage.free / (1024 * 1024 * 1024), 2)
            print(f"Точка монтирования: {mountpoint}")
            print(f"Файловая система: {fs_type}")
            print(f"Общий размер: {total_size} GB")
            print(f"Использовано: {used_space} GB")
            print(f"Свободно: {free_space} GB\n")
        except PermissionError:
            print(f"Нет доступа к разделу {mountpoint}\n")

if __name__ == "__main__":
    get_os_info()
    get_kernel_info()
    print("\nИнформация о процессоре:")
    get_cpu_info()
    get_cache_info()
    print("\nИнформация о размере оперативной памяти:")
    get_memory_info()
    print("\nСетевой интерфейс:")
    get_network_info()
    print("\nИнформация о системных разделах:")
    get_disk_info()