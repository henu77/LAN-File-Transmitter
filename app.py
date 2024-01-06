import os
import threading

from flask import Flask, send_from_directory, request

import config
from interface.index import index_blueprint
from interface.login import login_blueprint
from model.Response import Response
from network.utils import listen_receive_file

app = Flask(__name__, static_folder='templates/static', template_folder='templates')

app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)

listen_thread_dict = {}


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path),
                               'templates/static/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/start_listen_sender_ip')
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


if __name__ == '__main__':
    app.run(debug=True, port=config.PORT)
