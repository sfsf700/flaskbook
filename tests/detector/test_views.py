# 未ログイン時は 
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