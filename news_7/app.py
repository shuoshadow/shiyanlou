#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/zixun'
db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self, name):
        name = self.name
    def __repr__(self):
        return '<category(name=%s)>' % self.name


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship('Category', backref='files')
    content = db.Column(db.Text)
    def __init__(self, title, created_time, category, content):
        title = self.title
        crteated_time = self.created_time
        category = self.category
        content = self.content
    def __repr__(self):
        return '<file(title=%s)>' % self.title


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    files = File.query.all()
    filedict = {}
    for file in files:
        id = file.id
        title = file.title
        filedict[id] = title
    return render_template('index.html', filedict=filedict)

@app.route('/files/<file_id>')
def file(file_id):
    fileId = File.query.filter(File.id==file_id).first()
    print(fileId)
    if not fileId:
        return render_template('404.html'), 404
    else:
        filez = File.query.filter(File.id==file_id).first()
        content = filez.content
        created_time = filez.created_time
        category_id = filez.category_id
        category = Category.query.filter(Category.id==category_id).first().name
        fdict = {'content':content, 'create_time':created_time, 'category':category}
    return render_template('file.html', fdict=fdict)
