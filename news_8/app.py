#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os, json
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from pymongo import MongoClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/zixun'
db = SQLAlchemy(app)
mclient = MongoClient('127.0.0.1', 27017)
mdb = mclient.zixun

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<category(name=%s)>' % self.name


class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    created_time = db.Column(db.DateTime)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = relationship('Category')
    content = db.Column(db.Text)
    def __init__(self, title, created_time, category, content):
        self.title = title
        self.created_time = created_time
        self.category = category
        self.content = content
    def __repr__(self):
        return '<file(title=%s)>' % self.title

    def add_tag(self, tag_name):
        title = self.title
        if not mdb.zixun.find_one({'title':title}):
            tag_list = []
            tag_list.append(tag_name)
            mdb.zixun.insert_one({'title': title, 'tags': tag_list})
        else:
            tags = mdb.zixun.find_one({'title': title}, {'tags':1, '_id':0})
            tag_list = tags['tags']
            if tag_name not in tag_list:
                tag_list.append(tag_name)
            mdb.zixun.update_one({'title': title}, {'$set': {'tags': tag_list}})

    def remove_tag(self, tag_name):
        title = self.title
        if not mdb.zixun.find_one({'title': title}):
            return None
        else:
            tags = mdb.zixun.find_one({'title': title}, {'tags':1, '_id':0})
            tag_list = tags['tags']
            if tag_name in tag_list:
                tag_list.remove(tag_name)
            else:
                print("no this tag")
            mdb.zixun.update_one({'title': title}, {'$set': {'tags': tag_list}})
    
    @property
    def tags(self):
        title = self.title
        if not mdb.zixun.find_one({'title': title}):
            print('no this title')
            return None
        else:
            tags = mdb.zixun.find_one({'title': title}, {'tags':1, '_id':0})
            tag_list = tags['tags']
            for tag in tag_list:
                print(tag)


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
