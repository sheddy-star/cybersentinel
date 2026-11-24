
import psutil
import socket


class NetworkMonitor:

    def __init__(self):
        self.connections = []

    def get_network_info(self):

        connections = psutil.net_connections(kind="inet")

        self.connections = []

        for connection in connections:

            if connection.status == "ESTABLISHED":

                local_address = connection.laddr
                remote_address = connection.raddr

                self.connections.append({
                    "local_ip": local_address.ip if local_address else "Unknown",
                    "local_port": local_address.port if local_address else "Unknown",
                    "remote_ip": remote_address.ip if remote_address else "Unknown",
                    "remote_port": remote_address.port if remote_address else "Unknown",
                    "status": connection.status,
                    "protocol": (
                        "TCP"
                        if connection.type == socket.SOCK_STREAM
                        else "UDP"
                    )
                })

        return self.connections

    def display_connections(self):

        print("\n--- NETWORK MONITORING ---")

        try:
            connections = self.get_network_info()

            print(f"Active Connections: {len(connections)}")

            for connection in connections:

                print(
                    f"{connection['local_ip']}:{connection['local_port']} "
                    f"-> {connection['remote_ip']}:{connection['remote_port']} "
                    f"| {connection['status']} "
                    f"| {connection['protocol']}"
                )

        except psutil.AccessDenied:

            print("Permission denied: Cannot access all network connections.")

        except psutil.Error as error:

            print(f"Network monitoring error: {error}")
