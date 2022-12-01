from pathlib import Path

from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage
from apps.detector.models import UserImage

## 画像一覧画面のテスト
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

## 画像アップロード画面のテスト
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


## 物体検知とタグによる検索機能テスト
# バリデートエラー時
def test_detect_no_user_image(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/dog.jpg")
    # 存在しないIDを指定
    rv = client.post("/detect/notexistid", follow_redirects=True)
    # apps/detector/views.py  def detect(image_id):
    assert "物体検知対象の画像が存在しません。" in rv.data.decode()

# 物体検知成功時
def test_detect(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/dog.jpg")
    user_image = UserImage.query.first()

    # 物体検知を実行
    rv = client.post(f"/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()

    assert user_image.image_path in rv.data.decode()
    assert "dog" in rv.data.decode()

# タグ検索時
def test_detect_search(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/dog.jpg")
    user_image = UserImage.query.first()

    client.post(f"/detect/{user_image.id}", follow_redirects=True)
    # dog で検索する
    rv = client.get("/images/search?search=dog")
    # dogタグの画像があることを確認
    assert user_image.image_path in rv.data.decode()
    # dog があることを確認
    assert "dog" in rv.data.decode()

    rv = client.get("/images/search?search=test")
    # dogタグの画像がないことを確認
    assert user_image.image_path not in rv.data.decode()
    # dogがないことを確認
    assert "dog" not in rv.data.decode()


## 画像削除機能
def test_delete(client):
    signup(client, "admin", "flaskbook@example.com", "password")
    upload_image(client, "detector/testdata/dog.jpg")

    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f"/images/delete/{user_image.id}", follow_redirects=True)

    assert image_path not in rv.data.decode()

## カスタムエラー画面
def test_custom_error(client):
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()