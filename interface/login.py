from flask import Blueprint, render_template

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/')
def login():
    return render_template('login.html')
