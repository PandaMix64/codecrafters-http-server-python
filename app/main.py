import socket
import os
from .http_utils import HttpRequest, HttpResponse
import threading

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    try:
        while True:
            conn, addr = server_socket.accept() # wait for client
            print(f"Connected to: {addr}")
            client_thread = threading.Thread(target=process_client, args=[conn])
            client_thread.start()
    finally:
        server_socket.close()

def process_client(conn):
    data = conn.recv(1024).decode()
    print(f"Receive data: {data}")
    path = data.split()[1]
    path_elements = path.split("/")
    path_type = path_elements[1]
    
    #Parsing string to object
    http_request = HttpRequest(data)
    response = HttpResponse(http_request)
    match path_type:
        case "echo":
            msg = ""
            for i in range(2, len(path_elements)):
                msg += path_elements[i]
                if i < len(path_elements) - 1:
                    msg += "/"
            conn.sendall(response.process_get(msg).encode())
        case "user-agent":
            msg = http_request.headers[path_type]
            conn.sendall(response.process_get(msg).encode())
        case "files":
            if len(path_elements) <= 2:
                path_elements.append("/")
            if path_elements[2] == "":
                path_elements[2] = "/"
            local_path = "."
            for i in range(2, len(path_elements)):
                if not path_elements[i] == "/":
                    local_path += "/"
                local_path += path_elements[i]
            try:
                with open(local_path, "r") as file:
                    content = file.read()
                    conn.sendall(response.process_get(content, "application/octet-stream").encode())
            except (FileNotFoundError, IsADirectoryError):
                conn.sendall(response.not_found().encode())
        case _:
            if path == "/":
                conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
            else:
                conn.sendall(response.not_found().encode())

if __name__ == "__main__":
    main()