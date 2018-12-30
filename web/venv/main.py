#!congding = utf-8

from flask import Flask, render_template, request

from search import search_results

import xml.etree.ElementTree as ET
import sqlite3
import configparser
import time

import jieba

app = Flask(__name__)

doc_dir_path = ''
db_path = ''
global page #page代表页数
global keys #关键字


def searchidlist(key, selected=0):
    temp_page = []
    results = search_results(key)
    for i in range(1, (len(results) // 10 + 2)):
        temp_page.append(i)
    flag = 1
    return flag, temp_page


def cut_page(page, no): #no代表页数第no页的内容
    results = search_results(keys)
    docs = results[(no-1)*10:no*10] #每一页有10个
    return docs

def init():
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')


@app.route('/')
def main():
    init()
    return render_template('search.html', error=True)


# 读取表单数据，获得doc_ID
@app.route('/search/', methods=['POST'])
def search():
    global keys
    global checked
    global page
    checked = ['checked="true"', '', '']
    keys = request.form['key_word']
    print(keys)
    if keys not in ['']:
        print(time.clock())
        flag, page = searchidlist(keys)
        if flag == 0:
            return render_template('search.html', error=False)
        docs = cut_page(page, 1)  # 第一页文档
        print(time.clock())
        return render_template('high_search.html', checked=checked, key=keys, docs=docs, page=page,
                               error=True)
    else:
        return render_template('search.html', error=False)



@app.route('/search/page/<page_no>/', methods=['GET'])
def next_page(page_no):
    try:
        page_no = int(page_no)
        docs = cut_page(page, (page_no))  # 下一页的文档数目
        return render_template('high_search.html', checked=checked, key=keys, docs=docs, page=page,
                               error=True)
    except:
        print('next error')


@app.route('/search/<key>/', methods=['POST'])
def high_search(key):
    try:
        selected = int(request.form['order'])
        for i in range(3):
            if i == selected:
                checked[i] = 'checked="true"'
            else:
                checked[i] = ''
        flag,page = searchidlist(key)
        if flag==0:
            return render_template('search.html', error=False)
        docs = cut_page(page, 1)
        return render_template('high_search.html',checked=checked ,key=keys, docs=docs, page=page,
                               error=True)
    except:
        print('high search error')



if __name__ == '__main__':
    jieba.initialize()  # 手动初始化（可选）
    app.run(debug=True)