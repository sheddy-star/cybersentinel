"""import psutil
from datetime import datetime


class ThreatDetector:

    def __init__(self):
        self.threats = []

        self.suspicious_names = [
            "keylogger",
            "cryptominer",
            "meterpreter",
            "mimikatz",
            "malware"
        ]

    def detect_suspicious_processes(self):

        for process in psutil.process_iter(
            ['pid', 'name', 'username']
        ):

            try:
                name = (process.info['name'] or "").lower()

                if any(item in name for item in self.suspicious_names):

                    threat = {
                        "type": "Suspicious Process",
                        "process": name,
                        "pid": process.info['pid'],
                        "username": process.info['username'],
                        "severity": "HIGH",
                        "time": datetime.now().isoformat()
                    }

                    self.threats.append(threat)

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def scan(self):

        self.threats = []

        self.detect_suspicious_processes()

        return self.threats


if __name__ == "__main__":

    detector = ThreatDetector()

    print("=" * 45)
    print("       CYBERSENTINEL THREAT SCAN")
    print("=" * 45)

    results = detector.scan()

    if results:

        for threat in results:

            print("\nTHREAT DETECTED!")

            for key, value in threat.items():
                print(f"{key}: {value}")

    else:

        print("\nNo suspicious process names detected.")

    print("\nScan completed.")
    print("=" * 45)"""

import psutil
import json
import time
import subprocess
import logging
import threading

from pathlib import Path
from datetime import datetime


class ThreatDetector:

    def __init__(self):
        self.threats = []
        self.scan_interval = 5

        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        self.report_file = self.log_dir / "security_events.jsonl"

        # Main controller callback.
        self.alert_callback = None

        # Prevent duplicate alerts.
        self.last_alerts = {}

        # Allows main.py to stop monitoring.
        self.stop_event = threading.Event()

        self.suspicious_names = [
            "keylogger",
            "mimikatz",
            "meterpreter",
            "cryptominer",
            "malware",
        ]

        self.suspicious_ports = [
            4444,
            5555,
            1337,
            31337,
        ]

        self.temporary_paths = [
            "/tmp/",
            "/var/tmp/",
            "/dev/shm/",
        ]

        self.logger = logging.getLogger(
            "CyberSentinel.ThreatDetector"
        )

    # ==========================================
    # SECURITY EVENT GENERATOR
    # ==========================================

    def create_event(
        self,
        attack_type,
        severity,
        description,
        recommendation,
        source_ip=None,
        target=None,
        evidence=None,
    ):
        return {
            "attack_type": attack_type,
            "severity": severity,
            "description": description,
            "recommendation": recommendation,
            "source_ip": source_ip or "Unknown",
            "target": target or "Local System",
            "timestamp": datetime.now().isoformat(),
            "evidence": evidence or {},
        }

    # ==========================================
    # SAVE SECURITY EVENTS
    # ==========================================

    def save_event(self, event):
        try:
            with open(
                self.report_file,
                "a",
                encoding="utf-8",
            ) as file:
                file.write(json.dumps(event) + "\n")

        except OSError:
            self.logger.exception(
                "Could not save security event."
            )

    # ==========================================
    # DESKTOP NOTIFICATIONS
    # ==========================================

    def notify_user(self, event):
        title = (
            f"CyberSentinel: {event['severity']} THREAT"
        )

        message = (
            f"Attack: {event['attack_type']}\n"
            f"Source: {event['source_ip']}\n"
            f"Target: {event['target']}"
        )

        try:
            subprocess.run(
                ["notify-send", title, message],
                timeout=5,
                check=False,
            )

        except (
            FileNotFoundError,
            subprocess.TimeoutExpired,
        ):
            print("Desktop notification unavailable.")

    # ==========================================
    # ALERT MANAGEMENT
    # ==========================================

    def report_threat(self, event):
        fingerprint = (
            event["attack_type"],
            event["source_ip"],
            event["target"],
        )

        now = time.time()

        last_time = self.last_alerts.get(
            fingerprint,
            0,
        )

        # Suppress repeat alerts for 5 minutes.
        if now - last_time < 300:
            return

        self.last_alerts[fingerprint] = now

        self.threats.append(event)

        self.save_event(event)

        print("\n" + "=" * 55)
        print("       CYBERSENTINEL SECURITY ALERT")
        print("=" * 55)

        print(f"Attack: {event['attack_type']}")
        print(f"Severity: {event['severity']}")
        print(f"Source IP: {event['source_ip']}")
        print(f"Target: {event['target']}")
        print(f"Description: {event['description']}")
        print(f"Recommendation: {event['recommendation']}")
        print(f"Time: {event['timestamp']}")

        print("=" * 55)

        self.notify_user(event)

        # Forward the alert to main.py.
        if self.alert_callback:
            try:
                self.alert_callback(event)

            except Exception:
                self.logger.exception(
                    "Threat callback failed."
                )

    # ==========================================
    # NETWORK EVENT CONNECTION
    # ==========================================

    def handle_network_event(self, event):
        """
        Receive events from NetworkMonitor.
        Check only new TCP connections.
        """

        if event.get("event_type") != "new_connection":
            return

        connection = event.get("connection", {})

        remote_ip = connection.get(
            "remote_ip",
            "Unknown",
        )

        remote_port = connection.get("remote_port")

        process_name = connection.get(
            "process",
            "Unknown",
        )

        pid = connection.get("pid")

        process_name_lower = str(
            process_name
        ).lower()

        suspicious_process = any(
            indicator in process_name_lower
            for indicator in self.suspicious_names
        )

        suspicious_port = (
            remote_port in self.suspicious_ports
        )

        # Ordinary connections are not reported.
        if not suspicious_process and not suspicious_port:
            return

        event_data = self.create_event(
            attack_type="Suspicious Network Connection",
            severity="MEDIUM",
            description=(
                "A new TCP connection matches a configured "
                "suspicious process-name or remote-port indicator."
            ),
            recommendation=(
                "Verify the process, destination IP and remote port. "
                "Do not block the connection based on this indicator alone."
            ),
            source_ip=remote_ip,
            target=(
                f"{process_name} on remote port "
                f"{remote_port}"
            ),
            evidence={
                "remote_ip": remote_ip,
                "remote_port": remote_port,
                "process": process_name,
                "pid": pid,
                "local_ip": connection.get("local_ip"),
                "local_port": connection.get("local_port"),
                "suspicious_process": suspicious_process,
                "suspicious_port": suspicious_port,
            },
        )

        self.report_threat(event_data)

    # ==========================================
    # PROCESS BEHAVIOUR MONITORING
    # ==========================================

    def monitor_processes(self):
        for process in psutil.process_iter(
            ["pid", "name", "exe", "username"]
        ):
            try:
                info = process.info

                name = (
                    info.get("name") or ""
                ).lower()

                executable = (
                    info.get("exe") or ""
                ).lower()

                pid = info.get("pid")

                username = info.get("username")

                # Check suspicious process names.
                if any(
                    keyword in name
                    for keyword in self.suspicious_names
                ):
                    event = self.create_event(
                        attack_type="Suspicious Process Indicator",
                        severity="MEDIUM",
                        description=(
                            f"Process name '{name}' matches "
                            "a suspicious indicator."
                        ),
                        recommendation=(
                            "Investigate the process, executable "
                            "and its origin."
                        ),
                        target=f"Process PID {pid}",
                        evidence={
                            "process": name,
                            "pid": pid,
                            "username": username,
                        },
                    )

                    self.report_threat(event)

                # Check execution from temporary directories.
                if any(
                    executable.startswith(path)
                    for path in self.temporary_paths
                ):
                    event = self.create_event(
                        attack_type="Suspicious Execution Location",
                        severity="MEDIUM",
                        description=(
                            "A process is executing from a "
                            "temporary directory."
                        ),
                        recommendation=(
                            "Inspect the executable and verify "
                            "that it is legitimate."
                        ),
                        target=f"Process PID {pid}",
                        evidence={
                            "process": name,
                            "executable": executable,
                            "pid": pid,
                        },
                    )

                    self.report_threat(event)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

    # ==========================================
    # NETWORK MONITORING
    # ==========================================

    def monitor_network(self):
        """
        Performs a separate network scan.
        Live events are also received through
        handle_network_event() from main.py.
        """

        try:
            connections = psutil.net_connections(
                kind="inet"
            )

        except psutil.AccessDenied:
            print(
                "Network monitoring has limited permissions."
            )
            return

        except psutil.Error as error:
            self.logger.error(
                "Network scan failed: %s",
                error,
            )
            return

        established = 0
        listening = 0

        for connection in connections:

            if connection.status == "ESTABLISHED":
                established += 1

            elif connection.status == "LISTEN":
                listening += 1

            if not connection.raddr:
                continue

            if connection.status != "ESTABLISHED":
                continue

            try:
                process = psutil.Process(
                    connection.pid
                )

                name = (
                    process.name() or ""
                ).lower()

                executable = (
                    process.exe() or ""
                ).lower()

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ):
                continue

            remote_ip = connection.raddr.ip
            remote_port = connection.raddr.port

            suspicious_process = any(
                keyword in name
                for keyword in self.suspicious_names
            )

            temporary_execution = any(
                executable.startswith(path)
                for path in self.temporary_paths
            )

            suspicious_port = (
                remote_port in self.suspicious_ports
            )

            if (
                suspicious_process or temporary_execution
            ) and suspicious_port:

                event = self.create_event(
                    attack_type="Suspicious Outbound Connection",
                    severity="HIGH",
                    description=(
                        "A suspicious process is communicating "
                        "through an unusual remote port."
                    ),
                    recommendation=(
                        "Investigate the process and remote destination. "
                        "Verify the evidence before taking action."
                    ),
                    source_ip=remote_ip,
                    target=(
                        f"{name} on port {remote_port}"
                    ),
                    evidence={
                        "process": name,
                        "remote_ip": remote_ip,
                        "remote_port": remote_port,
                        "pid": connection.pid,
                    },
                )

                self.report_threat(event)

        print(
            f"\nNetwork status: {established} "
            f"established connections, "
            f"{listening} listening sockets."
        )

        print("\nSecurity scan completed.")

    # ==========================================
    # COMPLETE SECURITY SCAN
    # ==========================================

    def scan(self):
        """
        Run all current threat detection checks.
        """

        print("\nStarting CyberSentinel security scan...")

        self.monitor_processes()
        self.monitor_network()

    # ==========================================
    # START MONITORING
    # ==========================================

    def start_monitoring(self):
        print("=" * 55)
        print("       CYBERSENTINEL SECURITY ENGINE")
        print("=" * 55)

        print("Status: ACTIVE")
        print(
            f"Monitoring interval: "
            f"{self.scan_interval} seconds"
        )

        print("Monitoring can be stopped by main.py.")

        self.stop_event.clear()

        try:
            while not self.stop_event.is_set():
                self.scan()

                self.stop_event.wait(
                    self.scan_interval
                )

        except Exception:
            self.logger.exception(
                "Threat monitoring loop failed."
            )
            raise

        finally:
            print(
                "\nCyberSentinel threat monitoring stopped."
            )

    # ==========================================
    # STOP MONITORING
    # ==========================================

    def stop_monitoring(self):
        """Signal the monitoring thread to stop."""

        self.stop_event.set()


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    detector = ThreatDetector()
    detector.start_monitoring()