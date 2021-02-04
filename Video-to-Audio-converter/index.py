import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), 'static'))
import common_udf as cf

from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home_pg():
    if request.method == 'POST':
        input_path = request.form.getlist('fl_dr_path')[0].strip()
        quality = request.form.getlist('quality')[0].strip()
        output_path = cf.get_opt_path(input_path)
        if os.path.isfile(input_path):
            pass
        else:
            file_status_ls = cf.dir_walk(input_path, output_path, quality)

        df = cf.create_df(file_status_ls)
        return render_template('log.html') 
    else:
        return render_template('home.html')

@app.route('/log', methods=['POST', 'GET'])
def log_file():
    if request.method == 'POST':
        input_path = request.form.getlist('fl_dr_path')[0].strip()
        quality = request.form.getlist('quality')[0].strip()
        output_path = cf.get_opt_path(input_path)
        print('8'*80)
        # print(output_path)
        if os.path.isfile(input_path):
            file_status_ls = cf.file_convert(input_path, output_path, quality)
        elif os.path.isdir(input_path):
            file_status_ls = cf.dir_walk(input_path, output_path, quality)
        else:
            return render_template('error.html')

        df = cf.create_df(file_status_ls)
        results = df.to_dict('records')
        return render_template('log.html', results = results)

if __name__ == "__main__":
    app.run(debug=True, port=8088
    )