# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import send_file
from flask import session
from flask import url_for


from qtlweb import utils

import ntpath
import os
import socket


page = Blueprint('page', __name__, template_folder='templates')


@page.route('/ping')
def ping():
    return 'OK!!!!'


@page.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@page.route('/login', methods=['GET', 'POST'])
def login():
    #print(request.form.get('frm_id'))
    #print(request.form.get('frm_pwd'))

    #print(current_app.config['LOGIN_USERID'])
    #print(current_app.config['LOGIN_PASSWORD'])

    if request.form.get('frm_pwd') == current_app.config['LOGIN_PASSWORD'] and \
            request.form.get('frm_id') == current_app.config['LOGIN_USERID']:
        session['auth'] = True
        session['auth_message'] = False
    else:
        session['auth'] = False
        session['auth_message'] = True

    if request.method == 'GET':
        # don't display a message if calling login directly
        session['auth_message'] = False

    return redirect(url_for('page.index'))


@page.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('page.index'))


@page.route('/')
def index():
    # POST search_term = request.form.get("search_term")
    # GET  search_term = request.args.get("search_term")
    # BOTH search_term = request.values.get("search_term")

    search_term = request.values.get('search_term', '')
    datasetid = request.values.get('datasetid', '')
    debug = utils.str2bool(request.values.get('debug', ''))
    admin = utils.str2bool(request.values.get('admin', ''))
    app_version = os.getenv('DOCKER_QTLWEB_VERSION', '')

    if current_app.config['LOGIN_REQUIRED'] and not session.get('auth'):
        #print('session.get("auth")')
        #print(session.get('auth'))
        return render_template('page/login.html', debug=debug)

    return render_template('page/index.html',
                           search_term=search_term, datasetid=datasetid,
                           debug=debug, app_version=app_version, admin=admin)


'''
@page.route('/')
def home():
    print('CALL to /')
    # POST search_term = request.form.get("search_term")
    # GET  search_term = request.args.get("search_term")
    # BOTH search_term = request.values.get("search_term")
    search_term = request.values.get('search_term', '')
    datasetid = request.values.get('datasetid', '')

    print(request.cookies)

    resp = redirect('/')
    resp.set_cookie('search_term', 'NOVAL', expires=0)
    resp.set_cookie('datasetid', 'NOVAL', expires=0)

    if search_term or datasetid:

        for arg in request.args:
            if arg.lower() in ['search_term', 'datasetid']:
                resp.set_cookie('{}'.format(arg), request.args[arg])

        return resp
    else:

        if 'search_term' in request.cookies:
            search_term = request.cookies['search_term']

        if 'datasetid' in request.cookies:
            datasetid = request.cookies['datasetid']

    return render_template('page/index.html',
                           search_term=search_term, datasetid=datasetid)

'''


@page.route('/error/500')
def error():
    redirect_url = url_for('page.index')
    return render_template('errors/error.html',
                           error_code=500,
                           redirect_url=redirect_url), 500


@page.route('/_info', methods=['GET'])
def info():
    return '{}'.format(socket.gethostname())


@page.route('/rdata')
def rdata():
    # attempt to get the RData file and send it
    real_file_name = os.getenv('HOST_FILE_RDATA', '')
    real_file_name = ntpath.basename(real_file_name)

    root_url = url_for('page.index')

    if root_url[-1] == '/':
        redirect_url = '{}data/{}'.format(root_url, real_file_name)
    else:
        redirect_url = '{}/data/{}'.format(root_url, real_file_name)

    return redirect(redirect_url)








