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
        path_type = path.split("/")[1]
        if path_type == "echo":
            random_msg = path_type.split("/")[2]
            conn.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 3\r\n\r\n{random_msg}".encode())
        else:
            if path == "/":
                conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
        conn.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    server_socket.close()

if __name__ == "__main__":
    main()
