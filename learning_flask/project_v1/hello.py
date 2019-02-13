from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'glitch in the system'

if __name__ == '__main__':
	app.run()