from flask import Flask, request, Response
from .app_exe import start_ansible
#flask app
app = Flask(__name__)

@app.route('/42test', methods=['POST'])
def home():
    return Response('it works!')

@app.route('/42reboot', methods=['POST'])
def reboot():
    msg = start_ansible(request, 'reboot')
    return Response(msg)

@app.route('/42default', methods=['POST'])
def default_mode():
    msg = start_ansible(request, 'default')
    return Response(msg)

@app.route('/42exam', methods=['POST'])
def exam_mode():
    msg = start_ansible(request, 'exam')
    return Response(msg)

if __name__ == '__main__':
    app.run()
