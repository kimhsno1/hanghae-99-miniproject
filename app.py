import datetime

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.hbsrzff.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

# 이건 없이 어케 돌아가냐 레퍼런스 파일에서는 신기혀네

@app.route('/')
def home():
    return render_template('zero100manga.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/rank')
def manga_update():
    return render_template('rank.html')

@app.route('/manga_individual_page')
def manga_individual_page():
    return render_template('manga_individual_page.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route("/mangas", methods=["POST"])
def manga_update_post():
    image_receive = request.form['image_give']
    vol_receive = request.form['vol_give']
    time = datetime.datetime.now()

    doc = {
        'img' : image_receive,
        'vol' : vol_receive,
        'time' : time
    }
    db.mangas.insert_one(doc)
    return jsonify({'msg': '신간 만화 업데이트 완료'})

@app.route("/mangas", methods=["GET"])
def manga_update_get():
    new_book_list = list(db.mangas.find({}, {'_id': False}))
    now_time = datetime.datetime.now()
    lists = []
    for time in new_book_list:
        diff = now_time - time['time']
        if diff.seconds > 10:
            time.clear()
        if time != {}:
            lists.append(time)

    return jsonify({'mangas' : lists})

@app.route("/mangaMain", methods=["POST"])
def manga_main_post():
    manga_main_image_receive = request.form['manga_main_image_give']
    manga_main_title_receive = request.form['manga_main_title_give']
    manga_main_desc_receive = request.form['manga_main_desc_give']

    manga_main_list = list(db.main_mangas.find({},{'_id':False}))
    count = len(manga_main_list) + 1

    doc = {
        'num' : count,
        'image' : manga_main_image_receive,
        'title' : manga_main_title_receive,
        'desc' : manga_main_desc_receive,
    }

    db.main_mangas.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})

@app.route("/main_manga", methods=["GET"])
def manga_main_get():
    manga_main_get_list = list(db.main_mangas.find({}, {'_id': False}))
    return jsonify({'main_mangas' : manga_main_get_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)