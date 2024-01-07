from flask import Blueprint, render_template, request

import config
from model.Response import Response
from network.NIC import get_nic_list, find_unused_port
from network.utils import send_file_2, get_send_file_progress, get_send_file_speed_required_time

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index')
def index():
    return render_template('index.html')


@index_blueprint.get('/get_all_nic_info')
def get_all_nic_info():
    return get_nic_list()


@index_blueprint.get('/get_unused_port')
def get_unused_port():
    return find_unused_port()


@index_blueprint.post('/send_file')
def send_file():
    file = request.files['file']
    sender_ip = request.form['sender_ip']
    receiver_ip = request.form['receiver_ip']
    file_size = request.form['file_size']
    send_file_2(sender_ip, receiver_ip, file, file_size)
    return Response(config.SUCCESS_CODE, '发送成功', None).to_json()


@index_blueprint.get('/get_send_file_progress')
def get_send_progress():
    return Response(config.SUCCESS_CODE, '获取成功', get_send_file_progress()).to_json()


@index_blueprint.get('/get_send_file_speed_required_time')
def get_send_speed_required_time():
    return Response(config.SUCCESS_CODE, '获取成功', get_send_file_speed_required_time()).to_json()
