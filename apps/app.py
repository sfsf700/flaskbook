from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI=
          f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODEIFICATIONS=False
    )

    db.init_app(app)
    Migrate(app,db)

    # crudパッケージからviewsをimportする
    from apps.crud import views as crud_views
    # register_blueprintを使いviewsのcrudをアプリへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app

    # blueprint #
    # アプリを分割できる
    # URLプレフィックスやサブドメインを指定して、他のアプリケーションルートと区別できる
    # Blueprint単位でテンプレートを分けることができる
    # Blueprint単位で静的ファイルを分けることができる
