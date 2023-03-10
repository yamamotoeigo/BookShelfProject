from flask import Flask, render_template, request, flash, redirect
import requests, jsonify

app = Flask(__name__)
url = 'https://www.googleapis.com/books/v1/volumes?q='

# グローバル変数
books = []

@app.route("/")
def hello_world():
    return "<h1>ホームです</h1>"


@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template("post.html")
    if request.method == "POST":
        return render_template("post.html", username=request.form['username'], content=request.form['content'])


# 本検索ページ
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template('/search.html')

    if request.method == "POST":
        global books
        books = []
        q = request.form['q']

        if q == "":
            return redirect('/search')
        else:
            # json
            books = get_book_info(q)
            return render_template('/search.html', books=books)


# 本の個別ページ
@app.route('/book/register/<int:book_id>', methods=["GET", "POST"])
def book_detail(book_id):
    if request.method == "GET":
        book = books[(book_id - 1)]
        return render_template('book_detail.html', book=book)

    if request.method == "POST":
        return "登録しました"

# APIを叩いて本に関するデータを得る
def get_book(q):
    req_url = url + q
    book_datas = requests.get(req_url).json()
    return book_datas


# 本の詳細を取得するメソッド
def get_book_info(q):
    book_data = get_book(q)
    total_items = len(book_data['items'])  # 件数

    for i in range(total_items):
        author = ""
        publisher = ""
        thumbnail = ""
        if "authors" in book_data["items"][i]["volumeInfo"]:
            author = book_data["items"][i]["volumeInfo"]["authors"][0]
        elif "publisher" in book_data["items"][i]["volumeInfo"]:
            publisher = book_data["items"][i]["volumeInfo"]["publisher"]

        if "imageLinks" in book_data["items"][i]["volumeInfo"]:
            thumbnail = book_data["items"][i]["volumeInfo"]["imageLinks"]["smallThumbnail"]

        books.append({
            "id": i + 1,
            "title": book_data["items"][i]["volumeInfo"]["title"],
            "publisher": publisher,
            "author": author,
            "thumbnail": thumbnail,
        })

    return books


if __name__ == '__main__':
    app.run(debug=True)
