#!/usr/bin/env python
#coding=utf-8
from utils.DataManager import DataManager
from flask import Flask
from flask import render_template


app = Flask(__name__)

@app.route('/')
def home_page():
    """直接返回
    """
    return render_template('table.html', posts=DataManager.get_all_post_list())

# ----------------------Perment Task <Simple Web Server> ------------------------
def run():
    app.run()

def stop():
    app.stop()
