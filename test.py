import socket
import threading

def handle_client(client_socket):
    # 处理客户端请求的线程函数
    request = client_socket.recv(1024)  # 接收请求信息
    # 处理请求逻辑，例如接收文件
    # ...

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12345))  # 服务器监听地址和端口
    server.listen(5)  # 最大连接数

    print('[*] Server listening on port 12345')

    while True:
        client_socket, addr = server.accept()
        print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()