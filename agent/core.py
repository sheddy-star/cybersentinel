from datetime import datetime

from modules.system_info import get_system_info
from modules.monitor import SystemMonitor
from modules.network_monitor import NetworkMonitor
from modules.process_monitor import ProcessMonitor


class CyberSentinelAgent:

    def __init__(self):

        self.name = "CyberSentinel"
        self.version = "1.0.0"
        self.status = "Stopped"

        # Initialize monitoring modules
        self.monitor = SystemMonitor()
        self.network_monitor = NetworkMonitor()
        self.process_monitor = ProcessMonitor()

    def start(self):

        self.status = "Running"

        print("=" * 55)
        print("          CYBERSENTINEL SECURITY AGENT")
        print("=" * 55)

        print(f"Agent: {self.name}")
        print(f"Version: {self.version}")
        print(f"Status: {self.status}")
        print(f"Time: {datetime.now()}")

        # System information
        self.collect_system_information()

        # Network monitoring
        self.network_monitor.display_connections()

        # Process security scan
        self.process_monitor.scan_processes()

        # Continuous system monitoring
        print("\nStarting CyberSentinel monitoring engine...")

        self.monitor.start_monitoring()

    def collect_system_information(self):

        print("\n--- SYSTEM INFORMATION ---")

        information = get_system_info()

        for key, value in information.items():

            print(f"{key}: {value}")

    def stop(self):

        self.status = "Stopped"

        print("\nCyberSentinel Agent stopped.")