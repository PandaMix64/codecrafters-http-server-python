from pathlib import Path
import socket
import sys
from .http_utils import HttpRequest, HttpResponse
import threading

def main(dir = None):
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    
    try:
        while True:
            conn, addr = server_socket.accept() # wait for client
            print(f"Connected to: {addr}")
            client_thread = threading.Thread(target=process_client, args=[conn, dir])
            client_thread.start()
    finally:
        server_socket.close()

def process_client(conn:socket.socket, dir = None):
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
            file = None
            given_path = None
            if dir:
                local_path = local_path[1:]
                given_path = Path(dir + local_path)
                if given_path.is_file():
                    file = given_path
            try:
                if http_request.method == "POST":
                    with open(str(given_path.absolute()), "x") as new_file:
                        new_file.write(http_request.body)
                        headers = {}
                        headers["Content-Length"] = len(http_request.body)
                        conn.sendall(response.process_post(http_request.body, "application/octet-stream", headers=headers).encode())
                        return
                if file:
                    content = file.read_text()
                    conn.sendall(response.process_get(content, "application/octet-stream").encode())
                else:
                    with open(local_path, "r") as file:
                        print("success")
                        content = file.read()
                        conn.sendall(response.process_get(content, "application/octet-stream").encode())
            except (FileNotFoundError, IsADirectoryError, FileExistsError) as err:
                print("failed", err)
                conn.sendall(response.not_found().encode())
        case _:
            if path == "/":
                conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
            else:
                conn.sendall(response.not_found().encode())

if __name__ == "__main__":
    args = sys.argv
    dir = None
    for i in range(len(args)):
        if args[i] == "--directory":
            dir = args[i + 1] # Getting next value wich should be the directory
    main(dir)