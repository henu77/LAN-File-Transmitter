# import psutil
# import socket
# d = psutil.net_if_addrs()
# def print_network_info():
#     for n, a in psutil.net_if_addrs().items():
#         for item in a:
#             if item.family == 2:
#                 print("接口: {}, IPv4 地址: {}".format(n, item.address))
#     # 获取网卡信息
#     gateway_info = psutil.net_if_stats()
#     for network, stats in gateway_info.items():
#         if stats.isup:
#             gateway = stats.gateway
#             print(f"接口 {network} 的网关地址: {gateway}")
#     dns_addresses = []
#     for info in socket.getaddrinfo(socket.gethostname(), None):
#         if info[0] == socket.AF_INET:
#             dns_addresses.append(info[4][0])
#
#     print(f"系统DNS服务器地址: {', '.join(dns_addresses)}")
#
# print_network_info()
#
# import socket
#
#
# def get_unused_port():
#     # 创建一个套接字
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     # 绑定到端口0上
#     sock.bind(('10.166.216.249', 0))
#     # 获取这个套接字的端口
#     port = sock.getsockname()[1]
#     # 关闭套接字
#     sock.close()
#
#     # 返回端口号
#     return port
#
#
# # 调用函数
# port = get_unused_port()
# print("未被使用的端口号是:", port)
from network.NIC import get_nic_list
for i in get_nic_list():
    print(i)
print(get_nic_list())
