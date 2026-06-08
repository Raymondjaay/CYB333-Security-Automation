import socket
import sys

def start_server(host='127.0.0.1', port=65432):
    """
    Initializes a TCP server, binds to localhost, listens for incoming 
    connections, and echoes back received messages with formatting.
    """
    # Create a TCP/IP socket using IPv4 addressing (AF_INET) and TCP protocol (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow immediate reuse of the socket port after shutdown to prevent "Address already in use" errors
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1) # Listen for 1 unaccepted connection before refusing new ones
        print(f"[*] Server successfully initialized and listening on {host}:{port}")
        print("[*] Awaiting connection from client...")

        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"[+] Connection established with client from host address: {client_address}")

        while True:
            # Receive data up to 1024 bytes buffer size
            data = client_socket.recv(1024)
            if not data:
                # If recv returns empty bytes, it indicates a clean disconnection from the client
                print("[-] Client closed the connection protocol.")
                break
            
            # Decode bytes back into string format for processing
            decoded_message = data.decode('utf-8')
            print(f"[Received] Client data payload: '{decoded_message}'")

            # Process custom exit commands gracefully
            if decoded_message.lower().strip() == 'exit':
                print("[*] Exit command acknowledged. Initiating termination...")
                break

            # Format response payload (Exceeds Expectations feature)
            response = f"SERVER_ACK: Packet received successfully. Payload length: {len(decoded_message)} bytes"
            client_socket.sendall(response.encode('utf-8'))

    except KeyboardInterrupt:
        print("\n[-] Server execution interrupted via keyboard (Ctrl+C). Exiting.")
    except socket.error as error_msg:
        print(f"[!] Critical socket architecture error encountered: {error_msg}")
    finally:
        # Guarantee cleanup of open file descriptors on shutdown
        if 'client_socket' in locals():
            client_socket.close()
        server_socket.close()
        print("[*] Server sockets released. Shutdown sequence complete.")

if __name__ == "__main__":
    start_server()