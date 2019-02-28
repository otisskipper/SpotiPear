from flask import Flask, render_template, request, redirect, url_for
from functions import custom_add
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/adding")
def adding():
	n1 = request.args.get('n1')
	n2 = request.args.get('n2')
	return custom_add(n1, n2)

@app.route('/getname')
def getname():
	user = request.args.get('nm')
	return redirect(url_for('success', name = user))
		


@app.route('/success/<name>')
def success(name):
		return 'welcome %s' % name


if __name__ == "__main__":
    app.run(debug=True)
