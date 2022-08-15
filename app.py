#coding: UTF-8
from flask import Flask, redirect, render_template, request, flash
from audioop import add
from fileinput import filename
from genericpath import isdir
import glob
import os
from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
import mysql.connector
from models.load_qualis import load_qualis

'''
heroku access
'''

user= 'b96e08051c345f'
pwd= '2503c6ba'
host= 'us-cdbr-east-06.cleardb.net'
database= 'heroku_34fb507d853ce4f'

'''
local access
user = 'root'
pwd = 'Qwer#1234'
host = 'localhost'
database = 'lattes4web'
'''

app = Flask(__name__)

try:
    db = mysql.connector.connect(user=user,password= pwd,host=host, database= database)
    print(db)
except:
    print("not connect")

@app.route('/connection')
def connection():
    return render_template('connection.html')


# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML','pdf','xls'}  # extensões validas

# verifica se pasta existe
if os.path.isdir('curriculos'):
    UPLOAD_FOLDER = 'curriculos'
else:
    os.mkdir('curriculos')
    os.mkdir('arquivos')
    UPLOAD_FOLDER = 'curriculos'

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
    cont = 0
    curriculos = []
    projeto = []
    dados = []
    ano_inicio = []
    ano_fim = []
    natureza = []
    coordenadores = []

    for f in glob.glob('curriculos/*.xml'):
        curriculos.append(f)
        cont = cont+1

    curriculos.sort()
    i = 1
    print("currículos importados: "+str(cont))
    for m in range(0, len(curriculos)):
        tree = ET.parse(curriculos[m])
        root = tree.getroot()
        coord = ""
        for t in root.iter('DADOS-GERAIS'):
            coord = t.attrib['NOME-COMPLETO']
            #print (coord)

        integrantes = []
        financiamento = []
        temp = 0
        for t in root.iter('PARTICIPACAO-EM-PROJETO'):
            # print(t)

            entra = False

            coordenador = ""

            for v in t.iter():
                # print(v)
                if v.tag == 'PROJETO-DE-PESQUISA' and not v.attrib['ANO-FIM']:
                    # print(v.attrib)
                    projeto = v.attrib['NOME-DO-PROJETO']
                    ano_inicio = v.attrib['ANO-INICIO']
                    ano_fim = v.attrib['ANO-FIM'] or "Atual"
                    natureza = v.attrib['NATUREZA']
                    entra = True
                    # print(coord)
                    # print(projeto)
                    # print(ano_inicio)
                    #print( natureza)

                    temp = i
                    i = i+1
                    financiamento = []
                    coordenador = ""

                if entra and v.tag == 'INTEGRANTES-DO-PROJETO':
                    integrantes.append(v.attrib['NOME-COMPLETO'])
                    #print(v.attrib['NOME-COMPLETO'],v.attrib['FLAG-RESPONSAVEL'], coordenador)
                    if v.attrib['FLAG-RESPONSAVEL'] == "SIM" and coordenador == "":
                        coordenadores = v.attrib['NOME-COMPLETO']
                        
                        
                        # print(coordenador)
                        #worksheet.write(temp, 4, coordenador)

                if entra and v.tag == 'FINANCIADOR-DO-PROJETO':
                    financiamento.append(v.attrib['NOME-INSTITUICAO'])

            if entra:
                integra = ', '.join(set(integrantes))
                # print(integra)
            if entra:
                fin = ', '.join(set(financiamento))
                # print(fin)
                
                c = db.cursor()
                
                data  = """ insert into projetos (nome,titulo, ano_inicio, natureza, coordenador, financiamento, integrantes)
                                VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                                            
                c.execute(data,(coord,projeto,ano_inicio,natureza,coordenadores, fin , integra))
                db.commit()
                c.close()
        
    return render_template("projetos.html")

@app.route("/tabela_periodicos_e_qualis")
def gerar_tabela_qualis():
    return render_template('qualis.html'), load_qualis()


if __name__ == "__main__":
    app.run()
