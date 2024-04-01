import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    
    with conn:
        print(f"Connected to: {addr}")
        data = conn.recv(1024).decode()
        print(f"Receive data: {data}")
        path = data.split()[1]
        path_elements = path.split("/")
        path_type = path_elements[1]
        if path_type == "echo":
            random_msg = ""
            for i in range(2, len(path_elements)):
                random_msg += path_elements[i]
                if i < len(path_elements) - 1:
                    random_msg += "/"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_msg)}\r\n\r\n{random_msg}"
            conn.sendall(response.encode())
        else:
            if path == "/":
                conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
        conn.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    server_socket.close()

if __name__ == "__main__":
    main()
