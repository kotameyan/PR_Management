# 各種インポート
from flask import Flask, render_template, request, redirect
import sqlite3
from flask_bcrypt import Bcrypt
from datetime import datetime

# 最初の呪文
app = Flask(__name__)
bcrypt = Bcrypt(app)
DATABASE = 'PR_Management/database.db'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # usersテーブルの中から一覧を取得
        db = sqlite3.connect(DATABASE)  # データベースと接続
        # 検索条件:usersテーブル全項目
        sql_statement = 'SELECT id,email,username,role,signup_date,login_date FROM users'
        cur = db.execute(sql_statement)  # 検索を実行
        userdata = cur.fetchall()  # 該当部分を全て取得
        db.close()  # データベースとの接続を閉じる

        return render_template('home.html', userdata=userdata)


@app.route('/students/<int:key>', methods=['GET', 'POST'])
def students(key):
    if request.method == 'GET':
        # 特定のユーザーの成績表を取得
        db = sqlite3.connect(DATABASE)  # データベースと接続
        sql_statement = 'SELECT id,word_id,response,correct,response_date FROM students WHERE user_id={}'.format(
            key)  # 検索条件:特定のユーザーのstudentsテーブル全項目
        cur = db.execute(sql_statement)  # 検索を実行
        studentsdata = cur.fetchall()  # 該当部分を全て取得
        db.close()  # データベースとの接続を閉じる

        # usernameを取得
        db = sqlite3.connect(DATABASE)  # データベースと接続
        sql_statement = 'SELECT username FROM users WHERE id={}'.format(
            key)  # 検索条件:特定のユーザーのusersテーブル内のusername
        cur = db.execute(sql_statement)  # 検索を実行
        username = cur.fetchone()  # 該当部分を一つ取得
        db.close()  # データベースとの接続を閉じる

        # usernameの体裁を整える
        username = str(username)
        username = username.replace('(\'', '')
        username = username.replace('\',)', '')

        return render_template('students.html', studentsdata=studentsdata, username=username)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')

    else:
        # usersテーブルに追加するユーザーの情報(email)
        email = request.form.get('email')
        email = str(email)

        # usersテーブルに追加するユーザーの情報(username)
        username = request.form.get('username')

        # usersテーブルに追加するユーザーの情報(password)
        password = request.form.get('password')
        password = bcrypt.generate_password_hash(password).decode(
            'utf-8')  # python3環境は.decode('utf-8')が必要

        # usersテーブルに追加するユーザーの情報(role)
        role = request.form.get('role')

        # usersテーブルに追加するユーザーの情報(signup_date)
        signup_date = datetime.now()  # 勝手に日本時間になってたのでpytz.timezone('Asia/Tokyo')はなし

        # usersテーブルに追加するユーザーの情報(login_date)
        login_date = datetime.now()  # 勝手に日本時間になってたのでpytz.timezone('Asia/Tokyo')はなし

        # usersテーブルに追加
        db = sqlite3.connect(DATABASE)  # データベースと接続
        sql_statement = 'INSERT INTO users (email,username,password,role,signup_date,login_date) VALUES (\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\')'.format(
            email, username, password, role, signup_date, login_date)  # 追加するユーザーの各項目を設定
        db.execute(sql_statement)  # 追加を実行
        db.commit()  # 実行結果を確定
        db.close()  # データベースとの接続を閉じる

        return redirect('/')


@app.route('/delete_user/<int:key>')
def delete_user(key):
    db = sqlite3.connect(DATABASE)  # データベースと接続
    sql_statement = 'DELETE FROM users WHERE id={}'.format(key)  # 削除するユーザーを指定
    db.execute(sql_statement)  # 削除を実行
    db.commit()  # 実行結果を確定
    db.close()  # データベースとの接続を閉じる

    return redirect('/')


# 最後の呪文
if __name__ == '__main__':
    app.run(debug=True, port=5000)
