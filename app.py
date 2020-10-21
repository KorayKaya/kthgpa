from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', gpa="0")





if __name__ == '__main__': app.run(debug=True)