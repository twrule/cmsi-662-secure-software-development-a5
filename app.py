from flask_wtf.csrf import CSRFProtect
from flask import (
    Flask, request, make_response,
    redirect, render_template, g, abort)
from user_service import get_user_with_credentials_safe, logged_in
from account_service import get_balance, do_transfer, get_pokemon_by_owner, get_pokemon

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e783eeb139649d3fabc370700eeca1511297438ee89265410b282b05292df010'
csrf = CSRFProtect(app)


@app.route("/", methods=['GET'])
def home():
    if not logged_in():
        return render_template("login.html")
    return redirect('/dashboard')


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials_safe(email, password)
    if not user:
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/dashboard", methods=['GET'])
def dashboard():
    if not logged_in():
        return render_template("login.html")
    alert = request.args['alert'] if 'alert' in request.args else False
    return render_template("dashboard.html", email=g.user, alert=alert)


@app.route("/details", methods=['GET'])
def details():
    if not logged_in():
        return render_template("login.html")
    account_number = request.args['account']
    pokemon_owned = get_pokemon_by_owner(account_number)
    return render_template(
        "details.html",
        user=g.user,
        pokemons=get_pokemon(pokemon_owned))


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if not logged_in():
        return render_template("login.html")

    if request.method == "GET":
        return render_template("transfer.html", user=g.user)

    source = request.form.get("from")
    target = request.form.get("to")

    if source == target:
        abort(400, "You can't transfer to yourself")

    try:
        pokemon = request.form.get("pokemon")
    except ValueError:
        abort(400, "Invalid pokemon, need a name")

    try:
        card_count = int(request.form.get("card"))
    except ValueError:
        abort(400, "Invalid card count, need a number")

    if card_count < 0:
        abort(400, "NO STEALING")
    if card_count > 10:
        abort(400, "WOAH THERE TAKE IT EASY")

    available_balance = get_balance(g.user, pokemon)
    if available_balance is None:
        abort(404, "Account not found")
    if card_count > available_balance:
        abort(400, "You don't have that much")

    alert = False

    if do_transfer(source, target, card_count, pokemon):
        alert = True
    else:
        abort(400, "Something bad happened")

    response = make_response(redirect("/dashboard?alert=" + str(alert)))
    return response, 303


@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie('auth_token')
    return response, 303
