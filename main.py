from flask import Flask, render_template
from counter.main import run_main
import thread
import sqlite3 as sql

app = Flask(__name__)

@app.route('/')
def main():
	thread.start_new_thread(run_main, ())
	con = sql.connect("shootings.db")
	cur = con.cursor()
	cur.execute('SELECT tps FROM events WHERE shooting_name="Noblesville"')
	num = cur.fetchone()[0]

	return render_template('index.html', number = num)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)