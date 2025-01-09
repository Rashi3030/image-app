from flask import Flask

app = Flask(__name__)

@app.route("/")
def student_intro():
    name = "Rashika"
    age = 20
    course = "BCA"
    return 
 

