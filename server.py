import socket
import threading

# Server configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))  # Server IP and port
server_socket.listen(5)

print("Server started. Waiting for connections...")

# List to keep track of client connections
clients = []

# Function to handle client connections
def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Received message from {client_address}: {message}")
            
            # Broadcast message to all clients
            for client in clients:
                if client is not client_socket:
                    try:
                        client.send(message.encode())
                    except:
                        clients.remove(client)
        client_socket.close()
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
        client_socket.close()

# Function to accept incoming connections
def accept_connections():
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} established.")
            
            # Add client to list
            clients.append(client_socket)
            
            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except Exception as e:
        print(f"Error accepting connections: {e}")
    finally:
        server_socket.close()

# Start accepting connections
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()
