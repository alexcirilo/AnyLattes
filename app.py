# -*- coding: utf-8 -*-
from flask import Flask, redirect, render_template, request, flash
from audioop import add
from fileinput import filename
from genericpath import isdir
import glob
import os
from werkzeug.utils import secure_filename
import xml.etree.ElementTree as ET
# import models.graficos as g
from models.corrige_notas import corrige_notas
from models.import_projetos import import_project
from models.load_qualis import load_qualis
from models.consulta import * #lista, busca_prof, soma_nota, contador_estratos



app = Flask(__name__)


# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML','pdf','xls','xlsx'}  # extensões validas

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
                        'arquivos/'+ filename))
                    f = file.filename.rsplit('.',1)[1].lower()
                    dir = 'arquivos/'
                    if f == 'pdf' or f == 'PDF':
                        old = os.path.join(dir,filename)
                        new = os.path.join(dir,'QUALIS_novo.pdf')
                        os.rename(old,new)
                        
                    elif f == 'xls' or f == 'xlsx':
                        old = os.path.join(dir,filename)
                        new = os.path.join(dir,'QualisEventosComp.xls')
                        os.rename(old,new)
                    else :
                        flash("Erro no sistema")
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

@app.route('/import_projetos')
def import_projetos():
    return render_template('projetos.html')

@app.route("/projetos", methods=['POST'])
def projetos():
    if request.method == 'POST':
        anos = request.form.getlist('anos')
    return import_project(anos)



@app.route("/tabela_periodicos_e_qualis")
def gerar_tabela_qualis():
    return render_template('qualis.html'), load_qualis()


@app.route('/listar')
def listar():
    
    contadorEstratos = contador_estratos()
    titulosRepetidos = titulos_qualis()
    for tits in titulosRepetidos:
        for t in tits:
            rep = qualis_repetidos(titulo=t)
            for r in rep:
                print(r)
                if r[0] == t:
                    media = float(r[1]) / float(r[3])
                    update_qualis_repetido(titulo=r[0],valor=str(media))
                    # showinfo(title="VALIDADO",message="Corrigido com Sucesso!")
                    break
    # corrige_notas(titulosRepetidos)
    listar = lista()
    totalNotas = soma_nota()
    return render_template("teste.html", listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)

# def graficos():
#     grafico = g.grafico()
#     return render_template("grafico.html",grafico=grafico)

@app.route('/corrige_notas')
def corrige_notas():
    titulosRepetidos = titulos_qualis()
    for tits in titulosRepetidos:
        for t in tits:
            rep = qualis_repetidos(titulo=t)
            for r in rep:
                print(r)
                if r[0] == t:
                    media = float(r[1]) / float(r[3])
                    update_qualis_repetido(titulo=r[0],valor=str(media))
                    # showinfo(title="VALIDADO",message="Corrigido com Sucesso!")
                    break
    return redirect('/listar')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
