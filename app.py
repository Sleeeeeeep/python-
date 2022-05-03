from flask import Flask,render_template
import sqlite3

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    #return render_template('index.html')
    return index()

@app.route('/movie')
def movie():

    datalist = []
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    sql ="select * from movie250"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.cursor()
    return render_template('movie.html',movies = datalist)

@app.route('/score')
def score():
    score=[]
    count=[]
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        count.append(item[1])
    con.cursor()
    cur.close()
    con.cursor()
    return render_template('score.html',score=score,count=count)

@app.route('/word')
def word():
    return render_template('word.html')

@app.route('/team')
def team():
    return render_template('team.html')


if __name__ == '__main__':
    app.run()
