#ldap search
import subprocess
import pandas as pd
from .ftapi import *
from time import sleep
import json
from pprint import pprint

u,s = auth()
terry = Api(u,s)


def exe_set_pswd_with_login(login:str):
    global terry

    full_password = "A!!000000" + login
    datas = {"user":{"password":full_password}}
    res = ''

    while True:
        try:
            a = terry.path(f'users/{login}').patch(data=datas)

            if 'Response [204]' in str(a):
                res = '패스워드 업데이트 완료!'
                break;
            else:
                if 'message' in a.keys() and a['message'] == 'The access token expired':
                    u,s = auth()
                    terry = Api(u,s)
                else:
                    res = '에러 발생!'
                    break;
        except:
            res = '에러 발생!'
            break;

    return res


def exe_srch_email_get_login(email:str):
    res = ''
    try:
        df = pd.read_csv('/home/bocal/3_1.csv')
        df_list = list(df['email'])
        tmp = [val for val in df_list if email in val]

        if len(tmp) != 1:
            res = '중복되는 이메일이 있거나 존재하지 않는 이메일 주소입니다. 더 자세하게 이메일 주소를 입력하세요!'
        else:
            eng_name = tmp[0].split(',')[1]
            ldap_res = subprocess.check_output(f"ldapsearch -x -LLL cn='{eng_name}' | grep uid:", shell=True, encoding='utf-8')
            res = ldap_res.split(' ')[1][:-1]
    except:
        res = '에러 발생!'

    return res

def start_ldapsearch(request, command:str):
    global ac_thread
    global ack_thread

    res = ''
    data = str(request.form['text'])

    if command == 'email':
        res = exe_srch_email_get_login(data)
    elif command == 'setpswd':
        res = exe_set_pswd_with_login(data)

    #res = wait_msg
    return res




