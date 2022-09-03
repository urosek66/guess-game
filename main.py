from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        secret_number = request.cookies.get("secret_number")

        response = make_response(render_template("index.html"))
        if not secret_number:
            random_number = random.randint(1, 30)
            response.set_cookie("secret_number", str(random_number))

        return response

    elif request.method == "POST":
        secret_number = int(request.cookies.get("secret_number"))
        user_guess = int((request.form.get("number")))

        if secret_number == user_guess:
            text = "Congratulations your are correct."
            play_again = "Start over"
            response = make_response(render_template("result.html", text=text, play_again=play_again))
            response.set_cookie("secret_number", str(random.randint(1, 30)))

            return response

        elif secret_number > user_guess:
            text = "Sorry your guess is to small."
            play_again = "Play again"
            return render_template("result.html", text=text, play_again=play_again)

        else:
            text = "Sorry your guess is to big."
            play_again = "Play again"
            return render_template("result.html", text=text, play_again=play_again)


if __name__ == '__main__':
    app.run(debug=True)
