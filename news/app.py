#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, json
from flask import Flask, render_template, request

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    filedir = '/home/shiyanlou/files/'
    filelist = os.listdir(filedir)
    filedict = {}
    for file_json in filelist:
        file_path = filedir + file_json
        with open(file_path, 'r') as file:
            fdict = json.load(file)
            filedict[file_json] = fdict['title']
    print(filedict)

    return render_template('index.html', filedict=filedict)

@app.route('/files/<filename>')
def file(filename):
    file_path = '/home/shiyanlou/files/' + filename + '.json'
    print(file_path)
    if not os.path.exists(file_path):
        return render_template('404.html'), 404
    else:
        with open(file_path, 'r') as file:
            fdict = json.load(file)
        return render_template('file.html', fdict=fdict)
