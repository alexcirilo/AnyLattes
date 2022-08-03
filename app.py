#coding: UTF-8
from audioop import add
from flask import Flask, url_for
from fileinput import filename
from genericpath import isdir
import glob
import os
from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
#from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy


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


class Projetos(db.Model):
    __tablename__ = 'projetos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(255))
    titulo = db.Column(db.Text)
    ano_inicio = db.Column(db.DateTime)
    natureza = db.Column(db.String(100))
    coordenador = db.Column(db.String(255))
    financiamento = db.Column(db.String(255))
    integrantes = db.Column(db.Text)

    def __init__(self, nome, titulo, ano_inicio, natureza, coordenador, financiamento, integrantes):
        self.nome = nome
        self.titulo = titulo
        self.ano_inicio = ano_inicio
        self.natureza = natureza
        self.coordenador = coordenador
        self.financiamento = financiamento
        self.integrantes = integrantes


db.create_all()


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
                        #coordenador = v.attrib['NOME-COMPLETO']
                        coordenadores.append(v.attrib['NOME-COMPLETO'])
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
        print(coord)
        print(projeto)
        print(ano_inicio)
        print(natureza)
        print(coordenadores)
        print(integra)
        print(fin)
    '''
        for m in range(0, len(curriculos)):
            tree2 = ET.parse(curriculos[m])
            root2 = tree2.getroot()

            coord = []

            for t2 in root2.iter('DADOS-GERAIS'):  # Imprimir nome do professor
                coord.append(t2.attrib['NOME-COMPLETO'])

            integrantes = []
            financiamento = []
            for t in root2.iter('PARTICIPACAO-EM-PROJETO'):

                entra = False
                coordenador = ""

                for v in t.iter():
                    if v.tag == 'PROJETO-DE-PESQUISA' and not v.attrib['ANO-FIM']:
                        #print(v.attrib)
                        projeto = v.attrib['NOME-DO-PROJETO']
                        ano_inicio = v.attrib['ANO-INICIO']
                        ano_fim = v.attrib['ANO-FIM'] or "Atual"
                        natureza = v.attrib['NATUREZA']
                        entra = True

                        #print(i, 0, coord)
                        print(i, 1, projeto)
                        entra = True

                        financiamento = []
                        coordenador = ""

                    if entra and v.tag == 'INTEGRANTES-DO-PROJETO':
                        integrantes.append(v.attrib['NOME-COMPLETO'])

                        if v.attrib['FLAG-RESPONSAVEL'] == "SIM" and coordenador == "":
                            coordenadores.append(v.attrib['NOME-COMPLETO'])

                    if entra and v.tag == 'FINANCIADOR-DO-PROJETO':
                        financiamento.append(v.attrib['NOME-INSTITUICAO'])

            if projeto:
                prod = "\n".join(projeto)
                #save = Titulo(projeto)
                print(prod)

            print(integrantes)
            print(coord)
            print(projeto)
            print(ano_inicio)
            print(natureza)
            print(coordenadores)
            print(financiamento)
            print(integrantes)

            if coord and projeto and ano_inicio and natureza and coordenadores and financiamento and integrantes:


                save = Projetos(coord,projeto,ano_inicio,natureza,
                                coordenador,financiamento, integrantes)
                db.session.add(save)
                db.session.commit()
                if db.session.commit():
                    flash("Salvo com sucesso!")
                    redirect("projetos.html")
                else:
                    flash("Não foi possível salvar")
                    redirect("index.html")
            '''
    # print(dados)
    '''
    if coord and projeto and ano_inicio and natureza and coordenadores and fin and integra:
        s = Projetos(coord, projeto, ano_inicio, natureza,
                        coordenadores, integra, fin)
        #print(s)
        
        try:
            db.session.add(s)
            db.session.commit()
            flash("Salvo com sucesso!")
        except:
            flash("Não foi possível salvar")
        '''
                
    
    return render_template("projetos.html")


if __name__ == "__main__":
    app.run(debug=True)
