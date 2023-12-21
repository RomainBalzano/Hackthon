
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from smtpd import SMTPServer
from flask import Flask, request, render_template, redirect, url_for,session, send_file
from flask_mail import Mail, Message
import secrets
import json
import pdfkit
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hackthonedfgroupe15@gmail.com'
app.config['MAIL_PASSWORD'] = 'ridz syqg tioe uyga'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
PDF_FOLDER = 'pdf'
app.config['PDF_FOLDER'] = PDF_FOLDER
mail = Mail(app)
app.secret_key = secrets.token_hex(16)

@app.route("/")
def index():
    return redirect("/home")

@app.route("/home")
def hello_world():
    return render_template("home.html")

@app.route("/define_user")
def define_user():
    #à utiliser sous forme de 
    # http://127.0.0.1:5000/define_user?name=testnom&firstname=prenom
    session["username"] = request.args.get('name')
    session["firstname"] = request.args.get('firstname')
    session["score"] = 0
    return redirect("/home")

@app.route("/test")
def test():
    session["username"] = "test"
    session["firstname"] = "test2"
    session["score"] = 200
    return redirect("/home")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            session["username"] = username
            session["score"] = score
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")
    
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        return redirect(url_for("Home"))
    
    return redirect("/")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/profile")

def profil():
    if not session.get("name"):
        return redirect("/home")
    return render_template("profile.html")


@app.route("/stats")
def stats():
    if not session.get("name"):
        return redirect("/home")
    return render_template("stats.html")

@app.route("/game")
def game():
    if not session.get("name"):
        return redirect("/login")
    return render_template("game.html")

@app.route("/game/board")
def game_board():
    if not session.get("name"):
        return redirect("/login")
    return render_template("game_board.html")

@app.route("/game/home" )
def game_home():
    with open('./question/home.json') as file:
            data = json.load(file)
    return data

@app.route("/game/score/<int:score>")
def game_score(score):
    session[score]=session[score]+score

@app.route("/game/route")
def game_route():
    with open('./question/home.json') as file:
            data = json.load(file)
    return data

@app.route("/game/work")
def game_work():
    with open('./question/home.json') as file:
            data = json.load(file)
    return data
@app.route("/leaderboard/get")
def leaderboard_get():
    with open('./question/leaderboard.json') as file:
            data = json.load(file)
    return data

@app.route("/leaderboard/")
def leaderboard():
    return render_template("leaderboard.html")


    
@app.route("/certification")
def download_pdf():
    if not session.get("name") and not session.get("score"):
        return redirect("/home")
    
    if session.get("score")<100:
        return redirect("/home")
    
    username = session.get("username")
    score = session.get("score")
    
    config=pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe') 
    html_content = f"<h1>Score: {score}</h1><h2>Username: {username}</h2>"
    
    pdfkit.from_string(html_content, 'certificat.pdf',configuration=config)
    pdf_file_path = 'certificat.pdf'
    return send_file(pdf_file_path, as_attachment=True)

@app.route("/certification/send")
def send_pdf():
    if not session.get("name") and not session.get("score"):
        return redirect("/login")
    
    if session.get("score")<100:
        return redirect("/home")
    
    
    username = session.get("username")
    score = session.get("score")
    config=pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe') 
    html_content = f"<h1>Score: {score}</h1><h2>Username: {username}</h2>"
    pdfkit.from_string(html_content, 'certificat.pdf',configuration=config)
    msg = Message(subject='Eco Certificat de HACKTHON groupe 15', sender='hackthonedfgroupe15@gmail.com', recipients=['shinatu1905@gmail.com'])
    msg.body = f"Hey {username}, Voici votre eco-certificat !Pour rappel votre score etait de {score}"
    with app.open_resource("certificat.pdf") as pdf:
        msg.attach("certificat.pdf", "application/pdf", pdf.read())
    
    mail.send(msg)
    return "Message sent!"
    

if __name__ == '__main__':

    app.run(debug=True)