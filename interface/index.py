from flask import Blueprint, render_template, request
from network.NIC import get_nic_list, find_unused_port
from network.utils import send_file_2

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route('/index')
def index():
    return render_template('index.html')


@index_blueprint.route('/get_all_nic_info')
def get_all_nic_info():
    return get_nic_list()


@index_blueprint.route('/get_unused_port')
def get_unused_port():
    return find_unused_port()


@index_blueprint.post('/send_file')
def send_file():
    file = request.files['file']
    sender_ip = request.form['sender_ip']
    receiver_ip = request.form['receiver_ip']
    file_size = request.form['file_size']
    send_file_2(sender_ip, receiver_ip, file, file_size)
    return {'status': 'success', 'message': '文件上传成功！'}
