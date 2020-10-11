from flask import Flask, request, Response
#from sqlalchemy import create_engine, text
from .app_exe import start_ansible
from .userdb import start_userdb
from .ldap import start_ldapsearch

#flask app
app = Flask(__name__)
#app.config.from_pyfile('config.py')
#db = create_engine(app.config['DB_URL'], encoding = 'utf-8')
#app.database = db 

@app.route('/42test', methods=['POST'])
def home():
    return Response('it works!')

@app.route('/42reboot', methods=['POST'])
def reboot():
    msg = start_ansible(request, 'reboot')
    return Response('/42reboot  ' + msg)

@app.route('/42default', methods=['POST'])
def default_mode():
    msg = start_ansible(request, 'default')
    return Response('/42default  ' + msg)

@app.route('/42exam', methods=['POST'])
def exam_mode():
    msg = start_ansible(request, 'exam')
    return Response('/42exam  ' + msg)

@app.route('/42srchid', methods=['POST'])
def get_id_srch_email():
    msg = start_ldapsearch(request, 'email')
    return Response('login id : ' + msg)

@app.route('/42setpswd', methods=['POST'])
def set_pswd_with_id():
    msg = start_ldapsearch(request, 'setpswd')
    return Response('/42setpswd ' + msg)


@app.route('/42adduser', methods=['POST'])
def add_manager():
    msg = start_userdb(request, 'add')
    return Response(msg)

@app.route('/42deluser', methods=['POST'])
def delete_manager():
    msg = start_userdb(request, 'delete')
    return Response(msg)

if __name__ == '__main__':
    app.run()
