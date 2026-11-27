import time
import socket
import logging

import psutil


class NetworkMonitor:
    def __init__(self):
        self.connections = []
        self.previous_connections = set()
        self.initial_scan = True

        # Optional callback for sending events to CyberSentinel
        self.event_callback = None

        self.logger = logging.getLogger("CyberSentinel.NetworkMonitor")

    def get_network_info(self):
        """
        Get currently established TCP connections.

        Each connection includes:
        - Local IP and port
        - Remote IP and port
        - Connection state
        - Process ID and process name, when available
        """

        current_connections = []

        try:
            connections = psutil.net_connections(kind="tcp")

            for connection in connections:
                if connection.status != psutil.CONN_ESTABLISHED:
                    continue

                local_address = connection.laddr
                remote_address = connection.raddr

                if not local_address or not remote_address:
                    continue

                process_name = "Unknown"
                process_id = connection.pid

                if process_id:
                    try:
                        process_name = psutil.Process(process_id).name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = "Unknown"

                connection_info = {
                    "protocol": "TCP",
                    "local_ip": local_address.ip,
                    "local_port": local_address.port,
                    "remote_ip": remote_address.ip,
                    "remote_port": remote_address.port,
                    "status": connection.status,
                    "pid": process_id,
                    "process": process_name,
                }

                current_connections.append(connection_info)

        except psutil.AccessDenied:
            self.logger.warning(
                "Permission denied while reading network connections."
            )

        except psutil.Error as error:
            self.logger.error(
                "Network monitoring error: %s",
                error
            )

        self.connections = current_connections

        return current_connections

    def get_connection_key(self, connection):
        """
        Create a unique identifier for a TCP connection.
        """

        return (
            connection["protocol"],
            connection["local_ip"],
            connection["local_port"],
            connection["remote_ip"],
            connection["remote_port"],
        )

    def send_event(self, event):
        """
        Send a network event to CyberSentinel if a callback is configured.
        """

        if self.event_callback:
            try:
                self.event_callback(event)

            except Exception as error:
                self.logger.error(
                    "Network event callback failed: %s",
                    error
                )

    def detect_connection_changes(self, current_connections):
        """
        Compare the current connections with the previous scan.

        Detect:
        - Newly established connections
        - Connections that have disappeared
        """

        current_connection_map = {
            self.get_connection_key(connection): connection
            for connection in current_connections
        }

        current_keys = set(current_connection_map.keys())

        # First scan establishes the baseline.
        if self.initial_scan:
            self.previous_connections = current_keys
            self.initial_scan = False

            print(
                f"[NETWORK] Initial baseline recorded: "
                f"{len(current_keys)} established TCP connections"
            )

            return

        new_connections = (
            current_keys - self.previous_connections
        )

        closed_connections = (
            self.previous_connections - current_keys
        )

        # Report new connections.
        for connection_key in new_connections:
            connection = current_connection_map[connection_key]

            event = {
                "event_type": "new_connection",
                "connection": connection,
                "timestamp": time.time(),
            }

            print("\n[NEW TCP CONNECTION DETECTED]")
            print(
                f"Local:  {connection['local_ip']}:"
                f"{connection['local_port']}"
            )
            print(
                f"Remote: {connection['remote_ip']}:"
                f"{connection['remote_port']}"
            )
            print(f"Process: {connection['process']}")
            print(f"PID: {connection['pid']}")
            print(f"State: {connection['status']}")

            self.logger.info(
                "New TCP connection: %s:%s -> %s:%s | Process: %s | PID: %s",
                connection["local_ip"],
                connection["local_port"],
                connection["remote_ip"],
                connection["remote_port"],
                connection["process"],
                connection["pid"],
            )

            self.send_event(event)

        # Report connections that disappeared.
        for connection_key in closed_connections:
            event = {
                "event_type": "connection_closed",
                "connection_key": connection_key,
                "timestamp": time.time(),
            }

            print(
                "\n[ TCP CONNECTION CLOSED ] "
                f"{connection_key[1]}:{connection_key[2]} -> "
                f"{connection_key[3]}:{connection_key[4]}"
            )

            self.logger.info(
                "TCP connection closed: %s",
                connection_key
            )

            self.send_event(event)

        self.previous_connections = current_keys

    def display_connections(self):
        """
        Display established connections and detect changes.
        This method can be called repeatedly by the main controller.
        """

        try:
            connections = self.get_network_info()

            print("\n--- CYBERSENTINEL NETWORK MONITOR ---")
            print(
                f"Established TCP Connections: {len(connections)}"
            )

            self.detect_connection_changes(connections)

        except Exception as error:
            self.logger.error(
                "Failed to display network connections: %s",
                error
            )

    def monitor_live_connections(self, interval=2):
        """
        Continuously monitor connections.

        Use this method only when running the monitor directly.
        The main CyberSentinel controller should use its own thread.
        """

        print("[NETWORK] Live connection monitoring started.")

        try:
            while True:
                self.display_connections()
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n[NETWORK] Monitoring stopped.")

    def get_listening_ports(self):
        """
        Return TCP ports currently listening on this computer.
        """

        listening_ports = []

        try:
            connections = psutil.net_connections(kind="tcp")

            for connection in connections:
                if connection.status != psutil.CONN_LISTEN:
                    continue

                if not connection.laddr:
                    continue

                listening_ports.append({
                    "ip": connection.laddr.ip,
                    "port": connection.laddr.port,
                    "pid": connection.pid,
                })

        except psutil.AccessDenied:
            self.logger.warning(
                "Permission denied while reading listening ports."
            )

        return listening_ports


if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.monitor_live_connections(interval=2)