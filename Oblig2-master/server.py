import socket
import os.path
import threading
import shutil

def handle_request(client_socket):
    """
    Handles incoming HTTP requests from clients.

    Parameters:
        client_socket (socket): The client socket object for communication.

    Returns:
        None
    """
    request_data = client_socket.recv(1024).decode()
    request_lines = request_data.split("\n")
    filename = request_lines[0].split()[1]

    if filename == "/":
        filename = "/index.html"

    filename = "server_files" + filename  # Assume server files are in "server_files" directory
    if os.path.isfile(filename):
        with open(filename, "rb") as f:
            content = f.read()
            response = b"HTTP/1.1 200 OK\r\n\r\n" + content
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

    client_socket.sendall(response)
    client_socket.close()


def run_server(host, port):
    """
    Runs the multi-threaded web server.

    Parameters:
        host (str): The IP address of the server.
        port (int): The port number to listen on.

    Returns:
        None
    """
    if not os.path.exists("server_files"):
        os.makedirs("server_files")
    if not os.path.exists("server_files/index.html"):
        shutil.move("index.html", "server_files/index.html")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        client_thread = threading.Thread(target=handle_request, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    host = "127.0.0.1"  # Change to your desired host IP
    port = 8000  # Change to your desired port number
    run_server(host, port)
