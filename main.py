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


#Turn the flask into a socket app
socketio = SocketIO(app)

#We have the update thread and the event that says to stop
thread_update = Thread()
thread_stop_event = Event()
thread.start_new_thread(run_main, ())

#Created a new Thread class that is specific to the Update Thread for the counter
class UpdateThread(Thread):
	def __init__(self):
		self.delay = 1
		super(UpdateThread, self).__init__()

	def updater(self):
		print("working")
		#Connect to the SQL database
		con = sql.connect("shootings.db")
		cur = con.cursor()

		#As long as we don't get a signal to stop, we keep updating the thread
		while not thread_stop_event.isSet():
			#We select the corresponding data, for now, the database only has Noblesville, this can change
			cur.execute('SELECT tps FROM events WHERE shooting_name="Noblesville"')
			num = cur.fetchone()[0]
			#We then send this to the listening socket
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

	#If the thread does not exist then we create the new thread and start it. This prevents multiple threads from coming up
	if not thread_update.isAlive():
		thread_update = UpdateThread()
		thread_update.start()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)