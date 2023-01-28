from flask import Flask, render_template, request
import requests, jsonify

app = Flask(__name__)
url = 'https://www.googleapis.com/books/v1/volumes?q='

# グローバル変数
books = []


@app.route("/")
def hello_world():
    return "<h1>Hello Flask!</h1>"


@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template("post.html")
    elif request.method == "POST":
        return render_template("post.html", username=request.form['username'], content=request.form['content'])


# 本検索ページ
@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template('/search.html')

    if request.method == "POST":
        q = request.form['q']
        if q == "":
            print("hoge")
            return render_template('/search.html')
        else:
            # json
            books = get_book_info(q)
            return render_template('/search.html', books=books)


# 本の個別ページ
@app.route('/book/detail/<int:book_id>', methods=["GET"])
def book_detail(book_id):
    # book_id -= 1
    book = books[(book_id - 1)]
    return render_template('bookDetail.html', book=book)


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
        image_url = ""
        if "authors" in book_data["items"][i]["volumeInfo"]:
            author = book_data["items"][i]["volumeInfo"]["authors"][0]
        elif "publisher" in book_data["items"][i]["volumeInfo"]:
            publisher = book_data["items"][i]["volumeInfo"]["publisher"]

        if "imageLinks" in book_data["items"][i]["volumeInfo"]:
            image_url = book_data["items"][i]["volumeInfo"]["imageLinks"]["smallThumbnail"]

        books.append({
            "id": i + 1,
            "title": book_data["items"][i]["volumeInfo"]["title"],
            "publisher": publisher,
            "author": author,
            "image_url": image_url,
        })

    return books


if __name__ == '__main__':
    app.run(debug=True)
