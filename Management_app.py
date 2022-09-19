from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DATABASE = 'PR_Management/database.db'


@app.route('/')
def index():
    return redirect('/users')


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # usersテーブルの中から一覧を取得
        db = sqlite3.connect(DATABASE)  # データベースと接続
        sql_statement = "SELECT id,email,username,role,signup_date,login_date FROM users"  # 検索条件を設定
        cur = db.execute(sql_statement)  # 検索条件に基づいて検索
        userdata = cur.fetchall()  # 該当部分を全て取得
        db.close()  # データベースとの接続を閉じる

        return render_template('home.html', userdata=userdata)


@app.route('/students/<int:key>', methods=['GET', 'POST'])
def students(key):
    if request.method == 'GET':
        # 特定のユーザーの成績表を取得
        db = sqlite3.connect(DATABASE)  # データベースと接続
        sql_statement = "SELECT id,word_id,response,correct,response_date FROM students WHERE user_id={}".format(
            key)  # 検索条件を設定
        cur = db.execute(sql_statement)  # 検索条件に基づいて検索
        studentsdata = cur.fetchall()  # 該当部分を全て取得
        db.close()  # データベースとの接続を閉じる

        # usernameを取得
        db = sqlite3.connect(DATABASE)  # データベースと接続
        sql_statement = "SELECT username FROM users WHERE id={}".format(
            key)  # 検索条件を設定
        cur = db.execute(sql_statement)  # 検索条件に基づいて検索
        username = cur.fetchone()  # 該当部分を一つ取得
        db.close()  # データベースとの接続を閉じる

        # usernameの体裁を整える
        username = str(username)
        username = username.replace('(\'', '')
        username = username.replace('\',)', '')

        return render_template('students.html', studentsdata=studentsdata, username=username)


if __name__ == "__main__":
    app.run(debug=True)
