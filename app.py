from flask import Flask, render_template, request
import requests, jsonify

app = Flask(__name__)
url = 'https://www.googleapis.com/books/v1/volumes?q='

@app.route("/")
def hello_world():
    return "<h1>Hello Flask!</h1>"

@app.route('/post', methods=["GET", "POST"])
def post():
    if request.method == "GET":
        return render_template("post.html")
    elif request.method == "POST":
        return render_template("post.html", username=request.form['username'], content=request.form['content'])

@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template('search.html')

    if request.method == "POST":
        q = request.form['isbn']
        # json
        bookData = getBook(q)
        # title = bookData["items"][0]["volumeInfo"]["title"]
        # authors = bookData["items"][0]["volumeInfo"]["authors"][0]
        # image = bookData["items"][0]["volumeInfo"]["imageLinks"]["smallThumbnail"]
        totalItems = len(bookData['items'])  # 件数
        # 検索結果の初期化を行う
        items = []
        titles = []
        authors = []
        images = []

        # 本の情報を配列に追加
        for i in range(totalItems):
            items.append(bookData["items"][i])

        # 必要な情報を取得
        for item in items:
            titles.append(item["volumeInfo"]["title"])
            authors.append(item["volumeInfo"]["authors"][0])
            # images.append(item["volumeInfo"]["imageLinks"]["smallThumbnail"])
            print(item["volumeInfo"])

        # サムネ画像が存在しない( = "imageLinks" が" volumeInfo" にない)とき, から文字列を入れる
        for item in items:
            if "imageLinks" not in item["volumeInfo"]:
                images.append("")
            else:
                images.append(item["volumeInfo"]["imageLinks"]["smallThumbnail"])

        return render_template('/search.html', title=titles, author=authors, totalItems=totalItems, image=images)

# 9784167741013
def getBook(isbn):
    req_url = url + isbn
    bookDatas = requests.get(req_url).json()
    return bookDatas

# def bookDataParse(data):



if __name__ == '__main__':
    app.run(debug=True)
