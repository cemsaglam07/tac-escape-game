import os
import time
from flask import Flask, render_template, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.utils import secure_filename
from helpers import apology, valid_group, valid_question
from questions import control


# Constant variable names:
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'py'}

# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["GET", "POST"])
# @login_required  # Sessions expire quickly, had to disable login/register feature
def process():
    """Get text file from user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure method was uploaded
        if not request.form.get("group"):
            return apology("must provide group name", 400)
        if not request.form.get("question"):
            return apology("must specify which question", 400)
        # query database for question and method
        group = valid_group(request.form.get("group"))
        question = valid_question(request.form.get("question"))
        # ensure method is method
        if group == "":
            return apology("group name not valid", 400)
        if question == "":
            return apology("question number not valid", 400)
        # check if the post request has the file part
        if 'file' not in request.files:
            return apology("no file part", 400)
        file = request.files['file']
        # if user does not select file, browser also submit an empty part without filename
        if not file:
            return apology("did you upload a file?", 400)
        if file.filename == "":
            return apology("no selected file", 400)
        if not allowed_file(file.filename):
            return apology("the file type is not permitted", 400)
        filename = secure_filename(file.filename)
        filename = f"{filename.rsplit('.', 1)[0].lower()}_{group}_{question}_{round(time.time() * 1000)}.{filename.rsplit('.', 1)[1].lower()}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        given = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(given, "r") as f:
            attempt = f.read()
        returned_file = control(question, os.path.join(app.config['UPLOAD_FOLDER'], filename), attempt)
        with open(returned_file, "r") as f:
            returned = f.read().splitlines()
        os.remove(returned_file)
        return render_template("processed.html", returned=returned)

    else:
        return render_template("process.html")

# Pages for questions will remain private until the contest is over.

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
