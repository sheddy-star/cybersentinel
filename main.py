"""from modules.system_info import get_system_info


class CyberSentinelAgent:

    def __init__(self):
        self.name = "CyberSentinel"
        self.status = "Online"

    def start(self):
        print("=" * 40)
        print("       CYBERSENTINEL AI AGENT")
        print("=" * 40)

        print(f"Agent: {self.name}")
        print(f"Status: {self.status}")

        print("\n--- SYSTEM INFORMATION ---")

        system_info = get_system_info()

        for key, value in system_info.items():
            print(f"{key}: {value}")

        print("\nCyberSentinel is running...")


if __name__ == "__main__":
    agent = CyberSentinelAgent()
    agent.start()



import psutil
from datetime import datetime

from modules.system_info import get_system_info


class CyberSentinelAgent:

    def __init__(self):
        self.name = "CyberSentinel"
        self.version = "1.0.0"
        self.status = "Stopped"

    def start(self):

        self.status = "Running"

        print("=" * 50)
        print("       CYBERSENTINEL SECURITY AGENT")
        print("=" * 50)

        print(f"Agent: {self.name}")
        print(f"Version: {self.version}")
        print(f"Status: {self.status}")
        print(f"Time: {datetime.now()}")

        self.collect_system_information()
        self.monitor_system()

    def collect_system_information(self):

        print("\n--- SYSTEM INFORMATION ---")

        information = get_system_info()

        for key, value in information.items():
            print(f"{key}: {value}")

    def monitor_system(self):

        print("\n--- SYSTEM MONITORING ---")

        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        processes = len(psutil.pids())

        print(f"CPU Usage: {cpu}%")
        print(f"RAM Usage: {ram}%")
        print(f"Running Processes: {processes}")

        print("\nCyberSentinel monitoring completed.")

    def stop(self):

        self.status = "Stopped"
        print("\nCyberSentinel Agent stopped.")
    from agent.core import CyberSentinelAgent


def main():

    agent = CyberSentinelAgent()

    try:
        agent.start()

    except KeyboardInterrupt:
        agent.stop()


if __name__ == "__main__":
    main()
from agent.core import CyberSentinelAgent


def main():

    agent = CyberSentinelAgent()

    try:
        agent.start()

    except KeyboardInterrupt:
        agent.stop()


if __name__ == "__main__":
    main()
from agent.core import CyberSentinelAgent


def main():

    print("Starting CyberSentinel...")

    agent = CyberSentinelAgent()

    try:
        agent.start()

    except KeyboardInterrupt:
        agent.stop()


if __name__ == "__main__":
    main()

import time
import threading
from datetime import datetime

from modules.threat_detector import ThreatDetector


class CyberSentinel:

    def __init__(self):
        print("=" * 55)
        print("          CYBERSENTINEL AI SECURITY ENGINE")
        print("=" * 55)

        self.running = False
        self.threat_detector = ThreatDetector()

    def handle_threat(self, threat):
       

        print("\n" + "!" * 55)
        print("             SECURITY ALERT")
        print("!" * 55)

        print(f"Time: {datetime.now()}")
        print(f"Threat: {threat}")

        print("!" * 55 + "\n")

    def start_monitoring(self):
        

        if self.running:
            return

        self.running = True

        print("[+] Starting CyberSentinel monitoring...")

        self.monitor_thread = threading.Thread(
            target=self.threat_detector.start_monitoring,
            daemon=True
        )

        self.monitor_thread.start()

        print("[+] Threat detector activated.")
        print("[+] CyberSentinel is monitoring your system.")

    def stop_monitoring(self):
        

        self.running = False
        print("[!] CyberSentinel monitoring stopped.")

    def run(self):

        self.start_monitoring()

        try:
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop_monitoring()


if __name__ == "__main__":
    agent = CyberSentinel()
    agent.run()"""

import os
import time
import threading
import logging

from datetime import datetime

from modules.system_info import get_system_info
from modules.monitor import SystemMonitor
from modules.network_monitor import NetworkMonitor
from modules.process_monitor import ProcessMonitor
from modules.threat_detector import ThreatDetector
from modules.ai_engine import AISecurityEngine


# ==========================================
# CYBERSENTINEL LOGGING SYSTEM
# ==========================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/cybersentinel.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ==========================================
# MAIN CYBERSENTINEL CONTROLLER
# ==========================================

class CyberSentinel:

    def __init__(self):
        print("=" * 60)
        print("       CYBERSENTINEL UNIFIED SECURITY SYSTEM")
        print("=" * 60)

        self.running = False
        self.stop_event = threading.Event()
        self.alert_lock = threading.Lock()
        self.threads = []

        # System monitoring modules
        self.monitor = SystemMonitor()
        self.network_monitor = NetworkMonitor()
        self.process_monitor = ProcessMonitor()

        # Threat detection and AI
        self.threat_detector = ThreatDetector()
        self.ai_engine = AISecurityEngine()

        # Connect module callbacks to the main controller
        self.network_monitor.event_callback = (
            self.handle_network_event
        )

        self.threat_detector.alert_callback = (
            self.handle_threat
        )

        print("[+] System Monitor: INITIALIZED")
        print("[+] Network Monitor: INITIALIZED")
        print("[+] Process Monitor: INITIALIZED")
        print("[+] Threat Detector: INITIALIZED")
        print("[+] AI Security Engine: INITIALIZED")
        print("[+] Alert Manager: INITIALIZED")

        logging.info("CyberSentinel initialized.")

    # ======================================
    # SYSTEM INFORMATION
    # ======================================

    def collect_system_information(self):
        print("\n--- SYSTEM INFORMATION ---")

        information = get_system_info()

        if not information:
            print("Unable to collect system information.")
            return

        for key, value in information.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

    # ======================================
    # CENTRAL THREAT ALERT HANDLER
    # ======================================

    def handle_threat(self, threat):
        with self.alert_lock:
            print("\n" + "=" * 60)
            print("       CYBERSENTINEL SECURITY ALERT")
            print("=" * 60)

            print(f"Detection Time: {datetime.now()}")
            print(f"Threat Details: {threat}")

            logging.warning("THREAT DETECTED: %s", threat)

            try:
                # Build readable information for the AI engine
                if isinstance(threat, dict):
                    threat_text = (
                        f"Attack: {threat.get('attack_type', 'Unknown')}\n"
                        f"Severity: {threat.get('severity', 'Unknown')}\n"
                        f"Description: {threat.get('description', '')}\n"
                        f"Source IP: {threat.get('source_ip', 'Unknown')}\n"
                        f"Target: {threat.get('target', 'Unknown')}\n"
                        f"Evidence: {threat.get('evidence', {})}"
                    )
                else:
                    threat_text = str(threat)

                print("\n[+] Forwarding threat to AI Security Engine...")

                report = self.ai_engine.analyze_threat(
                    threat_text
                )

                self.ai_engine.display_report(report)

                logging.warning(
                    "CYBERSENTINEL AI ANALYSIS: %s",
                    report
                )

                print("[+] Threat analysis completed.")

            except Exception:
                logging.exception(
                    "AI threat analysis failed."
                )

                print("[ERROR] AI threat analysis failed.")

            print("=" * 60)

    # ======================================
    # NETWORK EVENT HANDLER
    # ======================================

    def handle_network_event(self, event):
        event_type = event.get("event_type", "unknown")

        if event_type == "new_connection":
            connection = event.get("connection", {})

            local_ip = connection.get("local_ip", "Unknown")
            local_port = connection.get("local_port", "Unknown")

            remote_ip = connection.get("remote_ip", "Unknown")
            remote_port = connection.get("remote_port", "Unknown")

            process = connection.get("process", "Unknown")
            pid = connection.get("pid", "Unknown")

            message = (
                f"NEW CONNECTION | "
                f"{local_ip}:{local_port} -> "
                f"{remote_ip}:{remote_port} | "
                f"Process: {process} | PID: {pid}"
            )

            print(f"\n[NETWORK EVENT] {message}")
            logging.info("NETWORK EVENT: %s", message)

        elif event_type == "connection_closed":
            connection_key = event.get(
                "connection_key",
                ()
            )

            logging.info(
                "NETWORK EVENT: CONNECTION CLOSED | %s",
                connection_key
            )

        else:
            logging.info(
                "NETWORK EVENT: %s | %s",
                event_type,
                event
            )

    # ======================================
    # LIVE NETWORK MONITOR
    # ======================================

    def network_monitor_loop(self):
        print("[+] Live Network Monitor started.")
        logging.info("Live Network Monitor started.")

        while self.running and not self.stop_event.is_set():
            try:
                self.network_monitor.display_connections()

            except Exception:
                logging.exception("Network Monitor error.")
                print("[ERROR] Network Monitor encountered an error.")

            self.stop_event.wait(2)

        print("[+] Live Network Monitor stopped.")
        logging.info("Live Network Monitor stopped.")

    # ======================================
    # THREAT DETECTOR
    # ======================================

    def threat_detection_loop(self):
        print("[+] Starting Threat Detection Engine...")

        try:
            self.threat_detector.start_monitoring()

        except Exception:
            logging.exception("Threat Detector error.")
            print("[ERROR] Threat Detector failed.")

    # ======================================
    # START ALL COMPONENTS
    # ======================================

    def start(self):
        if self.running:
            print("CyberSentinel is already running.")
            return

        self.running = True
        self.stop_event.clear()

        print("\nStarting CyberSentinel components...\n")

        logging.info("CyberSentinel unified engine started.")

        # Collect system information once at startup
        self.collect_system_information()

        # Run an initial process security scan
        print("\n[+] Running initial process security scan...")

        try:
            self.process_monitor.scan_processes()

        except Exception:
            logging.exception("Initial process scan failed.")

        # Record the initial network baseline
        print("\n[+] Recording initial network connections...")

        self.network_monitor.display_connections()

        # Start continuous system monitoring
        self.system_thread = threading.Thread(
            target=self.monitor.start_monitoring,
            name="SystemMonitor",
            daemon=True
        )

        # Start continuous network monitoring
        self.network_thread = threading.Thread(
            target=self.network_monitor_loop,
            name="NetworkMonitor",
            daemon=True
        )

        # Start continuous threat detection
        self.detector_thread = threading.Thread(
            target=self.threat_detection_loop,
            name="ThreatDetector",
            daemon=True
        )

        self.threads = [
            self.system_thread,
            self.network_thread,
            self.detector_thread
        ]

        for thread in self.threads:
            thread.start()

        print("\n" + "=" * 60)
        print("       CYBERSENTINEL MONITORING STATUS")
        print("=" * 60)

        print("System Monitor: ACTIVE")
        print("Network Monitor: ACTIVE")
        print("Process Monitor: INITIAL SCAN COMPLETE")
        print("Threat Detector: STARTING")
        print("AI Security Engine: ACTIVE")
        print("Alert Manager: ACTIVE")

        print("=" * 60)
        print("Press CTRL+C to stop CyberSentinel.")

    # ======================================
    # MAIN APPLICATION LOOP
    # ======================================

    def run(self):
        self.start()

        try:
            while self.running:
                time.sleep(1)

        except KeyboardInterrupt:
            self.stop()

    # ======================================
    # STOP ALL COMPONENTS
    # ======================================

    def stop(self):
        if not self.running:
            return

        print("\nStopping CyberSentinel...")

        self.running = False
        self.stop_event.set()

        # Stop the system monitor
        try:
            self.monitor.stop_monitoring()
        except Exception:
            logging.exception("Failed to stop System Monitor.")

        # Stop the threat detector
        try:
            self.threat_detector.stop_monitoring()
        except Exception:
            logging.exception("Failed to stop Threat Detector.")

        # Wait briefly for background threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=3)

        logging.info("CyberSentinel stopped.")

        print("[+] All monitoring components stopped.")


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    agent = CyberSentinel()
    agent.run()