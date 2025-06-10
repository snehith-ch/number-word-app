from flask import Flask, render_template, request
from .converter import convert_number

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        number_input = request.form["number"]
        result = convert_number(number_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
