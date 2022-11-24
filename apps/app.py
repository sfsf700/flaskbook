from pathlib import Path
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(config_key):
    app = Flask(__name__)
    
    app.config.from_object(config[config_key])

    db.init_app(app)
    Migrate(app,db)
    csrf.init_app(app)

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
