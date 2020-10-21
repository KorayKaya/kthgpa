# #
# # pip install tika
# # Sen ha intyget som "Intyg.pdf" i samma mapp
# #
# from tika import parser
# import re

# gradeDictionary = {
#     "A":5,
#     "B":4.5,
#     "C":4,
#     "D":3.5,
#     "E":3,
#     "F":0,
#     "P":0
# }

# rawText = parser.from_file('Intyg.pdf')

# rawList = rawText['content'].splitlines()
# finalList  = []

# gradeRe = "\\b[A-Z]\\b"
# hpRe = "\\d+,\\d"

# totalHp = 0
# totalIgnoredHp = 0
# numerator = 0

# for rawLine in rawList:
#     if ("(" not in rawLine and "hp" in rawLine):
#         line = rawLine.replace(u'\xa0', u' ')
#         finalList.append(line)
#         key = re.search(gradeRe, line).group(0)
#         grade = gradeDictionary[key]
#         hp = float(re.search(hpRe, line).group(0).replace(",","."))
#         numerator += hp*grade
#         if (key!="P"):
#             totalHp += hp
#         else:
#             totalIgnoredHp += hp
#         print(line)

# print("")
# print("############")
# print("GPA:",numerator/totalHp)
# print("Total used HP:",totalHp)
# print("Ignored P hp:",totalIgnoredHp)
# print("Total studied:",totalHp+totalIgnoredHp)
# input("Press any key to close...")

import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)