from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

db = SQLAlchemy()
csrf = CSRFProtect()


login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定
login_manager.login_view = "auth.signup"

login_manager.login_message = ""

def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    db.init_app(app)
    Migrate(app,db)
    csrf.init_app(app)

    # login_managerをアプリケーションと連携する
    login_manager.init_app(app)

    # crudパッケージからviewsをimportする
    from apps.crud import views as crud_views
    # register_blueprintを使いviewsのcrudをアプリへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app