# app.py

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


# データベースに接続し、テーブルを作成する関数
def create_table():
    conn = sqlite3.connect('instance/edu_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS study_time (
            subject TEXT PRIMARY KEY,
            time INTEGER
        )
    ''')
    conn.commit()
    conn.close()


# データベースから科目と勉強時間のデータを取得する関数
def get_study_data():
    conn = sqlite3.connect('instance/edu_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM study_time')
    study_data = c.fetchall()
    conn.close()
    return study_data


# インデックスページのルート
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        time = int(request.form['time'])

        conn = sqlite3.connect('instance/edu_data.db')
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO study_time VALUES (?, ?)', (subject, time))
        conn.commit()
        conn.close()

    study_data = get_study_data()
    return render_template('index.html', study_data=study_data)


# 結果ページのルート
@app.route('/results')
def results():
    study_data = get_study_data()
    return render_template('results.html', study_data=study_data)


if __name__ == '__main__':
    app.run(port=5009)  # 別のポート番号を指定



