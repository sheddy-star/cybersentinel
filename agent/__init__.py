import platform
import psutil
import socket
from datetime import datetime


def get_system_info():
    """Collect basic information about the computer."""

    try:
        system_info = {
            "hostname": socket.gethostname(),
            "operating_system": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "logical_processors": psutil.cpu_count(logical=True),
            "cpu_usage": psutil.cpu_percent(interval=1),
            "total_memory": round(
                psutil.virtual_memory().total / (1024 ** 3), 2
            ),
            "available_memory": round(
                psutil.virtual_memory().available / (1024 ** 3), 2
            ),
            "memory_usage": psutil.virtual_memory().percent,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return system_info

    except Exception as error:
        print(f"Error collecting system information: {error}")
        return None


if __name__ == "__main__":
    information = get_system_info()

    if information:
        print("\n========== CYBERSENTINEL SYSTEM INFORMATION ==========\n")

        for key, value in information.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

        print("\n======================================================")