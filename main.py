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

        secret_number = random.randint(1, 30)

        user = db.query(User).filter_by(email=email).first()

        if not user:
            user = User(name=name, email=email, password=hashed_password, secret_number=secret_number)
            user.save()

        if hashed_password != user.password:
            return "WRONG PAASSWORD! Try again"

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

        if user_guess == user.secret_number:
            text = "Congratulations your are correct."
            play_again = "Start over"
            new_secret = random.randint(1, 30)
            user.secret_number = new_secret
            user.save()
            response = make_response(render_template("result.html", text=text, play_again=play_again))

            return response

        elif user_guess < user.secret_number:
            text = "Sorry your guess is to small."
            play_again = "Play again"
            return render_template("result.html", text=text, play_again=play_again)

        elif user_guess > user.secret_number:
            text = "Sorry your guess is to big."
            play_again = "Play again"
            return render_template("result.html", text=text, play_again=play_again)


if __name__ == '__main__':
    app.run(debug=True)
