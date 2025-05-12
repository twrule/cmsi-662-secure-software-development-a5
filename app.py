import os
from flask_wtf.csrf import CSRFProtect
from flask import (
    Flask, request, make_response,
    redirect, render_template, g, abort, flash)
from dotenv import load_dotenv
from user_service import get_user_with_credentials_safe, login_required
from card_service import get_card_count, do_transfer, get_pokemon_by_owner, get_pokemon

app = Flask(__name__)

load_dotenv()  # Load environment variables from .env file
SECRET = os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = SECRET
csrf = CSRFProtect(app)  # Enables CSRF protection for all form POSTs


@app.route("/", methods=['GET'])
@login_required
def home():
    return redirect('/dashboard')


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    # Prevent user enumeration by returning the same message regardless of cause
    # of failure
    # This is a common security practice to prevent attackers from guessing
    # valid usernames or emails.
    # If the email is not found, or the password is incorrect, we return the same
    # error message.
    # This way, an attacker cannot determine if the email exists in the system
    # based on the error message.
    user = get_user_with_credentials_safe(email, password)
    if not user:
        # Error message is intentionally vague (user not found vs bad password)
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    # Store authentication securely in cookie; ensure cookie flags set elsewhere
    # (e.g., Secure, HttpOnly)
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    # Alert used for display only; Jinja2 auto-escapes to prevent XSS
    alert = request.args['alert'] if 'alert' in request.args else False
    return render_template("dashboard.html", email=g.user, alert=alert)


@app.route("/details", methods=['GET'])
@login_required
def details():
    pokemon_owned = get_pokemon_by_owner(g.user)
    return render_template(
        "details.html",
        email=g.user,
        pokemons=get_pokemon(pokemon_owned))


@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
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

    card_balance = get_card_count(g.user, pokemon)
    if card_balance is None:
        abort(404, "Account not found")
    if card_count > card_balance:
        abort(400, "You don't have that much")

    if do_transfer(source, target, card_count, pokemon):
        flash(
            f"Successfully transferred {card_count} card(s) of type Pokemon!")
        flash(f"Pokemon ID: {pokemon} transferred to {target}!")

        return render_template(
            "transfer_success.html",
            count=card_count,
            pokemon=pokemon,
            target=target
        )
    else:
        abort(400, "Something bad happened")


@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie('auth_token')
    return response, 303
