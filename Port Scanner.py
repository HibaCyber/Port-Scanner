import socket
import sys
from datetime import datetime

# Function to scan ports
def port_scanner(target, start_port, end_port):
    print(f"\nScanning Target: {target}")
    print(f"Scanning started at: {datetime.now()}\n")

    # Loop through ports
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)  # timeout for faster scanning
        result = s.connect_ex((target, port))  # returns 0 if port is open

        if result == 0:
            print(f"[+] Port {port} is OPEN")
        s.close()

    print("\nScan Completed.")

# Main function
if __name__ == "__main__":
    # Example: user input for target and port range
    target = input("Enter target IP (e.g. 127.0.0.1): ").strip()
    start_port = int(input("Enter start port (e.g. 1): "))
    end_port = int(input("Enter end port (e.g. 1024): "))

    try:
        port_scanner(target, start_port, end_port)
    except KeyboardInterrupt:
        print("\nExiting Program.")
        sys.exit()
    except socket.gaierror:
        print("Hostname could not be resolved.")
        sys.exit()
    except socket.error:
        print("Couldn't connect to server.")
        sys.exit()
