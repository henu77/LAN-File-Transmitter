import threading

from flask import Blueprint, render_template, request

import config
from model.Response import Response
from network.utils import listen_receive_file

login_blueprint = Blueprint('login', __name__)

listen_thread_dict = {}


@login_blueprint.route('/')
def login():
    return render_template('login.html')


@login_blueprint.route('/start_listen_sender_ip')
def start_listen_sender_ip():
    local_ip = request.args.get('local_ip')
    if not local_ip:
        return Response(config.ERROR_CODE, '缺少参数 local_ip', None).to_json()
    if local_ip in listen_thread_dict:
        return Response(config.ERROR_CODE, '该IP已经在监听', None).to_json()
    local_ip = request.args.get('local_ip')
    # 开启一个线程监听发送端的IP
    listen_thread = threading.Thread(target=listen_receive_file, args=(local_ip,))
    listen_thread_dict[local_ip] = listen_thread
    listen_thread.start()
    return Response(config.SUCCESS_CODE, '开始监听发送端IP', None).to_json()
