import socket
import sys
import time

def start_client(host='127.0.0.1', port=65432):
    """
    Initializes a TCP client, attempts to connect to the targeted server, 
    manages user input transmissions, and handles connectivity errors.
    """
    # Initialize the IPv4 TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"[*] Attempting to establish socket connection with remote host {host}:{port}...")
    try:
        client_socket.connect((host, port))
        print("[+] Network pathway established. Connected to server.")
        
        # Test Case 1 & 2: Loop to handle multi-turn communication
        while True:
            user_input = input("\nEnter data message to send to server (or type 'exit' to quit): ")
            
            if not user_input.strip():
                print("[!] Message payload cannot be null/empty. Try again.")
                continue

            # Transmit data payload over active socket channel
            client_socket.sendall(user_input.encode('utf-8'))
            
            if user_input.lower().strip() == 'exit':
                print("[-] Disconnection instruction initiated. Terminating pipeline.")
                break

            # Await transmission back from server infrastructure
            server_response = client_socket.recv(1024)
            if not server_response:
                print("[!] Connection with server lost abruptly.")
                break
                
            print(f"[Response] From Server -> {server_response.decode('utf-8')}")

    except ConnectionRefusedError:
        # Satisfies test case requirement for showing inactive server behavior
        print("[!] Connection Failure: Target server refused connection package.")
        print("[!] Troubleshooting Tip: Ensure server.py is executing active listening loops first.")
    except socket.error as e:
        print(f"[!] General Network Pipeline Exception: {e}")
    finally:
        client_socket.close()
        print("[*] Client operations closed. Environment flushed.")

if __name__ == "__main__":
    start_client()
    