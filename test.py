import platform
import subprocess

import psutil

def get_system_info():
    # Информация о системе
    system_info = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "Architecture": platform.machine(),
        "Processor": platform.processor(),
    }
    return system_info

def get_cpu_info():
    # Информация о процессоре
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "CPU Frequency": psutil.cpu_freq().current,
        "CPU Usage (%)": psutil.cpu_percent(),
    }
    return cpu_info


def get_memory_info():
    # Информация о памяти
    memory = psutil.virtual_memory()
    memory_info = {
        "Total Memory (GB)": round(memory.total / (1024 ** 3), 2),
        "Available Memory (GB)": round(memory.available / (1024 ** 3), 2),
        "Used Memory (GB)": round(memory.used / (1024 ** 3), 2),
        "Memory Usage (%)": memory.percent,
    }
    return memory_info


def get_disk_info():
    # Информация о диске
    disk = psutil.disk_usage('/')
    disk_info = {
        "Total Disk Space (GB)": round(disk.total / (1024 ** 3), 2),
        "Used Disk Space (GB)": round(disk.used / (1024 ** 3), 2),
        "Free Disk Space (GB)": round(disk.free / (1024 ** 3), 2),
        "Disk Usage (%)": disk.percent,
    }
    return disk_info

if __name__ == "__main__":

    # Путь к вашему репозиторию
    repo_path = "C:\\Users\\admin\\PycharmProjects\\test_02\\02_05"

    # Команда для выполнения коммита
    commit_command = "git commit -m 'Daily commit' --allow-empty"
    subprocess.call(commit_command, cwd=repo_path, shell=True)

    print("=== System Information ===")
    system_info = get_system_info()
    for key, value in system_info.items():
        print(f"{key}: {value}")

    print("\n=== CPU Information ===")
    cpu_info = get_cpu_info()
    for key, value in cpu_info.items():
        print(f"{key}: {value}")

    print("\n=== Memory Information ===")
    memory_info = get_memory_info()
    for key, value in memory_info.items():
        print(f"{key}: {value}")

    print("\n=== Disk Information ===")
    disk_info = get_disk_info()
    for key, value in disk_info.items():
        print(f"{key}: {value}")
