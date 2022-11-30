# セットアップ処理とクリーンナップ処理
import os
import shutil

import pytest

from apps.app import create_app, db

from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag

@pytest.fixture
def fixture_app():
    # セットアップ処理
    # テスト用のコンフィグを使うために引数にtestingを指定する
    app = create_app("testing")

    # データベースを利用するための宣言をする
    app.app_context().push()

    # テスト用データベースのテーブル作成
    with app.app_context():
        db.create_all()
    
    # テスト用の画像アップロードディレクトリを作成
    os.mkdir(app.config["UPLOAD_FOLDER"])


    # テスト実行
    yield app

    # クリーンナップ処理
    # 各テーブルのレコードを削除
    User.query.delete()

    UserImage.query.delete()

    UserImageTag.query.delete()

    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()

@pytest.fixture
def client(fixture_app):
    
    return fixture_app.test_client()