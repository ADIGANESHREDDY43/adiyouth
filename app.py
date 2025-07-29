from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import uuid
import smtplib

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
    db.init_app(app)

    from models import Message

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/send', methods=['POST'])
    def send():
        content = request.form['content']
        email = request.form['email']
        token = str(uuid.uuid4())

        message = Message(token=token, content=content, email=email)
        db.session.add(message)
        db.session.commit()

        link = f"http://localhost:5000/view/{token}"
        send_email(email, link)

        return render_template('success.html', link=link)

    @app.route('/view/<token>')
    def view(token):
        msg = Message.query.filter_by(token=token).first()
        if msg:
            content = msg.content
            db.session.delete(msg)
            db.session.commit()
            return render_template('view.html', content=content)
        return render_template('expired.html')

    def send_email(recipient, link):
        sender = "adiganeshayyappareddykovvuri@gmail.com"
        password = "dxxm mnvt qxeu bfee"
        message = f"Subject:  Your Secure Message\n\nClick to view: {link}"

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, message)

    return app