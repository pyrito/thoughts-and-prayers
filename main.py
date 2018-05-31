from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from counter.counter_main import run_main
import thread
from time import sleep
from threading import Thread, Event
from flask_sqlalchemy import SQLAlchemy
import eventlet
from counter.accessAPI import get_db_string
eventlet.monkey_patch()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_string()
db = SQLAlchemy(app)
#Turn the flask into a socket app
socketio = SocketIO(app, async_mode='eventlet')
thread_update = Thread()
thread_stop_event = Event()

#Created a new Thread class that is specific to the Update Thread for the counter
class UpdateThread(Thread):
    def __init__(self):
        self.delay = 1
        super(UpdateThread, self).__init__()

    def updater(self):

		#As long as we don't get a signal to stop, we keep updating the thread
        while not thread_stop_event.isSet():
            #We select the corresponding data, for now, the database only has Noblesville, this can change
            event = db.session.execute("""SELECT count FROM events WHERE place = :location """, {'location':'Noblesville'}).fetchone()
            if len(event) == 0:
                db.session.execute("INSERT INTO events VALUES(:id, :location, :count, :when)", {'id': 0, 'location': "Noblesville", 'count': 0, 'when': datetime.datetime(2018, 5, 25)})
                db.commit()
                event = db.session.execute("""SELECT count FROM events WHERE place = :location """, {'location':'Noblesville'}).fetchone()
            num = event[0]
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
#We have the update thread and the event that says to stop
    print("helllllloo world creating thread")
    #thread.start_new_thread(run_main, ())
    socketio.run(app)
