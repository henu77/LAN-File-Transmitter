import os.path
import socket
import time

import config


def send_file(local_ip, file_path, remote_ip):
    # 判断文件是否存在
    if not os.path.exists(file_path):
        return {'status': 'error', 'message': '文件不存在！'}

    # 创建TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定本地IP和端口
    client_socket.bind((local_ip, 0))

    # 连接远程IP和端口
    client_socket.connect((remote_ip, config.RECEIVE_DATA_PORT))
    # 发送文件名
    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode('utf-8'))

    # 记录传输速度
    send_bytes = 0
    start_time = time.time()
    # 发送文件
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(1024)
            if not data:
                break
            client_socket.send(data)
            temp_time = time.time()
            send_bytes += len(data)
            if temp_time - start_time > 1:
                print(f"传输速度: {send_bytes / 1024 / 1024 / (temp_time - start_time)} MB/s")
                start_time = temp_time
                send_bytes = 0
    client_socket.close()


from werkzeug.datastructures import FileStorage

global send_file_progress
global send_file_speed
global send_file_required_time


def send_file_2(local_ip, remote_ip, file: FileStorage, file_size):
    # 创建TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定本地IP和端口
    client_socket.bind((local_ip, 0))
    print(f"请求连接 {remote_ip}:{config.RECEIVE_DATA_PORT}")
    # 连接远程IP和端口
    client_socket.connect((remote_ip, config.RECEIVE_DATA_PORT))
    print(f"连接到 {remote_ip}:{config.RECEIVE_DATA_PORT}")
    # 发送文件名
    file_name = file.filename
    print(f"发送文件名 {file_name}")

    client_socket.send(file_name.encode('utf-8'))
    print(file_name.encode('utf-8'))

    # 接收对方回应
    client_socket.recv(1024)
    # 记录传输速度
    send_bytes = 0
    start_time = time.time()

    global send_file_progress
    global send_file_speed
    global send_file_required_time
    send_file_progress = 0
    send_file_speed = 0
    send_file_required_time = 0
    # 发送文件
    while True:
        data = file.read(config.CHUNK_SIZE)
        if not data:
            break
        client_socket.send(data)
        temp_time = time.time()
        send_bytes += len(data)
        send_file_progress = send_bytes / int(file_size)
        if temp_time - start_time > 1:
            send_file_speed = send_bytes / 1024 / 1024 / (temp_time - start_time)
            send_file_required_time = (int(file_size) - send_bytes) / 1024 / 1024 / send_file_speed
    client_socket.close()
    print(f"文件 {file_name} 发送完成")
    print(f"关闭连接 {remote_ip}")


def get_send_file_progress():
    # 如果没有发送文件，返回0
    try:
        # 尝试访问变量
        value = globals()['send_file_progress']
        # 如果访问成功，说明变量已定义
        return round(send_file_progress * 100, 2)
    except KeyError:
        # 如果访问失败，捕获 NameError 异常，说明变量未定义
        return 0

def get_send_file_speed_required_time():
    # 如果没有发送文件，返回0
    try:
        # 尝试访问变量
        value = globals()['send_file_speed']
        # 如果访问成功，说明变量已定义
        return {'speed': round(send_file_speed, 2), 'time': round(send_file_required_time, 2)}
    except KeyError:
        return {'speed': 0, 'time': 0}


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
        client_socket.send(b'ok')
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
                    print(f"接收速度: {received_bytes / 1024 / 1024 / (temp_time - start_time)} MB/s")
                    start_time = temp_time
                    received_bytes = 0
                if not data:
                    break
                file.write(data)

        print(f"文件 {received_file_name} 接收完成")

        # 关闭连接
        client_socket.close()
        print(f"关闭连接 {client_address}")
