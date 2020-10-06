#from sqlalchemy import text
import pymysql
from .info import *
from .config import *

class db_work:
    def __init__(self):
        self.conn = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, charset=db_charset)
        self.cur = self.conn.cursor()

    def do_sql(self, sql:str):
        self.cur.execute(sql)

    def __exit__(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()
    

def start_userdb(request, userdb_command:str):
    user_id = str(request.form['text'])
    if user_id == '':
        res = db_info_error_msg
    else:
        db = db_work()
        if userdb_command == 'add':
            res = db.do_sql("INSERT INTO users VALUES({user_id});")
        elif userdb_command == 'delete':
            pass
    return res

        
        
