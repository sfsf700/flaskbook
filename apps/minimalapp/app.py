import logging
import os # 環境変数取得のため

from email_validator import EmailNotValidError, validate_email
from flask import (
    Flask,
    current_app,
    flash,
    g,
    redirect, 
    render_template,
    request,
    url_for,
)

from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message


app = Flask(__name__)

# SECRET_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"
# ログレベルを設定 
app.logger.setLevel(logging.DEBUG)
# リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# DebugToolbarExtensionにアプリケーションをセット

# Mailクラスのコンフィグ
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

toolbar = DebugToolbarExtension(app)

# flask-mail拡張を登録
mail = Mail(app)

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
    return render_template("index.html", name=name)

with app.test_request_context():
    # /
    print(url_for("index"))
    # /hello/world
    print(url_for("hello-endpoint", name="world"))
    # /name/ichiro?page = 1
    print(url_for("show_name", name="ichiro", page="1"))

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

##問い合わせフォーム ルーティング
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form属性を使ってフォームの値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 入力チェック 空の場合は下記のFlashメッセージを表示
        is_valid = True
        if not username:
            flash("ユーザ名は必須です")
            is_valid = False

        if not email:
            flash("メールアドレスは必須です")
            is_valid = False
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("メールアドレスの形式で入力して下さい")
            is_valid = False

        if not description:
            flash("問い合わせ内容は必須です")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        # 問い合わせ完了エンドポイントへリダイレクト

        ##メールを送る
        send_email(
            email,
            "問い合わせ有難うございました。",
            "contact_mail",
            username=username,
            description=description,
        )

        flash("問い合わせ内容はメールにて送信しました。")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")


def send_email(to, subject, template, **kwargs):
    """メールを送信する関数"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
    