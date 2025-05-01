from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    # For now, we're just getting started, so assume login is
    # always okay and just deliver a fake authentication token.
    # We'll do real auth later after the XSS and CSRF demos.
    request.form.get("email")
    request.form.get("password")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", "Fake-token-for-now")
    return response, 303


@app.route("/dashboard", methods=['GET'])
def dashboard():
    return render_template("dashboard.html")


@app.route("/details", methods=['GET', 'POST'])
def details():
    account_number = request.args['account']
    return render_template("details.html", account_number=account_number)


@app.route("/transfer", methods=["GET"])
def transfer():
    return render_template("transfer.html")
