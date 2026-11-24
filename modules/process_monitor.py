import psutil
import os


class ProcessMonitor:

    def __init__(self):
        self.suspicious_processes = []

        self.temporary_locations = [
            "/tmp/",
            "/var/tmp/",
            "/dev/shm/"
        ]

    def scan_processes(self):

        self.suspicious_processes = []

        print("\n--- PROCESS SECURITY SCAN ---")

        for process in psutil.process_iter(
            ["pid", "name", "username", "exe", "memory_percent"]
        ):

            try:
                info = process.info

                pid = info["pid"]
                name = info["name"] or "Unknown"
                username = info["username"] or "Unknown"
                executable = info["exe"] or "Unknown"
                memory = info["memory_percent"] or 0

                reasons = []

                if executable != "Unknown":

                    executable_path = os.path.realpath(executable)

                    for location in self.temporary_locations:

                        if executable_path.startswith(location):
                            reasons.append(
                                "Executable running from temporary directory"
                            )
                            break

                if memory > 25:
                    reasons.append(
                        "Unusually high memory consumption"
                    )

                if reasons:

                    self.suspicious_processes.append({
                        "pid": pid,
                        "name": name,
                        "username": username,
                        "executable": executable,
                        "memory": round(memory, 2),
                        "reasons": reasons
                    })

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        self.display_results()

    def display_results(self):

        if not self.suspicious_processes:
            print("No suspicious process indicators detected.")
            return

        print(
            f"Potentially suspicious processes: "
            f"{len(self.suspicious_processes)}"
        )

        for process in self.suspicious_processes:

            print("\nWARNING: Process requires investigation")

            print(f"Name: {process['name']}")
            print(f"PID: {process['pid']}")
            print(f"User: {process['username']}")
            print(f"Memory: {process['memory']}%")
            print(f"Executable: {process['executable']}")

            for reason in process["reasons"]:
                print(f"Indicator: {reason}")