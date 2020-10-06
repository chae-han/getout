from sqlalchemy import text
from .info import *

def start_userdb(request, userdb_command:str):
    user_id = str(request.form['text'])
    if userdb_command == 'add':
        add_user(user_id)
    elif userdb_command == 'delete':
        delete_user(user_id)
        

def add_user(user_id:str):
    res = error_db_msg
    try:
        id = app.database.execute(text("""
                INSERT INTO users (
                    user_id
                    ) VALUES (
                        :user_id
                        )
                """), user_id).lastrowid
        res = success_db_msg + " user_id: " + id
    except:
        pass
    return res

def delete_user(user_id:str):
    pass
        
        
