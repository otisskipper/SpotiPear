from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dropdown")
def dropdown():
    
    labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
    
    return render_template('dropdown.html', labels = labels)
    

if __name__ == "__main__":
    app.run(debug=True)

