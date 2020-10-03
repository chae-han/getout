from flask import Flask, request, Response
import slackweb
import os
import json
import requests
import threading
import time
import re
from . import ansible_cluster as ac
from .info import *

#thread for ansible cluster command allow only one thread for safety
ac_thread = None
ack_thread = None

#regex
p = []
p.append(re.compile("c([1-9]|[1][0])"))
p.append(re.compile("c([1-9]|[1][0])r([1-9][0-9]?)"))
p.append(re.compile("c([1-9]|[1][0])r([1-9][0-9]?)s([1-9][0-9]?)"))

#thread lock
_lock = threading.Lock()

#=================================================================

def slack_send(url, message):
    slack = slackweb.Slack(url=url)
    #slack.notify(response_type="in_channel", text=message)
    slack.notify(text=message)

def is_host_error(hostname_list:list):
    res = False
    right_host = 0
    for name in hostname_list:
        for exp in p:
            obj = exp.fullmatch(name)
            if obj:
                right_host += 1
    
    if right_host < len(hostname_list):
        res = True

    return res

def start_ansible(request, ansible_command:str):
    global ac_thread
    global ack_thread

    res = ""
    command = ""

    data = str(request.form['text'])
    hostname_list = data.split(',')

    if request.form['channel_id'] != slack_channel_id:
        res = error_channel_msg
    elif request.form['user_id'] not in slack_manager:
        res = error_user_msg
    elif is_ac_thread_alive():
        res = already_msg 
    elif data == '' or is_host_error(hostname_list):
        res = error_host_msg
    else:
        command = ac_commands[ansible_command] + ' -l '
        # make command format
        for name in hostname_list:
            command += name
            if name.find('s') > -1:
                command += '.42seoul.kr'
            command += ',' #without any space
        # start ansible
        ac_thread = threading.Thread(target=exe_response, args=(command, request.form['response_url']))
        ack_thread = threading.Timer(20, exe_ack, (request.form['response_url'],))

        ack_thread.start()
        ac_thread.start()

        res = wait_msg
    return res

def exe_ack(response_url:str):
    global ack_thread
    data = "진행중..."
    post_response(response_url, data)
    ack_thread = threading.Timer(60, exe_ack, (response_url,))
    ack_thread.start()

def exe_response(command:str, response_url:str):
    _lock.acquire()
    global ack_thread

    data = exe_ansible(command)
    ack_thread.cancel()

    if data == "":
        data = error_ansible_msg

    res = post_response(response_url, data)
    _lock.release()
    return res

def exe_ansible(command:str):
    c = ac.ansible_cluster(ssh_privatekey_path, command) 
    res = c.start_command()
    return res

def post_response(response_url:str, data:str):
    headers = {'Content-Type' : 'application/json'}
    payload = {'text' : data}
    res = requests.post(response_url, headers=headers, data=json.dumps(payload))
    return res

def is_ac_thread_alive():
    global ac_thread
    res = False
    if ac_thread != None and ac_thread.is_alive():
        res = True
    return res


