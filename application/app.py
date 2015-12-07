# coding=utf-8

from flask import (Flask, request, make_response, render_template, Response)
from handler import *


app = Flask(__name__.split('.')[0])

@app.route(r'/tiantian', methods=['GET', 'POST'])
def handle():
    if request.method == 'GET':
        return check_signature(request)
    if request.method == 'POST':
        return handle_client(request)
    return Response(status=403)
