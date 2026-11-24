
import psutil
import time
from datetime import datetime


class SystemMonitor:

    def __init__(self):
        self.running = False

    def collect_metrics(self):

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage("/").percent
        processes = len(psutil.pids())

        return {
            "time": datetime.now().strftime("%H:%M:%S"),
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "processes": processes
        }

    def start_monitoring(self):

        self.running = True

        print("\nCYBERSENTINEL CONTINUOUS MONITORING")
        print("=" * 45)

        try:
            while self.running:

                metrics = self.collect_metrics()

                print(f"\nTime: {metrics['time']}")
                print(f"CPU Usage: {metrics['cpu']}%")
                print(f"RAM Usage: {metrics['ram']}%")
                print(f"Disk Usage: {metrics['disk']}%")
                print(f"Running Processes: {metrics['processes']}")

                if metrics["cpu"] > 85:
                    print("WARNING: High CPU usage!")

                if metrics["ram"] > 85:
                    print("WARNING: High RAM usage!")

                time.sleep(2)

        except KeyboardInterrupt:
            self.stop_monitoring()

    def stop_monitoring(self):

        self.running = False
        print("\nCyberSentinel monitoring stopped.")
