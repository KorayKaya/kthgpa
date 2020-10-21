from flask import Flask, render_template, request, redirect
from tika import parser
from werkzeug.utils import secure_filename
import re
import os
import tempfile, datetime

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        with tempfile.TemporaryDirectory() as tempdirectory:
            uploaded_file = request.files['file']
            if "pdf" not in uploaded_file.filename:
                return render_template('index.html', gpa="0")
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(tempdirectory, filename))
            date_from = request.form.get('date_from')
            date_to = request.form.get('date_to')
            print(date_from,date_to)
            # try:
            gpa, ignoredhp, totalhp = calcGPA(os.path.join(tempdirectory, filename),date_from,date_to)
            return render_template('index.html', gpa=str(gpa), ignoredHP=ignoredhp, totalHP=totalhp)
            # except:
            #     return render_template('index.html', gpa="0")
    else:
        return render_template('index.html', gpa="0")

def calcGPA(file,date_from,date_to):
    gradeDictionary = {
        "A":5,
        "B":4.5,
        "C":4,
        "D":3.5,
        "E":3,
        "F":0,
        "P":0
    }

    datetime_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    datetime_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')

    rawText = parser.from_file(file)

    rawList = rawText['content'].splitlines()

    gradeRe = "\\b[A-Z]\\b"
    hpRe = "\\d+,\\d"

    totalHp = 0
    totalIgnoredHp = 0
    numerator = 0

    for rawLine in rawList:
        if ("(" not in rawLine and "hp" in rawLine):
            line = rawLine.replace(u'\xa0', u' ').replace(u'\xad', u'-')

            course_date = datetime.datetime.strptime(line.split(" ")[-2], '%Y-%m-%d')
            if (course_date < datetime_to and course_date > datetime_from):
                key = re.findall(gradeRe, line)[-1]
                grade = gradeDictionary[key]
                hp = float(re.findall(hpRe, line)[-1].replace(",","."))
                numerator += hp*grade
                if (key!="P"):
                    totalHp += hp
                else:
                    totalIgnoredHp += hp
    gpa = numerator/totalHp
    return gpa,totalIgnoredHp,(totalHp+totalIgnoredHp)

if __name__ == '__main__': app.run(debug=True)