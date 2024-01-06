import os.path
import socket
import time

import config


def listen_receive_file(local_ip):
    # 服务器地址和端口
    server_address = (local_ip, config.RECEIVE_DATA_PORT)

    # 创建TCP socket
    recive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定地址和端口
    recive_socket.bind(server_address)

    while True:
        # 监听连接
        recive_socket.listen(1)

        print(f"等待客户端连接在 {server_address} 上...")

        # 等待连接
        client_socket, client_address = recive_socket.accept()
        print(f"接受来自 {client_address} 的连接")

        # 接收文件名
        received_file_name = client_socket.recv(1024).decode('utf-8')
        print(f"接收文件名 {received_file_name}")

        # 接收文件
        data_path = os.path.join(config.RECEIVE_DATA_SAVE_PATH, received_file_name)
        # 记录传输速度
        received_bytes = 0
        with open(data_path, 'wb') as file:
            start_time = time.time()
            while True:
                data = client_socket.recv(config.CHUNK_SIZE)
                temp_time = time.time()
                received_bytes += len(data)
                if temp_time - start_time > 1:
                    print(f"传输速度: {received_bytes / 1024 / 1024 / (temp_time - start_time)} MB/s")
                    start_time = temp_time
                    received_bytes = 0
                if not data:
                    break
                file.write(data)

        print(f"文件 {received_file_name} 接收完成")

        # 关闭连接
        client_socket.close()


listen_receive_file()
