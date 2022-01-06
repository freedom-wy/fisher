from flask import render_template
from .blueprint import web


@web.route('/')
def index():
    return 'index'


@web.route('/personal')
def personal_center():
    return 'personal'
