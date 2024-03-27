import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    
    with conn:
        print("Connected to:", addr)
        data = conn.recv(1024)
        conn.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
    server_socket.close()

if __name__ == "__main__":
    main()
