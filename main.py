from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User, db
import random

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        return render_template("index.html")

    elif request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        secret_number = random.randint(1, 30)

        user = User(name=name, email=email, secret_number=secret_number)
        user.save()

        response = make_response(redirect(url_for('game')))
        response.set_cookie("user_name", name)

        return response


@app.route("/game", methods=["GET", "POST"])
def game():
    if request.method == "GET":


        return render_template("game.html")

    elif request.method == "POST":
        user_guess = request.form.get("number")
        user_name = request.cookies.get("user_name")
        user = db.query(User).filter_by(name=user_name).first()
        secret_number = user.secret_number

        if user_guess == secret_number:
            text = "Congratulations your are correct."
            play_again = "Start over"
            new_secret = random.randint(1, 30)
            user.secret_number = new_secret
            user.save()
            response = make_response(render_template("result.html", text=text, play_again=play_again))

            return response

        elif user_guess < secret_number:
            text = "Sorry your guess is to small."
            play_again = "Play again"
            return render_template("result.html", text=text, play_again=play_again)

        elif user_guess > secret_number:
            text = "Sorry your guess is to big."
            play_again = "Play again"
            return render_template("result.html", text=text, play_again=play_again)


if __name__ == '__main__':
    app.run(debug=True)
