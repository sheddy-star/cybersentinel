import logging
from datetime import datetime


class AISecurityEngine:

    def __init__(self):

        self.name = "CyberSentinel AI Security Engine"
        self.status = "ACTIVE"

        print("[+] AI Security Engine initialized.")

    def analyze_threat(self, threat):

        """
        Analyse security events and determine
        their likely severity.
        """

        threat_text = str(threat).lower()

        severity = "LOW"
        recommendation = "Continue monitoring."

        # SSH brute-force detection
        if any(word in threat_text for word in [
            "brute force",
            "ssh attack",
            "failed login",
            "multiple login failures"
        ]):

            severity = "HIGH"
            recommendation = (
                "Investigate the source IP and review SSH logs. "
                "Consider restricting repeated login attempts."
            )

        # Malware indicators
        elif any(word in threat_text for word in [
            "malware",
            "trojan",
            "ransomware",
            "suspicious process"
        ]):

            severity = "CRITICAL"
            recommendation = (
                "Investigate the process immediately. "
                "Isolate the affected device if compromise is confirmed."
            )

        # Network threats
        elif any(word in threat_text for word in [
            "port scan",
            "network attack",
            "suspicious connection"
        ]):

            severity = "MEDIUM"
            recommendation = (
                "Investigate the connection and inspect "
                "the source address."
            )

        # Generate analysis report
        report = {

            "engine": self.name,

            "timestamp": datetime.now().isoformat(),

            "threat": str(threat),

            "severity": severity,

            "recommendation": recommendation

        }

        logging.warning(
            "AI SECURITY ANALYSIS: %s",
            report
        )

        return report

    def display_report(self, report):

        print("\n")
        print("=" * 60)
        print("          CYBERSENTINEL AI THREAT ANALYSIS")
        print("=" * 60)

        print(f"Threat: {report['threat']}")

        print(f"Severity: {report['severity']}")

        print(
            f"Recommendation: "
            f"{report['recommendation']}"
        )

        print(f"Analysis Time: {report['timestamp']}")

        print("=" * 60)
