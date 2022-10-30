# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, request, flash
from audioop import add
from fileinput import filename
from genericpath import isdir
import glob
import os
from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
import mysql.connector
import models.connection
from models.import_projetos import import_project
from models.load_qualis import load_qualis

'''
heroku access
'''
'''
user= 'b96e08051c345f'
pwd= '2503c6ba'
host= 'us-cdbr-east-06.cleardb.net'
database= 'heroku_34fb507d853ce4f'
'''
'''
local access
'''
# user = 'root'
# pwd = 'Qwer@1234'
# host = 'localhost'
# database = 'lattes4web'

models.connection.conexao()

app = Flask(__name__)

# try:
#     db = mysql.connector.connect(user=user,password= pwd,host=host, database=database)
#     print("Connected!")
# except:
#     print("YOU SHALL NOT PASS!")

@app.route('/connection')
def connection():
    return render_template('connection.html')


# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML','pdf','xls'}  # extensões validas

# verifica se pasta existe
if os.path.isdir('curriculos'):
    UPLOAD_FOLDER = 'curriculos'
    print('Existe')
else:
    os.mkdir('curriculos')
    UPLOAD_FOLDER = 'curriculos'

if os.path.isdir('arquivos'):
    print('Existe')
else:
    os.mkdir('arquivos')
    
# chave para validar sessão quando ocorre alteração de dados de cookie
app.secret_key = 'lattes4web'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # atribuição da pasta


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/imports", methods=['GET','POST'])
def imports():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        print(files)
        for file in files:
            if file.filename == '':
                flash("No Selected file(s)")
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        'arquivos/', filename))
                    flash('File(s) uploaded successfully')
                else:
                    flash(
                        "Não foi possível efetuar upload. Arquivo com extensão inválida")
    return render_template('imports.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        print(files)
        for file in files:
            if file.filename == '':
                flash("No Selected file(s)")
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(
                        app.config['UPLOAD_FOLDER'], filename))
                    flash('File(s) uploaded successfully')
                else:
                    flash(
                        "Não foi possível efetuar upload. Arquivo com extensão inválida")
        return redirect('/')


@app.route("/projetos")

def projetos():
    
    return import_project()

@app.route("/tabela_periodicos_e_qualis")
def gerar_tabela_qualis():
    return render_template('qualis.html'), load_qualis()



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
