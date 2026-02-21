import random
import turtle
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

random = ranint (300 -300)

x = ranint (300)
y = ranint (-300)

turtle goto
