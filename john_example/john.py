import socket

# Server configuration
SERVER_HOST = '0.0.0.0' # client should change this to the ip address of the server
SERVER_PORT = 5555

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Get username from user
    username = input("Enter username: ")
    client_socket.send(username.encode('utf-8'))

    # Receive authentication message
    auth_message = client_socket.recv(1024).decode('utf-8')

    if auth_message == 'SEND_PASSWORD':
        # Get password from user
        password = input("Enter password: ")
        client_socket.send(password.encode('utf-8'))

        # Receive authentication result
        auth_result = client_socket.recv(1024).decode('utf-8')

        if auth_result == 'AUTH_SUCCESS':
            print("Authentication successful!")
        else:
            print("Authentication failed.")
    elif auth_message == 'USER_NOT_FOUND':
        print("User not found.")
    else:
        print("Unexpected response from server.")

    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    main()