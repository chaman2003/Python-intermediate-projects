import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except Exception as e:
            print("[ERROR]", e)
            break

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

# Main loop to send messages
first_message_received = False
while True:
    message = input()
    client.send(message.encode())
    
    # Check if this is the first message from the server
    if not first_message_received:
        print(f"[User 1] Welcome to the chat server!")
        first_message_received = True
