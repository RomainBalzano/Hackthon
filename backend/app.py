
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os
from smtpd import SMTPServer
import time
from flask import Flask, request, render_template, redirect, url_for,session,jsonify, send_file
from flask_mail import Mail, Message
import secrets
import json
import pdfkit

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
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
    session["username"] = "test"
    session["nom"]
    session["score"] = 200
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    msg = Message(subject='Hello from the other side!', sender='hackthonedfgroupe15@gmail.com', recipients=['shinatu1905@gmail.com'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    with app.open_resource("certificat.pdf") as pdf:
        msg.attach("certificat.pdf", "application/pdf", pdf.read())
    
    mail.send(msg)
    return "Message sent!"
    

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
        return redirect("/login")
    return "<p>Hello, World!</p>"

@app.route("/stats")
def stats():
    if not session.get("name"):
        return redirect("/login")
    return "<p>Hello, World!</p>"

@app.route("/game/board")
def game_board():
    if not session.get("name"):
        return redirect("/login")
    return "<p>Hello, World!</p>"

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

@app.route("/certification")
def download_pdf():
    if not session.get("name") and not session.get("score"):
        return redirect("/login")
    
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
    
    pdfkit.from_string(html_content, 'certificat.pdf', configuration=config)
    
    msg = Message(subject='Eco Certificat de HACKTHON groupe 15', sender='hackthonedfgroupe15@gmail.com', recipients=['shinatu1905@gmail.com'])
    msg.body = f"Hey {username}, Voici votre eco-certificat !Pour rappel votre score était de {score}"
    with app.open_resource("certificat.pdf") as pdf:
        msg.attach("certificat.pdf", "application/pdf", pdf.read())
    
    mail.send(msg)
    return "Message sent!"
    
    
   




  


if __name__ == '__main__':

    app.run(debug=True)