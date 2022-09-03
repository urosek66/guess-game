from flask import Flask, render_template, request, make_response
import random

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":

        secret_number = request.cookies.get("number")

        if not secret_number:
            secret_number = random.randint(1, 30)
            response = make_response(render_template("index.html"))
            response.set_cookie("secret_num", str(secret_number))

            return response

    elif request.method == "POST":
        secret_number = request.cookies.get("secret_num")
        user_guess = request.form.get("number")

        if secret_number == user_guess:
            text = "Congratulations your are correct."
            return render_template("result.html", text=text)

        elif secret_number > user_guess:
            text = "Sorry your guess is to small."
            return render_template("result.html", text=text)

        else:
            text = "Sorry your guess is to big."
            return render_template("result.html", text=text)


if __name__ == '__main__':
    app.run(debug=True)
