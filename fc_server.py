#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  5 17:38:52 2019

@author: maximoskaliakatsos-papakostas
"""

import os
cwd = os.getcwd()
from flask import Flask, render_template, send_file, request, redirect, Response, jsonify
import json
import shutil
import FC_feature_computation_functions as fcf

user_ID = []
parts_in = []
sever_busy = False

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
static_root = APP_ROOT + os.sep + 'static' + os.sep
templates_static_root = APP_ROOT + os.sep + 'templates/static' + os.sep

folder_in = static_root + 'input_files' + os.sep
folder_out = static_root + 'output_files' + os.sep
templates_folder_out = templates_static_root + 'output_files' + os.sep

# file_in_name = 'BC_001_026900B_a1.xml';
# file_in_path = cwd + os.sep + folder_in + file_in_name
# file_out_name = file_in_name.split('.')[0] + '.csv'
# file_out_path = cwd + os.sep + folder_out + file_out_name

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=['POST'])
def upload():
    # use globals
    global parts_in
    global user_ID
    global static_root
    global folder_in
    global folder_out
    global sever_busy
    sever_busy = True
    # make folders of user
    user_input_folder = folder_in + 'input_of' + user_ID
    user_output_folder = folder_out + 'output_of' + user_ID
    if not os.path.isdir(user_input_folder):
        os.mkdir(user_input_folder)
    if not os.path.isdir(user_output_folder):
        os.mkdir(user_output_folder)
    # initialise list of all input and output files
    input_files = []
    output_files = []
    # save files in input
    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([user_input_folder, filename])
        input_files.append( destination )
        output_files.append( user_output_folder + os.sep +  filename.split('.')[0] + '.csv' )
        print(destination)
        file.save(destination)
    # extract features for all files
    for i in range( len( input_files ) ):
        f = fcf.extract_features_of_parts_to_csv(input_files[i], parts_in, output_files[i])
    # make zip file name
    zip_name = 'output_of' + user_ID
    # and full path
    full_path_zip_file = folder_out + zip_name + '.zip'
    templates_full_path_zip_file = templates_folder_out + zip_name + '.zip'
    # first check if file exists and delete it
    if os.path.isfile(full_path_zip_file):
        os.remove(full_path_zip_file)
    # zip folder
    shutil.make_archive(zip_name, 'zip', user_output_folder)
    # move folder to static
    shutil.copy(APP_ROOT + os.sep + zip_name + '.zip', templates_folder_out)
    shutil.move(APP_ROOT + os.sep + zip_name + '.zip', folder_out)
    # send back zipped folder
    sever_busy = False;
    return send_file(filename_or_fp=templates_full_path_zip_file, attachment_filename='output_of' + user_ID + '.zip', as_attachment=True)

@app.route("/set_parameters", methods=['POST'])
def set_parameters():
    print('inside set_parameters')
    data = request.get_data()
    dat_json = json.loads(data.decode('utf-8'))
    # use globals
    global parts_in
    global user_ID
    global sever_busy
    parts_in = dat_json['parts']
    user_ID = dat_json['clientID']
    print('len(parts_in): ', len(parts_in))
    if len( parts_in ) == 0:
        parts_in = []
    else:
        # make an int array
        parts_in = [int(s) for s in parts_in.split(',')]
    print('parts_in: ', parts_in)
    print('user_ID: ', user_ID)
    # prepare response
    tmp_json = {}
    tmp_json['sever_busy'] = sever_busy
    return jsonify(tmp_json)

if __name__ == '__main__':
    print('--- --- --- main')
    app.run(host='0.0.0.0', port=8111, debug=True)