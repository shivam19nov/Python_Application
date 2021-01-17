import sys
import os
from flask import Flask, render_template, request, redirect
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'assets'))
import common_udf as cf

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def login_pg():
    if request.method == 'POST':
        email = request.form.getlist('email')[0].strip()
        pswrd = request.form.getlist('password')[0].strip()
        print(email, pswrd)
        conn = cf.create_connection('subscription.db')
        user_detail = cf.fetch_user(conn, email, pswrd)
        cf.close_connection(conn)
        print(user_detail)
        if user_detail:
            return render_template('user.html', user_detail = user_detail)
        else:
            result = {
                'header': 'User Creation Failed',
                'icon': 'fail',
                'message': 'Unable to Login User ' + email.lower(),
                'option' : 'Please Check Your Credentials.'
            }
            print('User Login Failed')
            return render_template('login_pg.html', result = result)
    else:
        return render_template('login_pg.html')

@app.route('/register', methods=['POST', 'GET'])
def register_pg():
    if request.method == 'POST':
        fname = request.form.getlist('fname')[0].lower().strip()
        lname = request.form.getlist('lname')[0].lower().strip()
        email = request.form.getlist('email')[0].lower().strip()
        pswrd = cf.encrypt(request.form.getlist('password')[0])
        conn = cf.create_connection('subscription.db')
        status = cf.create_user(conn, fname, lname, email, pswrd)
        cf.close_connection(conn)
        if status:
            return redirect('/')
        else:
            result = {
                'header': 'User Creation Failed',
                'icon': 'fail',
                'message': 'Registration Failed for ' + lname.title() + ', ' + fname.title(),
                'option' : 'Please Try again with different email.'
            }
            print('User Creation Failed')
            return render_template('register_pg.html', result = result)
    else:
        return render_template('register_pg.html', result = {})


if __name__ == "__main__":
    app.run(debug=True)
