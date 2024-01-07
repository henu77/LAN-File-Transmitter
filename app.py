import argparse
import os

from flask import Flask, send_from_directory

import config
from interface.index import index_blueprint
from interface.login import login_blueprint

app = Flask(__name__, static_folder='templates/static', template_folder='templates')

app.register_blueprint(index_blueprint)
app.register_blueprint(login_blueprint)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path),
                               'templates/static/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    # 获取参数
    parser = argparse.ArgumentParser(description='局域网文件传输工具')

    # 添加位置参数（Positional Arguments）
    parser.add_argument('-p', '--port', type=int, default=None, help='前端页面运行的端口号')

    args = parser.parse_args()
    port = args.port if args.port else config.PORT

    app.run(debug=True, port=port)
