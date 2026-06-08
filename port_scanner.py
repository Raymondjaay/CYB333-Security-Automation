import socket
import sys
import time
from datetime import datetime

def validate_target(target_host):
    """Resolves hostname to IP addresses and verifies network target routing validity."""
    try:
        target_ip = socket.gethostbyname(target_host)
        return target_ip
    except socket.gaierror:
        print(f"\n[!] Error: Hostname '{target_host}' could not be resolved by DNS protocol.")
        return None

def fetch_service_banner(target_ip, port):
    """Attempts an aggressive application layer banner-grab to fulfill service discovery."""
    try:
        # Short timeout to keep scan highly performant
        banner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        banner_socket.settimeout(0.8)
        banner_socket.connect((target_ip, port))
        
        # Send raw carriage return to prompt a server response banner
        banner_socket.send(b'GET / HTTP/1.1\r\n\r\n')
        banner = banner_socket.recv(100).decode('utf-8', errors='ignore').strip()
        banner_socket.close()
        return banner.replace('\n', ' ')[:40] if banner else "Unknown Service Profile"
    except:
        return "Service responsive but suppressed banner"

def run_port_scanner():
    """Main interface loops for scanning network ports safely using user options."""
    print("=" * 60)
    print("         CYB333 SECURITY AUTOMATION PORT SCANNER        ")
    print("=" * 60)
    
    # User Configuration Input Phase
    target_host = input("[?] Enter Target Domain or Host IP Address: ").strip()
    if not target_host:
        print("[!] Input Validation Error: Destination cannot be blank.")
        return

    # Security Guardrails Validation Check
    # Restricts scanner inputs tightly to local system and nmap testing domains
    authorized_scopes = ['127.0.0.1', 'localhost', 'scanme.nmap.org']
    is_authorized = any(scope in target_host for scope in authorized_scopes)
    
    if not is_authorized:
        print("\n[CRITICAL VIOLATION] Execution Denied!")
        print("[!] Policy Notice: You are only authorized to scan localhost or scanme.nmap.org.")
        return

    # DNS Target Resolution
    target_ip = validate_target(target_host)
    if not target_ip:
        return

    # Range Configuration inputs with input validation error boundaries
    try:
        start_port = int(input("[?] Enter Starting Port Index (e.g., 1): "))
        end_port = int(input("[?] Enter Ending Port Index (e.g., 1000): "))
        
        if not (0 <= start_port <= 65535) or not (0 <= end_port <= 65535):
            print("[!] Range Boundary Exception: Port values must remain within 0-65535 range limits.")
            return
        if start_port > end_port:
            print("[!] Sequence Constraint Error: Start port cannot out-index end port configuration.")
            return
    except ValueError:
        print("[!] Input Failure: Port parameters must represent clear integers.")
        return

    # Adaptive Rate Limiting Scan Speed Input Configuration
    try:
        scan_delay = float(input("[?] Enter Scan Inter-packet Delay in seconds (e.g., 0.1 for stealth/safety): "))
    except ValueError:
        scan_delay = 0.0

    print("\n" + "-" * 50)
    print(f"[*] Scanning initiated against: {target_host} ({target_ip})")
    print(f"[*] Scan Scope Scope: Ports {start_port} through {end_port}")
    print(f"[*] Chronological Start Timestamp: {str(datetime.now())}")
    print("-" * 50)

    open_ports_discovered = 0
    total_ports_scanned = 0

    try:
        for port in range(start_port, end_port + 1):
            total_ports_scanned += 1
            
            # Create a localized clean socket context block per iteration 
            scan_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            # Configure restrictive timeout window for optimal balance of scanning speed and precision
            scan_socket.settimeout(0.5)
            
            # Attempt active connection check handshake return values
            result = scan_socket.connect_ex((target_ip, port))
            
            if result == 0:
                # 0 return value signifies open socket connection port state matches
                open_ports_discovered += 1
                print(f"[+] PORT OPEN: {port:<5} | Scanning Banner Fingerprint...")
                
                # Grab advanced service indicators details
                banner = fetch_service_banner(target_ip, port)
                print(f"    --> Details: {banner}")
            else:
                # Optional debug output configuration for small ranges (shows closed ports)
                if (end_port - start_port) <= 20:
                    print(f"[-] Port Closed: {port}")

            scan_socket.close()

            # Enforce the user-configured ethical timing constraints delay rate limit
            if scan_delay > 0:
                time.sleep(scan_delay)

    except KeyboardInterrupt:
        print("\n[-] User Request Interrupt: Halting scanner loops.")
    except socket.error as generic_socket_error:
        print(f"\n[!] Global Network Infrastructure Fault Intercepted: {generic_socket_error}")

    print("\n" + "=" * 50)
    print(f"[*] Diagnostic Execution Scan Complete.")
    print(f"[*] Evaluated Ports count: {total_ports_scanned}")
    print(f"[*] Confirmed Discovered Open Ports: {open_ports_discovered}")
    print(f"[*] Stop Timestamp: {str(datetime.now())}")
    print("=" * 50)

if __name__ == "__main__":
    run_port_scanner()