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
        self.alert_lock = threading.Lock()

        # Initialize Threat Detector
        self.threat_detector = ThreatDetector()

        # Initialize AI Security Engine
        self.ai_engine = AISecurityEngine()

        # Connect Threat Detector to Main Controller
        self.threat_detector.alert_callback = self.handle_threat

        print("[+] Security Agent: INITIALIZED")
        print("[+] AI Security Engine: INITIALIZED")
        print("[+] Threat Detector: INITIALIZED")
        print("[+] Alert Manager: INITIALIZED")

        logging.info("CyberSentinel initialized.")

    # ======================================
    # CENTRAL SECURITY ALERT MANAGER
    # ======================================

    def handle_threat(self, threat):

        with self.alert_lock:

            print("\n")
            print("=" * 60)
            print("          CYBERSENTINEL SECURITY ALERT")
            print("=" * 60)

            print(f"Detection Time: {datetime.now()}")
            print(f"Threat Details: {threat}")

            logging.warning("THREAT DETECTED: %s", threat)

            # Forward threat to AI Engine
            print("\n[+] Forwarding threat to AI Security Engine...")

            try:

                report = self.ai_engine.analyze_threat(threat)

                self.ai_engine.display_report(report)

                logging.warning(
                    "CYBERSENTINEL SECURITY EVENT: %s",
                    report
                )

                print("\n[+] Threat analysis completed.")
                print("[+] Security event recorded.")
                print("[+] Alert Manager notified.")

            except Exception:

                logging.exception("AI threat analysis failed.")

                print("[ERROR] AI threat analysis failed.")

            print("=" * 60)

    # ======================================
    # SECURITY AGENT
    # ======================================

    def security_agent(self):

        while self.running:

            print("\n[SECURITY AGENT] System monitoring active.")

            # Existing system and network monitoring
            # will be integrated here.

            time.sleep(5)

    # ======================================
    # THREAT DETECTION ENGINE
    # ======================================

    def start_threat_detection(self):

        print("[+] Starting Threat Detection Engine...")

        try:

            self.threat_detector.start_monitoring()

        except Exception:

            logging.exception("Threat Detector error.")

            print("[ERROR] Threat Detector failed.")

    # ======================================
    # START ALL SECURITY COMPONENTS
    # ======================================

    def start(self):

        if self.running:
            return

        self.running = True

        print("\nStarting CyberSentinel components...\n")

        # Start Security Agent
        self.agent_thread = threading.Thread(
            target=self.security_agent,
            daemon=True
        )

        self.agent_thread.start()

        # Start Threat Detector
        self.detector_thread = threading.Thread(
            target=self.start_threat_detection,
            daemon=True
        )

        self.detector_thread.start()

        print("\n" + "=" * 60)
        print("       CYBERSENTINEL MONITORING STATUS")
        print("=" * 60)

        print("Security Agent: ACTIVE")
        print("AI Security Engine: ACTIVE")
        print("Threat Detector: STARTING")
        print("Alert Manager: ACTIVE")

        print("=" * 60)

        logging.info("CyberSentinel unified engine started.")

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
    # STOP APPLICATION
    # ======================================

    def stop(self):

        self.running = False

        print("\nStopping CyberSentinel...")

        logging.info("CyberSentinel stopped.")

        print("[+] Security monitoring stopped.")


# ==========================================
# APPLICATION ENTRY POINT
# ==========================================

if __name__ == "__main__":

    agent = CyberSentinel()
    agent.run()