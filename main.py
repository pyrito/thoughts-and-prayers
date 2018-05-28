from flask import Flask, render_template
from counter.main import run_main
import thread

app = Flask(__name__)

@app.route('/')
def main():
	thread.start_new_thread(run_main, ())
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)