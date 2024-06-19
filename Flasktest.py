from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from flask_migrate import Migrate, upgrade as upgrade_database

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Ruan:Cenouracj70%@localhost/monitoramento_pacientes' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Jaunfodido' 
app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 587  
app.config['MAIL_USE_TLS'] = True  
app.config['MAIL_USERNAME'] = 'monitoramentocardiaco1@gmail.com'  
app.config['MAIL_PASSWORD'] = 'rwcs wupf jplb jsmu'  
app.config['MAIL_DEFAULT_SENDER'] = 'monitoramentocardiaco1@gmail.com' 
app.config['MAIL_SUBJECT_PREFIX'] = '[Monitoramento Cardíaco]'  
app.config['MAIL_ASCII_ATTACHMENTS'] = False  

app.config['SECURITY_PASSWORD_SALT'] = 'JaunFodido2024'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

plt.switch_backend('agg')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

df = pd.read_json("C:\\Users\\ruang\\Desktop\\curso_python3\\heartrate_auto.json")
df[['date', 'time', 'heartRate']] = df['date;time;heartRate'].str.split(';', expand=True)
df['Data'] = pd.to_datetime(df['Data'])
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], dayfirst=True)
df['heartRate'] = pd.to_numeric(df['heartRate'], errors='coerce')

UPLOAD_FOLDER = os.path.join(app.root_path, 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email

@app.route('/')
def root():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if user.email_confirmed:  
                login_user(user)
                return redirect(url_for('index'))
            else:
                message = 'Necessita verificação do email'
                return redirect(url_for('login', popup_message=message)) 
        else:
            message = 'Login inválido'
            return redirect(url_for('login', popup_message=message))  
    return render_template('login.html', popup_message=request.args.get('popup_message')) 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return redirect(url_for('register', popup_message='Usuário já cadastrado!'))

        try:
            new_user = User(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()

            confirmation_token = generate_confirmation_token(email)
            confirmation_link = f"http://127.0.0.1:8080/confirm/{confirmation_token}"
            msg = Message('Confirme seu email', recipients=[email])
            msg.body = f'Olá {username}, clique neste link para confirmar seu email: {confirmation_link}'
            mail.send(msg)

            return redirect(url_for('login'))

        except IntegrityError:
            db.session.rollback()
            return redirect(url_for('register', popup_message='Endereço de e-mail já em uso!'))

    if request.method == 'GET' or not current_user.is_authenticated:
        popup_message = request.args.get('popup_message', None)
        return render_template('register.html', popup_message=popup_message)


@app.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_confirmed = True
            db.session.commit()
            flash('Seu email foi confirmado com sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Usuário não encontrado!', 'error')
    else:
        flash('Token inválido ou expirado!', 'error')

    return redirect(url_for('login'))

@app.route('/index')
@login_required 
def index():
    usuarios = df['Usuario'].unique()
    popup_message = request.args.get('popup_message')
    return render_template('index.html', usuarios=usuarios, popup_message=popup_message)


@app.route('/plot', methods=['POST'])
@login_required
def plot():
    data_selecionada = pd.to_datetime(request.form['data'])
    usuario_selecionado = request.form['usuario']
    hora_inicio = pd.to_datetime(request.form['hora_inicio']).time()
    hora_fim = pd.to_datetime(request.form['hora_fim']).time()

    dados_selecionados = df.loc[(df['Data'].dt.date == data_selecionada.date()) &
                                (df['Usuario'] == usuario_selecionado) &
                                (df['datetime'].dt.time >= hora_inicio) &
                                (df['datetime'].dt.time <= hora_fim)]

    if dados_selecionados.empty:
        flash("Não há dados para o usuário e data selecionados.", 'info')
        return redirect(url_for('index'))

    grouped_df = dados_selecionados.groupby(dados_selecionados['datetime'].dt.time)['heartRate'].mean()

    x = np.arange(len(grouped_df))
    plt.figure(figsize=(10, 6))
    plt.plot(grouped_df.index.astype(str), grouped_df, color='red', label='Média')
    plt.xlabel('Horário')
    plt.ylabel('Batimentos Cardíacos (média)')
    plt.title(f'Batimentos Cardíacos por Horário - Data: {data_selecionada.date()}, Usuário: {usuario_selecionado}')
    plt.grid(True)
    plt.xticks(np.arange(0, len(grouped_df.index), step=10))
    plt.legend()

    img_path = 'static/plot.png'
    plt.savefig(img_path)
    plt.close()

    return render_template('index.html', img_path=img_path)

if __name__ == '__main__':
    with app.app_context():
        upgrade_database()
    app.run(host='0.0.0.0', port=8080)


