import socket

import psutil

import config
from model.Response import Response


class NIC(object):
    def __init__(self, name, mac, ip, netmask, isup, speed, mtu):
        self.name = name
        self.mac = mac
        self.ip = ip
        self.netmask = netmask
        self.isup = isup
        self.speed = speed
        self.mtu = mtu

    def __str__(self):
        return f"网卡名称: {self.name}\n" \
               f"MAC 地址: {self.mac}\n" \
               f"IP 地址: {self.ip}\n" \
               f"子网掩码: {self.netmask}\n" \
               f"是否启动: {self.isup}\n" \
               f"网卡速度: {self.speed}\n" \
               f"MTU: {self.mtu}"

    def to_json(self):
        return {
            "name": self.name,
            "mac": self.mac,
            "ip": self.ip,
            "netmask": self.netmask,
            "isup": self.isup,
            "speed": self.speed,
            "mtu": self.mtu
        }


def get_nic_list():
    global mac
    nic_info_list = psutil.net_if_stats()
    nic_list = []
    for interface, stats in nic_info_list.items():
        if stats.isup:
            nic = psutil.net_if_addrs()[interface]
            for item in nic:
                if item.family == psutil.AF_LINK:
                    # 硬件地址
                    mac = item.address
                elif item.family == 2:
                    # IPv4地址
                    nic_list.append(
                        NIC(interface, mac, item.address,
                            item.netmask, stats.isup, stats.speed,
                            stats.mtu).to_json())
    return Response(config.SUCCESS_CODE, '获取网卡信息列表成功', nic_list).to_json()


def find_unused_port(ip='localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, 0))
        _, port = s.getsockname()
    return Response(config.ERROR_CODE, '获取未使用端口成功', {'port': port}).to_json()
