from flask import Flask,render_template,request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/users', methods = ['GET','POST'])
def users():
    if request.method == 'GET':
        # usersテーブルの中から一覧を取得
        db = sqlite3.connect('PR_Management/database.db')
        cur = db.execute("SELECT id,email,username,role,signup_date,login_date FROM users")
        userdata = cur.fetchall()
        db.close()

        return render_template('home.html', userdata = userdata)



if __name__ == "__main__":
    app.run(debug=True)
