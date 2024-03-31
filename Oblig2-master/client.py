import socket
import argparse

def send_request(server_ip, server_port, filename):
    """
    Sends an HTTP request to the server and displays the server response.

    Parameters:
        server_ip (str): The IP address of the server.
        server_port (int): The port number of the server.
        filename (str): The name of the file to request from the server.

    Returns:
        None
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    request = f"GET /{filename} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
    client_socket.sendall(request.encode())

    response = client_socket.recv(4096).decode()
    print(response)

    client_socket.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP Client")
    parser.add_argument("-i", "--server_ip", help="Server IP Address", required=True)
    parser.add_argument("-p", "--server_port", help="Server Port", type=int, required=True)
    parser.add_argument("-f", "--filename", help="File Name", required=True)
    args = parser.parse_args()

    try:
        send_request(args.server_ip, args.server_port, args.filename)
    except Exception as e:
        print(f"Error occurred: {e}")
