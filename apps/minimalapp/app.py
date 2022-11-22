from flask import Flask, render_template, url_for, current_app, g, request

app = Flask(__name__)

@app.route("/")
def index():
  return "Hello, Flaskbook!"

# ルーティング #

@app.route("/hello/<name>",     # Rule
  methods = ["GET"],            # Methods
  endpoint = "hello-endpoint")  # Endpoint
def hello(name):
  return f"Hello, {name}!"

#show_nameエンドポイントを作成
@app.route("/name/<name>")
def show_name(name):
  #変数をテンプレートに渡す
  return render_template("index.html", name = name)

with app.test_request_context():
  # /
  print(url_for("index"))
  # /hello/world
  print(url_for("hello-endpoint", name = "world"))
  # /name/ichiro?page = 1
  print(url_for("show_name", name = "ichiro", page = "1"))

# アプリケーションコンテキストを取得してスタックへpushする
ctx = app.app_context()
ctx.push()

# current_appにアクセス可能になる
print(current_app.name)

# グローバルなテンポラリ領域に値を設定する
g.connection = "connection"
print(g.connection)

with app.test_request_context("/users?updated = true"):
  # trueが出力される
  print(request.args.get("updated"))