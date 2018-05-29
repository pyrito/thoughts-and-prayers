from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from counter.main import run_main
import thread
from time import sleep
from threading import Thread, Event
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True


#turn the flask into a socket app
socketio = SocketIO(app)

thread_update = Thread()
thread_stop_event = Event()
thread.start_new_thread(run_main, ())

class UpdateThread(Thread):
	def __init__(self):
		self.delay = 1
		super(UpdateThread, self).__init__()

	def updater(self):
		print("working")
		con = sql.connect("shootings.db")
		cur = con.cursor()
		while not thread_stop_event.isSet():
			cur.execute('SELECT tps FROM events WHERE shooting_name="Noblesville"')
			num = cur.fetchone()[0]
			socketio.emit('newnumber', {'number' : num}, namespace='/test')
			sleep(self.delay)

	def run(self):
		self.updater()

@app.route('/')
def main():
	return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
	global thread_update
	print('connected')

	if not thread_update.isAlive():
		thread_update = UpdateThread()
		thread_update.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)