import json
from datetime import datetime as dt
from cryptography.fernet import Fernet
import sqlite3
import sys
import os

prj_key = "122.74.49.80.56.45.51.116.66.88.55.103.48.68.79.121.80.109.75.120.82.99.83.85.82.109.104.118.56.86.45.121.48.65.116.119.76.79.90.55.88.122.85.61."

def encrypt(par_val):
    org_key = ''
    for num in prj_key.strip('.').split('.'):
        org_key += chr(int(num))
    mstr_key = org_key.encode()
    f = Fernet(mstr_key)
    pwd = f.encrypt(par_val.encode())
    pwd = pwd.decode()
    return pwd

def decrypt(enc_key):
    org_key = ''
    for num in prj_key.strip('.').split('.'):
        org_key += chr(int(num))
    mstr_key = org_key.encode()
    f = Fernet(mstr_key)
    pwd = f.decrypt(enc_key.encode())
    db_conn = pwd.decode()
    return db_conn

def create_connection(db_file):
    db_path = os.path.join(os.path.dirname(__file__), 'Data_files', db_file)
    # 'subscription.db'
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print("Connection to DB Successfull")
    except Exception as e:
        print(e)
    return conn

def create_user(conn, fname, lname, email, pswrd):
    try:
        user_valid = ''' Select u_email from user_cred 
                Where u_email = '{}' '''.format(email)
        cur_val = conn.cursor()
        cur_val.execute(user_valid)
        rec_val = cur_val.fetchall()
        if len(rec_val):
            return False

        sql = ''' INSERT INTO user_cred(u_fst_nm, u_lst_nm, u_email, u_pass_e, created_dt)
                VALUES('{0}', '{1}', '{2}', '{3}', '{4}') '''.format(fname, lname, email, pswrd, str(dt.utcnow()))
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        print("User created successfully")
        return True
    except Exception as e:
        print(e)

def fetch_user(conn, email, pswrd):
    try:
        sql = '''select u_id as 'User Unique ID', 
                    upper(substr(u_lst_nm, 1, 1))|| substr(u_lst_nm, 2) || ", " ||	upper(substr(u_fst_nm, 1, 1))|| substr(u_fst_nm, 2) as 'User Name',
                    u_email as 'User Email',
                    u_pass_e
                from user_cred
                WHERE u_email = '{0}' '''.format(email)
        cur = conn.cursor()
        cur.execute(sql)
        rec = cur.fetchone()
        columns = [description[0] for description in cur.description][:-1] 
        if rec is None or len(rec) < 1 or decrypt(rec[-1]) != pswrd:
            return False
        else:
            user = {}
            for key, val in zip(columns, rec):
                user[key] = val
            return [user]
    except Exception as e:
        print(e)

def close_connection(conn):
    try:
        conn.close()
        print("Connection Successfully Closed")
    except Exception as e:
        print(e)
