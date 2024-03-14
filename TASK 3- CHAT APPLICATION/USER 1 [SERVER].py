import socket
import threading

# Function to handle client connections
def handle_client(client_socket, addr, user):
    print(f"[NEW CONNECTION] {user} connected from {addr}.")

    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"[DISCONNECTED] {user} disconnected.")
                break
            print(f"[{user}] {message}")

            # Broadcast message to all clients
            broadcast(message, addr, user)
        except:
            print(f"[ERROR] Connection with {user} lost.")
            client_socket.close()
            break

# Function to broadcast message to all clients
def broadcast(message, sender_addr, sender_name):
    for client in clients:
        if client[1] != sender_addr:
            client[0].send(f"[{sender_name}] {message}".encode())

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

print("[STARTING] Server is starting...")

clients = []

# Assign user names
server_name = "User 1"

# Function for server input
def server_input():
    while True:
        message = input()
        broadcast(f"[{server_name}] {message}", ("localhost", 5555), server_name)  # Broadcast server message

# Start a thread for server input
input_thread = threading.Thread(target=server_input)
input_thread.start()

# Accept incoming connections
while True:
    client_socket, addr = server.accept()
    user_name = "User 2"
    clients.append((client_socket, addr, user_name))
    
    # Start a thread for each client
    thread = threading.Thread(target=handle_client, args=(client_socket, addr, user_name))
    thread.start()

    # Example: Server sends a welcome message to the newly connected client
    welcome_message = f"Welcome to the chat server, {user_name}!"
    client_socket.send(welcome_message.encode())
