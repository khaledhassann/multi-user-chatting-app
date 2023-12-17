import socket
import threading

# Server configuration
SERVER_HOST = '0.0.0.0' # this is so any computer on the network can connect to the server
SERVER_PORT = 5555

# Simple username-password database (in-memory for the sake of simplicity)
user_database = {'user1': 'password1', 'user2': 'password2'}


def handle_client(client_socket):
    # Receive username
    username = client_socket.recv(1024).decode('utf-8')

    # Check if the username exists in the database
    if username in user_database:
        # Send a message to the client for password
        client_socket.send('SEND_PASSWORD'.encode('utf-8'))

        # Receive password
        password = client_socket.recv(1024).decode('utf-8')

        # Check if the password matches
        if password == user_database[username]:
            client_socket.send('AUTH_SUCCESS'.encode('utf-8'))
            print(f"Authentication successful for {username}")
        else:
            client_socket.send('AUTH_FAIL'.encode('utf-8'))
            print(f"Authentication failed for {username}")
    else:
        client_socket.send('USER_NOT_FOUND'.encode('utf-8'))
        print(f"User {username} not found")

    # Close the connection
    client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()