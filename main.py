from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db
import random
import uuid
import hashlib

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        return render_template("index.html")

    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("user_password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        attempts = 0


        secret_number = random.randint(1, 30)

        user = db.query(User).filter_by(email=email).first()

        if not user:
            user = User(name=name, email=email, password=hashed_password, secret_number=secret_number, attempts=attempts)
            user.save()

        if name == "":

            return "Please type your name"

        elif email == "":

            return "Please type your email"

        elif user.deleted == True:

            return "This profile has been deleted"

        elif hashed_password != user.password:
            return "WRONG PAASSWORD try again"

        elif hashed_password == user.password:
            session_token = str(uuid.uuid4())

            user.session_token = session_token
            user.save()


        response = make_response(render_template("game.html", user=user.name))
        response.set_cookie("session_token", session_token, httponly=True, samesite='Strict')

        return response


@app.route("/game", methods=["GET", "POST"])
def game():

    if request.method == "GET":
        session_token = request.cookies.get("session_token")
        if session_token:
            user = db.query(User).filter_by(session_token=session_token).first()
        else:
            user = None

        return render_template("game.html", user=user.name)

    elif request.method == "POST":
        user_guess = int(request.form.get("number"))
        session_token = request.cookies.get("session_token")
        user = db.query(User).filter_by(session_token=session_token).first()
        attempts = user.attempts
        attempts += 1
        best_score = user.best_score

        if user_guess == user.secret_number:
            text = f"Congratulations you are correct the number was {user.secret_number}. You had {user.attempts + 1} attempts."
            play_again = "Start over"
            new_secret = random.randint(1, 30)
            user.secret_number = new_secret
            user.attempts = attempts

            user.save()

            if not best_score:
                user.best_score = user.attempts
                user.save()

            elif attempts < best_score:
                user.best_score = user.attempts
                user.save()

            user.attempts = 0
            user.save()

            response = make_response(render_template("result.html", text=text, play_again=play_again,))

            return response

        elif user_guess < user.secret_number:
            text = "Sorry your guess is to small."
            play_again = "Play again"
            user.attempts = attempts
            user.save()
            return render_template("result.html", text=text, play_again=play_again)

        elif user_guess > user.secret_number:
            text = "Sorry your guess is to big."
            play_again = "Play again"
            user.attempts = attempts
            user.save()
            return render_template("result.html", text=text, play_again=play_again)


@app.route("/profile", methods=["GET"])
def profile():
    session_token = request.cookies.get("session_token")

    # get user from the database based on her/his email address
    user = db.query(User).filter_by(session_token=session_token).first()

    if user:
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for("index"))


@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    session_token = request.cookies.get("session_token")

    # get user from the database based on her/his email address
    user = db.query(User).filter_by(session_token=session_token).first()

    if request.method == "GET":
        if user:  # if user is found
            return render_template("profile_edit.html", user=user)
        else:
            return redirect(url_for("index"))

    elif request.method == "POST":
        name = request.form.get("profile-name")
        email = request.form.get("profile-email")
        password = request.form.get("profile-password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user.name = name
        user.email = email
        user.password = hashed_password

        user.save()

        return redirect(url_for("profile"))


@app.route("/profile/delete", methods=["GET", "POST"])
def profile_delete():
    session_token = request.cookies.get("session_token")

    user = db.query(User).filter_by(session_token=session_token).first()

    if request.method == "GET":
        if user:
            return render_template("profile_delete.html", user=user)
        else:
            return redirect(url_for("index"))

    elif request.method == "POST":

        user.deleted = True
        user.save()

        return redirect(url_for("index"))


@app.route("/users", methods =["GET"])
def all_user():
    users = db.query(User).filter_by(deleted=False).all()

    return render_template("users.html", users=users)


@app.route("/score", methods=["GET"])
def score_list():
    users = db.query(User).filter_by(deleted=False).order_by("best_score").all()

    return render_template("best_score.html", users=users)


@app.route("/user/<user_id>")
def user_details(user_id):
    user = db.query(User).get(int(user_id))

    return render_template("user_details.html", user=user)

if __name__ == '__main__':
    app.run(debug=True)
