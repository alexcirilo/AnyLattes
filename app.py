#coding: UTF-8
from crypt import methods
from fileinput import filename
from genericpath import isdir
import glob
import os
from flask import Flask, redirect, render_template, request, flash
from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
from flask_sqlalchemy import SQLAlchemy

from models.tables import Projetos

# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML'}  # extensões validas

# verifica se pasta existe
if os.path.isdir('curriculos'):
    UPLOAD_FOLDER = 'curriculos'
else:
    os.mkdir('curriculos')
    UPLOAD_FOLDER = 'curriculos'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Qwer#1234@localhost/lattes4web'
db = SQLAlchemy(app)


@app.route('/connection')
def connection():
    return render_template('connection.html')

# chave para validar sessão quando ocorre alteração de dados de cookie
app.secret_key = 'files'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # atribuição da pasta


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('index.html')


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
    cont = 0
    curriculos = []
    for f in glob.glob('curriculos/*'):
        curriculos.append(f)
        cont = cont+1

        curriculos.sort()
        # for line in open(f):
        #print (line)
        for m in range(0, len(curriculos)):
            tree2 = ET.parse(curriculos[m])
            root2 = tree2.getroot()
            for t2 in root2.iter('DADOS-GERAIS'):  # Imprimir nome do professor
                nomeProf = (t2.attrib['NOME-COMPLETO'])
                for t in root2.iter('PARTICIPACAO-EM-PROJETO'):
                    for v in t.iter():
                        if v.tag == 'PROJETO-DE-PESQUISA' and not v.attrib['ANO-FIM']:
                            projeto = v.attrib['NOME-DO-PROJETO']
                            ano_inicio = v.attrib['ANO-INICIO']
                            ano_fim = v.attrib['ANO-FIM'] or "Atual"
                            natureza = v.attrib['NATUREZA']
                            #print(t2.attrib['NOME-COMPLETO'])
                            dados = v.attrib
                            
                            
                
    return render_template("projetos.html", registros=dados)


if __name__ == "__main__":
    app.run(debug=True)
