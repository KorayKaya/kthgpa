from flask import Flask, render_template, request, redirect
from tika import parser
import re

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return redirect(url_for('index'), gpa="0")
        return render_template('index.html', gpa=str(calcGPA(uploaded_file)))
    else:
        return render_template('index.html', gpa="0")

def calcGPA(file):
    gradeDictionary = {
        "A":5,
        "B":4.5,
        "C":4,
        "D":3.5,
        "E":3,
        "F":0,
        "P":0
    }

    rawText = parser.from_file(file)

    rawList = rawText['content'].splitlines()
    finalList  = []

    gradeRe = "\\b[A-Z]\\b"
    hpRe = "\\d+,\\d"

    totalHp = 0
    totalIgnoredHp = 0
    numerator = 0

    for rawLine in rawList:
        if ("(" not in rawLine and "hp" in rawLine):
            line = rawLine.replace(u'\xa0', u' ')
            finalList.append(line)
            key = re.findall(gradeRe, line)[-1]
            grade = gradeDictionary[key]
            hp = float(re.findall(hpRe, line)[-1].replace(",","."))
            numerator += hp*grade
            if (key!="P"):
                totalHp += hp
            else:
                totalIgnoredHp += hp
            print(line)
    gpa = numerator/totalHp
    return gpa

if __name__ == '__main__': app.run(debug=True)