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
import os
import re
import json
import time
import socket
import subprocess

from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict


class ThreatDetector:

    def __init__(self):

        self.threats = []

        self.scan_interval = 5

        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)

        self.report_file = self.log_dir / "security_events.jsonl"

        self.last_alerts = None

        self.suspicious_names = [
            "keylogger",
            "mimikatz",
            "meterpreter",
            "cryptominer"
        ]

        self.suspicious_ports = [
            4444,
            5555,
            1337,
            31337
        ]

        self.temporary_paths = [
            "/tmp/",
            "/var/tmp/",
            "/dev/shm/"
        ]

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
        evidence=None
    ):

        event = {
            "attack_type": attack_type,
            "severity": severity,
            "description": description,
            "recommendation": recommendation,
            "source_ip": source_ip or "Unknown",
            "target": target or "Local System",
            "timestamp": datetime.now().isoformat(),
            "evidence": evidence or {}
        }

        return event

    # ==========================================
    # SAVE SECURITY EVENTS
    # ==========================================

    def save_event(self, event):

        with open(self.report_file, "a") as file:

            file.write(json.dumps(event) + "\n")

    # ==========================================
    # DESKTOP NOTIFICATIONS
    # ==========================================

    def notify_user(self, event):

        title = (
            f"CyberSentinel: {event['severity']} "
            f"THREAT"
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
                check=False
            )

        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("Desktop notification unavailable.")

    # ==========================================
    # ALERT MANAGEMENT
    # ==========================================

    def report_threat(self, event):

        fingerprint = (
            event["attack_type"],
            event["source_ip"],
            event["target"]
        )

        now = time.time()

        # Prevent repeated notifications every 5 seconds.
        last_time = self.last_alerts.get(fingerprint, 0)

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

        print(
            f"Recommendation: "
            f"{event['recommendation']}"
        )

        print(f"Time: {event['timestamp']}")

        print("=" * 55)

        self.notify_user(event)

    # ==========================================
    # PROCESS BEHAVIOUR MONITORING
    # ==========================================

    def monitor_processes(self):

        for process in psutil.process_iter(
            ["pid", "name", "exe", "username"]
        ):

            try:

                info = process.info

                name = (info["name"] or "").lower()

                executable = info["exe"] or ""

                executable = executable.lower()

                pid = info["pid"]

                # Check suspicious process names.

                if any(
                    keyword in name
                    for keyword in self.suspicious_names
                ):

                    event = self.create_event(
                        attack_type="Suspicious Process Indicator",
                        severity="MEDIUM",
                        description=(
                            f"Process name '{name}' "
                            "matches a suspicious indicator."
                        ),
                        recommendation=(
                            "Investigate the process, "
                            "its executable and its origin."
                        ),
                        target=f"Process PID {pid}",
                        evidence={
                            "process": name,
                            "pid": pid,
                            "username": info["username"]
                        }
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
                            "Inspect the executable and "
                            "verify its legitimacy."
                        ),
                        target=f"Process PID {pid}",
                        evidence={
                            "process": name,
                            "executable": executable,
                            "pid": pid
                        }
                    )

                    self.report_threat(event)

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):

                continue

    # ==========================================
    # NETWORK MONITORING
    # ==========================================

    def monitor_network(self):

        try:

            connections = psutil.net_connections(
                kind="inet"
            )

        except psutil.AccessDenied:

            print(
                "Network monitoring has limited "
                "permissions."
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
                psutil.AccessDenied
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

            # Only alert when multiple indicators combine.

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
                        "Investigate the process and remote "
                        "destination. Do not assume the "
                        "connection is malicious without "
                        "further verification."
                    ),
                    source_ip=remote_ip,
                    target=f"{name} on port {remote_port}",
                    evidence={
                        "process": name,
                        "remote_ip": remote_ip,
                        "remote_port": remote_port,
                        "pid": connection.pid
                    }
                )

                self.report_threat(event)

        print(
            f"\nNetwork status: "
            f"{established} established connections, "
            f"{listening} listening sockets."
        )

    # ==========================================
    # SSH BRUTE-FORCE DETECTION
    # ==========================================

    def monitor_ssh_attacks(self):

        auth_log = Path("/var/log/auth.log")

        if not auth_log.exists():
            return

        try:

            with open(
                auth_log,
                "r",
                errors="ignore"
            ) as file:

                lines = file.readlines()[-5000:]

        except PermissionError:

            print(
                "Cannot read authentication logs. "
                "Check your user permissions."
            )

            return

        failures = defaultdict(list)

        now = datetime.now()

        for line in lines:

            if not re.search(
                r"Failed password|Invalid user",
                line,
                re.IGNORECASE
            ):

                continue

            match = re.search(
                r"from\s+(\d{1,3}(?:\.\d{1,3}){3})",
                line
            )

            if not match:
                continue

            ip = match.group(1)

            try:

                event_time = datetime.strptime(
                    f"{now.year} {line[:15]}",
                    "%Y %b %d %H:%M:%S"
                )

                if event_time - now > timedelta(days=1):
                    event_time = event_time.replace(
                        year=now.year - 1
                    )

            except ValueError:
                continue

            if now - event_time <= timedelta(minutes=5):

                failures[ip].append(event_time)

        for ip, attempts in failures.items():

            if len(attempts) >= 5:

                event = self.create_event(
                    attack_type="SSH Brute-Force Attempt",
                    severity="HIGH",
                    description=(
                        f"{len(attempts)} failed SSH "
                        "authentication attempts were "
                        f"recorded from {ip} within five minutes."
                    ),
                    recommendation=(
                        "Investigate the source IP, review "
                        "authentication logs and consider "
                        "restricting SSH access."
                    ),
                    source_ip=ip,
                    target="SSH Authentication Service",
                    evidence={
                        "failed_attempts": len(attempts),
                        "observation_window": "5 minutes"
                    }
                )

                self.report_threat(event)

    # ==========================================
    # COMPLETE SECURITY SCAN
    # ==========================================

    def scan(self):

        print("\nStarting CyberSentinel security scan...")

        self.monitor_processes()

        self.monitor_network()

        self.monitor_ssh_attacks()

        print("\nSecurity scan completed.")

    # ==========================================
    # CONTINUOUS MONITORING
    # ==========================================

    def start_monitoring(self):

        print("=" * 55)
        print("       CYBERSENTINEL SECURITY ENGINE")
        print("=" * 55)

        print("Status: ACTIVE")
        print("Monitoring interval: 5 seconds")
        print("Press CTRL+C to stop monitoring.")

        try:

            while True:

                self.scan()

                time.sleep(self.scan_interval)

        except KeyboardInterrupt:

            print("\nCyberSentinel monitoring stopped.")


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    detector = ThreatDetector()

    detector.start_monitoring()
