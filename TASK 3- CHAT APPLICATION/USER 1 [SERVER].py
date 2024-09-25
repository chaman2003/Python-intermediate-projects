import socket
import threading

def handle_client(client_socket, addr, user):
    print(f"[NEW CONNECTION] {user} connected from {addr}.")

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"[DISCONNECTED] {user} disconnected.")
                break
            print(f"[{user}] {message}")

            broadcast(message, addr, user)
        except:
            print(f"[ERROR] Connection with {user} lost.")
            client_socket.close()
            break

def broadcast(message, sender_addr, sender_name):
    for client in clients:
        if client[1] != sender_addr:
            client[0].send(f"[{sender_name}] {message}".encode())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5555))
server.listen()

print("[STARTING] Server is starting...")

clients = []

server_name = "User 1"

def server_input():
    while True:
        message = input()
        broadcast(f"[{server_name}] {message}", ("localhost", 5555), server_name) 

input_thread = threading.Thread(target=server_input)
input_thread.start()

while True:
    client_socket, addr = server.accept()
    user_name = "User 2"
    clients.append((client_socket, addr, user_name))
    
    thread = threading.Thread(target=handle_client, args=(client_socket, addr, user_name))
    thread.start()

    welcome_message = f"Welcome to the chat server, {user_name}!"
    client_socket.send(welcome_message.encode())
