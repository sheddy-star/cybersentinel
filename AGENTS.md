# CyberSentinel - AI Agent Instructions

## 1. Project Overview

CyberSentinel is a unified cybersecurity monitoring and traffic-control system designed to protect users' computers and network connections.

The project is being developed in Python, initially targeting Linux systems.

The long-term goal is to create a browser-based cybersecurity platform that allows users to connect their devices, monitor security activity, receive threat reports, and manage network protection.

CyberSentinel should be developed incrementally, prioritizing stability, simplicity, and reliable security functionality.

The project must not become unnecessarily complicated during its early development stages.

---

## 2. Main Objectives

CyberSentinel should eventually provide the following capabilities:

- Real-time network connection monitoring.
- Application and process network monitoring.
- Suspicious traffic detection.
- SSH brute-force detection.
- Suspicious listening-port detection.
- Behaviour-based malware detection.
- AI-assisted threat analysis.
- Security event logging.
- Real-time threat notifications.
- IP address blocking and unblocking.
- Application-level traffic control.
- Firewall management.
- Network traffic statistics.
- Browser-based security dashboard.
- Device security reports.

The system should provide useful security information while avoiding unnecessary disruption to legitimate network activity.

---

## 3. Current Project Status

CyberSentinel currently has a working Python monitoring framework.

The main application starts successfully and displays:

- Security Agent initialized.
- AI Security Engine initialized.
- Threat Detector initialized.
- Alert Manager initialized.
- Network monitoring active.

The current network monitor reports the number of established connections and listening sockets.

Example:

```text
Network status: 22 established connections, 9 listening sockets.
```

The system performs repeated security scans at approximately five-second intervals.

The application can be stopped using CTRL+C.

### Existing Components

The project currently contains the following modules:

```text
cybersentinel/
│
├── main.py
│
├── modules/
│   ├── __init__.py
│   ├── threat_detector.py
│   ├── ai_engine.py
│   ├── network_monitor.py
│   ├── process_monitor.py
│   ├── monitor.py
│   └── system_info.py
│
├── logs/
│
└── models/
```

The exact contents of existing modules must be inspected before making changes.

Do not assume that a module is incomplete simply because its implementation is not visible in this file.

---

## 4. Existing Architecture

CyberSentinel currently follows this architecture:

```text
                 CYBERSENTINEL
                       |
                       |
                MAIN CONTROLLER
                   main.py
                       |
          +------------+------------+
          |            |            |
          |            |            |
    SECURITY       THREAT        NETWORK
     AGENT         DETECTOR      MONITOR
          |            |            |
          |            |            |
          +------------+------------+
                       |
                       |
                 ALERT MANAGER
                       |
                       |
               AI SECURITY ENGINE
                       |
                       |
                THREAT ANALYSIS
                       |
                       |
                SECURITY REPORTS
                       |
                       |
                 LOGGING SYSTEM
```

The main controller coordinates the security components.

The Threat Detector identifies suspicious activity and forwards events to the central alert handler.

The AI Security Engine analyzes received events and produces security reports.

The logging system records important events for investigation and reporting.

---

## 5. Development Principles

The AI coding agent must follow these principles throughout development.

### 5.1 Inspect Before Editing

Before modifying any file:

1. Inspect the existing project structure.
2. Read the relevant Python modules.
3. Understand how the existing components communicate.
4. Identify dependencies and expected interfaces.
5. Avoid replacing working functionality unnecessarily.

### 5.2 Preserve Existing Functionality

Do not delete or replace existing modules without a clear technical reason.

Preserve existing classes, functions, callbacks, and integrations whenever possible.

If a module needs improvement, extend it rather than rebuilding it from scratch.

### 5.3 Make Incremental Changes

Implement one milestone at a time.

Do not attempt to implement the entire cybersecurity platform in one operation.

Each milestone must be tested before proceeding to the next.

### 5.4 Provide Complete Files

When modifying a Python module, provide the complete updated file rather than scattered code snippets.

Clearly identify the filename and its location.

The developer works in VS Code and prefers complete, connected code that can be copied into the project.

### 5.5 Avoid Unnecessary Dependencies

Use existing Python libraries whenever possible.

Prefer established libraries such as:

- `psutil` for system and network monitoring.
- Python's `logging` module for event logging.
- Python's `threading` module for background tasks.
- `subprocess` for carefully controlled system integration.

Do not install additional libraries unless they are necessary.

### 5.6 Handle Errors Properly

All monitoring components should handle expected errors gracefully.

Examples include:

- Permission errors.
- Missing processes.
- Unavailable network interfaces.
- Missing dependencies.
- Firewall command failures.
- Unexpected connection states.

Errors should be logged with useful details.

Do not silently ignore important security errors.

### 5.7 Keep Security Features Safe

CyberSentinel must not automatically block every unfamiliar IP address.

Unknown connections are not necessarily malicious.

Initially, firewall actions should require user confirmation.

Protect trusted IP addresses and essential system services from accidental blocking.

Do not modify firewall rules without clearly explaining the action and its consequences.

---

## 6. Development Roadmap

The following milestones define the planned development sequence.

### Milestone 1: Live Network Connection Monitoring

Upgrade the existing network monitoring module to display detailed connection information.

Required information:

- Local IP address.
- Local port.
- Remote IP address.
- Remote port.
- Protocol.
- Connection state.
- Process ID.
- Application or process name.

The monitor should distinguish between established connections and listening sockets.

The system should continue monitoring at a configurable interval.

Do not implement firewall blocking during this milestone.

**Completion criteria:**

CyberSentinel can display detailed network connections and associate them with processes where permissions and operating-system information allow.

---

### Milestone 2: Application and Process Monitoring

Improve the existing process monitoring functionality.

Required features:

- Identify applications using network connections.
- Display process IDs.
- Identify executable paths where accessible.
- Detect newly started processes.
- Detect processes that terminate.
- Associate network activity with processes.

The system should avoid repeatedly reporting unchanged process information.

**Completion criteria:**

CyberSentinel can identify which applications are responsible for network activity.

---

### Milestone 3: Suspicious Traffic Detection

Extend the Threat Detector to analyze network activity.

Detection capabilities should include:

#### Port Scanning

Identify remote IP addresses attempting to connect to multiple ports.

#### SSH Brute-Force Detection

Identify repeated SSH authentication failures where authentication logs are accessible.

#### Suspicious Listening Ports

Identify newly opened listening ports and compare them with previous observations.

#### Unusual Outbound Connections

Identify potentially suspicious outbound network activity.

#### Connection Spikes

Detect unusually large increases in network connections.

Detection thresholds should be configurable.

Avoid excessive false positives.

**Completion criteria:**

The Threat Detector generates structured security events when suspicious activity is detected.

---

### Milestone 4: Threat History and Security Reports

Create a persistent security event history.

Required features:

- Record threat detection time.
- Record source IP address.
- Record destination IP address.
- Record relevant ports.
- Record process information.
- Record threat category.
- Record severity.
- Record recommended actions.

Use a simple database such as SQLite if persistent structured storage is required.

The system should prevent repeated identical events from overwhelming the logs.

**Completion criteria:**

CyberSentinel can retain and retrieve previous security events.

---

### Milestone 5: Firewall Manager

Create a new module:

```text
modules/firewall_manager.py
```

The module should provide a controlled interface for firewall management.

Required functionality:

- Check firewall status.
- List managed blocked IP addresses.
- Block an IP address.
- Unblock an IP address.
- Create temporary IP blocks.
- Manage trusted IP addresses.
- Record firewall actions.

Use an appropriate Linux firewall backend, such as UFW or nftables, depending on the system.

Do not assume that a firewall command succeeded.

Check its result and report errors.

Use safe command execution practices.

Never construct shell commands by blindly concatenating untrusted input.

**Completion criteria:**

Authorized users can safely manage firewall rules through CyberSentinel.

---

### Milestone 6: IP Blocking and Unblocking

Connect the Firewall Manager to the central alert system.

When a suspicious IP address is detected:

1. Generate a security alert.
2. Analyze the event.
3. Present the threat details.
4. Recommend an appropriate action.
5. Allow the user to confirm blocking.
6. Apply the firewall rule.
7. Record the action.

Provide an option to unblock previously blocked IP addresses.

Implement safeguards against blocking trusted addresses or essential services.

**Completion criteria:**

CyberSentinel can block and unblock selected IP addresses and record the results.

---

### Milestone 7: Browser-Based Dashboard

Create a browser-based interface for CyberSentinel.

The dashboard should communicate with the Python backend through a local API.

Possible backend technologies include Flask or FastAPI.

The frontend may use HTML, CSS, and JavaScript.

Required dashboard sections:

#### Overview

- System security status.
- Total network connections.
- Active threats.
- Blocked IP addresses.
- Recent security events.

#### Live Traffic

- Current network connections.
- Application names.
- Remote IP addresses.
- Connection states.

#### Threat Reports

- Threat category.
- Severity.
- Detection time.
- AI analysis.
- Recommended actions.

#### Firewall

- Block IP addresses.
- Unblock IP addresses.
- View firewall status.
- Manage trusted addresses.

#### History

- Previous threats.
- Network events.
- Firewall actions.

The dashboard must not expose unrestricted system commands or firewall controls to unauthenticated users.

---

### Milestone 8: Application-Level Traffic Control

Add application-level network restrictions.

Potential functionality:

- Allow an application to access the network.
- Restrict an application's network access.
- Display application network activity.
- Manage application-specific firewall rules.

The implementation must account for Linux firewall capabilities and process identification limitations.

Do not assume that blocking a remote IP will block only one application.

**Completion criteria:**

Users can manage network access for selected applications using supported system-level controls.

---

### Milestone 9: Bandwidth Monitoring

Add network traffic statistics.

Required information:

- Upload speed.
- Download speed.
- Total bytes sent.
- Total bytes received.
- Network interface.
- Traffic history.

Display statistics in the dashboard.

Avoid claiming that per-application bandwidth is available unless it is actually measured.

---

## 7. AI Security Engine

The current AI Security Engine provides basic rule-based threat analysis.

It should eventually support:

- Threat classification.
- Severity assessment.
- Context-aware recommendations.
- Security event summarization.
- Threat correlation.
- Behaviour-based analysis.

Do not describe the current rule-based engine as a trained machine-learning model.

Advanced AI or machine-learning functionality should be introduced only after reliable security event data is available.

The AI engine must not independently execute destructive actions or modify firewall rules without authorization.

---

## 8. Security Event Format

Where possible, security events should use a consistent structure.

Example:

```python
{
    "event_type": "suspicious_connection",
    "timestamp": "2026-11-24 14:30:00",
    "source_ip": "192.168.1.50",
    "destination_ip": "203.0.113.10",
    "source_port": 52144,
    "destination_port": 22,
    "protocol": "TCP",
    "process_name": "python3",
    "severity": "HIGH",
    "description": "Suspicious network connection detected"
}
```

This is an example event structure.

Actual values must come from observed network activity.

Do not fabricate threat information.

---

## 9. Testing Requirements

Each new feature must be tested before it is considered complete.

Testing should include:

- Successful startup.
- Correct module imports.
- Normal network connections.
- Listening sockets.
- Missing process information.
- Permission errors.
- Invalid IP addresses.
- Firewall command failures.
- Repeated threat events.
- Graceful shutdown.

Use controlled test environments for security testing.

Do not test blocking functionality against unknown or third-party systems.

---

## 10. Immediate Development Task

The next development task is:

# Milestone 1: Live Network Connection Monitoring

The current system reports only connection counts.

The next implementation should upgrade the existing network monitor to display detailed network connection information.

Before writing code:

1. Inspect `modules/network_monitor.py`.
2. Inspect how `modules/threat_detector.py` uses the network monitor.
3. Identify existing functions and interfaces.
4. Preserve existing functionality.
5. Implement detailed connection monitoring.
6. Test the updated module.
7. Integrate it with the existing CyberSentinel controller.

Do not implement firewall blocking yet.

Do not replace the existing Threat Detector.

Do not rebuild the entire project.

Focus only on completing Milestone 1.

---

## 11. Final Development Goal

CyberSentinel should evolve into a reliable cybersecurity monitoring and traffic-control platform.

The development process must prioritize:

1. Reliable monitoring.
2. Accurate threat detection.
3. Useful security reporting.
4. Safe traffic control.
5. User authorization.
6. Stable system integration.
7. A clear browser-based interface.

Build the project carefully, one milestone at a time.

The immediate objective is to transform the current connection-counting monitor into a detailed live network monitoring system.