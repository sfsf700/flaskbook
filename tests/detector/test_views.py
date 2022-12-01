from pathlib import Path

from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage
from apps.detector.models import UserImage

# 画像一覧画面のテスト
# 未ログイン時
def test_index(client):

    rv = client.get("/")
    # ログインと画像新規登録ボタンがあるかテスト
    assert "ログイン" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()

# ログイン時
def signup(client, username, email, password):
    """サインアップする"""
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)

def test_index_signup(client):
    """サインアップを実行"""
    rv = signup(client, "admin", "flaskbook@example.com", "password")
    # サインアップしたらユーザー名に admin があるかテスト
    assert "admin" in rv.data.decode()

    rv = client.get("/")
    # ログアウトと画像新規登録ボタンがあるかテスト
    assert "ログアウト" in rv.data.decode()
    assert "画像新規登録" in rv.data.decode()

# 画像アップロード画面のテスト
# 未ログイン時
def test_upload_no_auth(client):
    rv = client.get("/upload", follow_redirects=True)

    assert "アップロード" not in rv.data.decode()

    assert "メールアドレス" in rv.data.decode()
    assert "パスワード" in rv.data.decode()

# ログイン時
def test_upload_signup_get(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = client.get("/upload")

    assert "アップロード" in rv.data.decode()

# バリデートエラー
def upload_image(client, image_path):
    """画像アップロード"""
    image = Path(get_root_path("tests"), image_path)

    test_file = (
        FileStorage(
            stream=open(image, "rb"),
            filename=Path(image_path).name,
            content_type="multipart_form-data",
        ),
    )

    data = dict(
        image=test_file,
    )
    return client.post("/upload", data=data, follow_redirects=True)

def test_upload_signup_post_validate(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    # ”サポートされていない画像形式です。" apps/detector/forms.py で指定したエラーメッセージ
    assert "サポートされていない画像形式です。" in rv.data.decode()

# 画像アップロード成功時
def test_upload_signup_post(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    rv = upload_image(client, "detector/testdata/dog.jpg")

    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()