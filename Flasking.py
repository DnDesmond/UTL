from flask import Flask, redirect, url_for, request, render_template
import os
app = Flask(__name__, template_folder="", static_folder="")

# @app.route('/', methods=['GET',"POST"])
# def squarenumber():
#     if request.method == "POST":
#         if request.form["num"] == "":
#             return "<html><body><h1>Invalid Number</h1></body></html>"
#         else:
#             number = request.form["num"]
#             sq = str(int(number)**2)
#             return render_template("answer.html", squareofnum=sq, num=number)
#     if request.method == "GET":
#         return render_template("squarenum.html")

# @app.route("/admin")
# def hello_admin():
#     strung = "<br>We have successfully harvested many gallons of orphan's blood and have barreled them to extend their shelf lives!"
#     return f"Greetings <b><i>Administrator</i></b> {strung}"

# @app.route("/", methods=["GET","POST"])
# def enter_name():
#     if request.method == "POST":
#         if request.form["name"] == "admin":
#             return redirect(url_for("hello_admin"))
#         if "0" in request.form["name"]:
#             return render_template("namenter.html")
#         elif request.form["name"] == "Thy Name If Thou Darest Mortal":
#             return render_template("funny.html", extra="You really went the extra mile didn't you!")
#         elif "Thy Name" in request.form["name"]:
#             return render_template("funny.html", extra="")
#         else:
#             # return redirect(f"/{request.form["name"]}")
#             return render_template("greets.html", name=request.form["name"])
#     if request.method == "GET":
#         return render_template("namenter.html")

from non import translator
@app.route("/", methods=["GET","POST"])
def enter_all():
    try:
        if request.method == "POST":
            for key,thought in request.form.items():
                if key != "submit" and key != "current":
                    if thought == "1":
                        raise ValueError
                    if int(thought)<=0:
                        raise ValueError
                    if int(thought) > 62:
                        raise ValueError
            base_1 = request.form["firstb"]
            base_2 = request.form["secondb"]
            current_value = request.form["current"]
            return render_template("basic.html",result=translator(current_value, int(base_1), int(base_2)), nombre=current_value, starter=base_1, ender=base_2)
        elif request.method == "GET":
            return render_template("basic.html", nombre="4", starter="10", ender="2")
    except ValueError:
        return redirect("/")

from viper import venom
@app.route("/viper", methods=["GET","POST"])
def bite():
    if request.method == "POST":
        first: str = request.form["first"]
        second: str = request.form["second"]
        result = venom(first, second)
        return render_template("fang.html",result=result, first=first, second=second)
    elif request.method == "GET":
        return render_template("fang.html",result="", first=1, second=1)

if __name__ == '__main__':
    app.run()