import socket
import sys
import threading
import csv
from datetime import datetime


class AdvancedPortScanner:
    def __init__(self, target: str, start_port: int, end_port: int, timeout: float = 0.5, threads: int = 50):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.threads = threads
        self.open_ports = []
        self.lock = threading.Lock()

    def scan_port(self, port: int):
        """Scan a single port and grab banner if open."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            result = s.connect_ex((self.target, port))

            if result == 0:
                service = self.get_service_name(port)
                banner = self.get_banner(s)
                with self.lock:
                    print(f"[+] Port {port} OPEN | Service: {service} | Banner: {banner}")
                    self.open_ports.append((port, service, banner))
            s.close()
        except Exception:
            pass

    def run_scan(self):
        """Run the scanning process with threading."""
        print(f"\n[*] Starting scan on target: {self.target}")
        print(f"[*] Port range: {self.start_port}-{self.end_port}")
        print(f"[*] Threads: {self.threads}")
        print(f"[*] Scan started at: {datetime.now()}\n")

        start_time = datetime.now()
        threads = []

        for port in range(self.start_port, self.end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()

            if len(threads) >= self.threads:
                for thr in threads:
                    thr.join()
                threads = []

        for thr in threads:
            thr.join()

        end_time = datetime.now()
        duration = end_time - start_time
        print(f"\n[*] Scan completed at: {end_time}")
        print(f"[*] Scan duration: {duration}\n")

        if not self.open_ports:
            print("[-] No open ports found.")
        else:
            print("[*] Summary of Open Ports:")
            for port, service, banner in self.open_ports:
                print(f"   Port {port} | Service: {service} | Banner: {banner}")

    def get_service_name(self, port: int) -> str:
        """Try to get the common service name for the port."""
        try:
            return socket.getservbyport(port)
        except OSError:
            return "Unknown"

    def get_banner(self, sock: socket.socket) -> str:
        """Try to grab banner from the open port."""
        try:
            sock.send(b"Hello\r\n")
            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner if banner else "No banner"
        except Exception:
            return "No banner"

    def reverse_dns(self):
        """Perform reverse DNS lookup for the target."""
        try:
            host, _, _ = socket.gethostbyaddr(self.target)
            return host
        except socket.herror:
            return "No reverse DNS found"

    def save_to_txt(self, filename="scan_results.txt"):
        """Save scan results to a text file."""
        try:
            with open(filename, "w") as f:
                f.write(f"Scan results for {self.target}\n")
                f.write(f"Port Range: {self.start_port}-{self.end_port}\n")
                f.write(f"Scan Time: {datetime.now()}\n\n")
                if not self.open_ports:
                    f.write("No open ports found.\n")
                else:
                    for port, service, banner in self.open_ports:
                        f.write(f"Port {port} | Service: {service} | Banner: {banner}\n")
            print(f"[*] Results saved to {filename}")
        except Exception as e:
            print(f"[-] Error saving TXT results: {e}")

    def save_to_csv(self, filename="scan_results.csv"):
        """Save scan results to a CSV file."""
        try:
            with open(filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Port", "Service", "Banner"])
                for port, service, banner in self.open_ports:
                    writer.writerow([port, service, banner])
            print(f"[*] Results saved to {filename}")
        except Exception as e:
            print(f"[-] Error saving CSV results: {e}")


def menu():
    print("=" * 70)
    print("             🔎 Advanced Python Port Scanner 🔎")
    print("=" * 70)
    target = input("Enter target IP (e.g. 127.0.0.1): ").strip()
    start_port = int(input("Enter start port (e.g. 1): "))
    end_port = int(input("Enter end port (e.g. 1024): "))
    timeout = float(input("Enter timeout (default 0.5): ") or 0.5)
    threads = int(input("Enter number of threads (default 50): ") or 50)

    scanner = AdvancedPortScanner(target, start_port, end_port, timeout, threads)

    print("\n[1] Run Scan")
    print("[2] Reverse DNS Lookup")
    print("[3] Run Scan + Save to TXT & CSV")
    choice = input("\nSelect an option: ")

    if choice == "1":
        scanner.run_scan()
    elif choice == "2":
        print(f"Reverse DNS: {scanner.reverse_dns()}")
    elif choice == "3":
        scanner.run_scan()
        scanner.save_to_txt()
        scanner.save_to_csv()
    else:
        print("Invalid choice. Exiting...")
        sys.exit()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n[-] User aborted scan.")
        sys.exit()
