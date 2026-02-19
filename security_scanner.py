import socket
import ssl
import requests
from datetime import datetime

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

def port_scan(target):
    print(f"\n[+] Starting Port Scan on {target}")
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"[OPEN] Port {port}")
            sock.close()
        except:
            pass

def check_headers(url):
    print("\n[+] Checking Security Headers")
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        security_headers = [
            "Content-Security-Policy",
            "X-Frame-Options",
            "Strict-Transport-Security",
            "X-Content-Type-Options",
            "Referrer-Policy"
        ]

        for header in security_headers:
            if header in headers:
                print(f"[OK] {header} present")
            else:
                print(f"[MISSING] {header}")
    except Exception as e:
        print("Error checking headers:", e)

def check_tls(target):
    print("\n[+] Checking TLS Version")
    try:
        context = ssl.create_default_context()
        with socket.create_connection((target, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                print("[OK] TLS Version:", ssock.version())
    except:
        print("[WARNING] Unable to verify TLS or HTTPS not supported")

def banner_grab(target, port):
    print(f"\n[+] Banner Grabbing on Port {port}")
    try:
        sock = socket.socket()
        sock.settimeout(2)
        sock.connect((target, port))
        banner = sock.recv(1024)
        print("[BANNER]", banner.decode(errors="ignore"))
        sock.close()
    except:
        print("No banner received.")

if __name__ == "__main__":
    target = input("Enter Target IP/Domain: ")
    url = f"http://{target}"

    print("\n==== Basic Security Scanner ====")
    print("Scan Started:", datetime.now())

    port_scan(target)
    check_headers(url)
    check_tls(target)
    banner_grab(target, 80)

    print("\nScan Completed.")
