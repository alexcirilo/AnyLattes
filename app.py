# -*- coding: utf-8 -*-
# import mysql.connector
from flask import Flask,jsonify, redirect, render_template, request, flash
import glob
import os
from werkzeug.utils import secure_filename
from models.import_projetos import import_project
from models.consulta import *
from models.docente import *
from models.crud import *
import json
import plotly
import plotly.express as px
from models.grafico import graficos
from models.grafico import pizza
from models.grafico import *
import models.BaseDeCorrecoes
import models.connection as database
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()


# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML','pdf','xls','xlsx'}  # extensões validas

# verifica se pasta existe
if os.path.isdir('curriculos'):
    UPLOAD_FOLDER = 'curriculos'
    print('Existe a pasta Currículos')
else:
    os.mkdir('curriculos')
    UPLOAD_FOLDER = 'curriculos'

if os.path.isdir('arquivos'):
    print('Existe a pasta Arquivos')
else:
    os.mkdir('arquivos')
    
if os.path.isdir('static/images'):
    print('Existe a pasta Images')
else:
    os.mkdir('static/images')
    os.mkdir('static/images/nuvem_docente')
    
# chave para validar sessão quando ocorre alteração de dados de cookie
app.secret_key = 'lattes4web'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # atribuição da pasta


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/imports", methods=['GET','POST']) #upload arquivos qualis
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
                        new = os.path.join(dir,'QualisConferencias.xlsx')
                        os.rename(old,new)
                    else :
                        flash("Erro no sistema")
                    flash('File(s) uploaded successfully')
                else:
                    flash(
                        "Não foi possível efetuar upload. Arquivo com extensão inválida")
    return render_template('imports.html')


@app.route("/upload", methods=['GET', 'POST']) #upload currículos
def upload():
    if request.method == 'POST':
        for f in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
        files = request.files.getlist('files[]')
        # print(files)
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
        anos = []
        result = []
        ano_inicio = request.form.get('ano_inicio')
        ano_fim = request.form.get('ano_fim')
        
        page = "upload"
        return render_template('loading.html', inicio=ano_inicio, fim=ano_fim, page=page)


@app.route('/resultado_total')
def resultado_total():
    
    dados = todosContador()
    
    listar = lista()
    totalNotas = soma_nota()
    contadorEstratos = total_estratos()

    conteudo = {}
    div = []
    for d in dados:
        conteudo = {'Ano':d[0],'Estratos':d[1],'Quantidade':d[2]}
        div.append(conteudo)
        conteudo = {}
    json_object = json.dumps(div,indent=4)
    with open("todos.json","w") as outfile:
        outfile.write(json_object)
    
    with open('todos.json','r') as file:
        data = json.load(file)
        
        
    fig = px.bar(data,x='Ano',y='Quantidade', color='Estratos', barmode='stack')
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    anos  = []
    for c in data:
        anos.append(c['Ano'])
        
    anos = sorted(set(anos))
    print (anos)
    names = []
    values = []
    pizza()
    with open ('pizza.json','r') as piz:
        d = json.load(piz)
        names.append(d[0]['Conferencia'])
        names.append(d[0]['Periodico'])
        values.append(d[0]['PercConferencia'])
        values.append(d[0]['PercPeriodico'])
        
    figs = px.pie(names=names,values=values)
    
    graph = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)  
    
    grafico_media()
    with open ('media_docentes.json','r') as med:
        dados = json.load(med)
    
    
    docente = []
    media = []
    mediana = []
    m = []
    for d in dados:
        docente.append(d['Docente'])
        media.append(d['Média'])
        mediana.append(d['Mediana'])
        
    m.append(dados[-1]['Mediana'])
    print(m)
    val1 = str(m[-1])
    figura = px.bar(dados,x='Docente',y='Média',color_discrete_sequence=px.colors.qualitative.T10,template='plotly_white',text='Média')
    figura.add_scatter(x=docente,y=mediana,xaxis='x',name="Mediana: "+val1,marker=dict(color="crimson"))
    
    figura.update_layout( 
        yaxis=dict(
            tickmode="array",
            tickfont=dict(size=15)
            ,tickangle=0
        ),
        font=dict(size=12)
    )
    figura.update_traces(
        textfont_size=15,texttemplate='%{text:.3rs}')
    figura.update_yaxes(showticklabels=True)
    
    medias = json.dumps(figura,cls=plotly.utils.PlotlyJSONEncoder)
    
    colaboracao  = grafico_colaboracao()
    
    valor_padrao = 'circular'
    
    tipo_grafo(valor_padrao,colaboracao)
    
    titulosRepetidos = titulos_qualis()
    
    return render_template("resultados.html", anos=anos ,graphJSON=graphJSON, graph=graph, medias=medias, listar = listar, totalNotas = totalNotas,
                           contadorEstratos = contadorEstratos, data=data, titulosRepetidos=titulosRepetidos)


@app.route("/projetos/inicio=<inicio>&fim=<fim>", methods=['POST'])
def projetos(inicio,fim):
    if request.method == 'POST':
        anos = []
        result = []
        ano_inicio = inicio
        ano_fim = fim
        
        for r in range(int(ano_inicio),int((ano_fim))+1):
            anos.append(r)
            r+1

    return import_project(anos)

@app.route("/tabela_periodicos_e_qualis")
def gerar_tabela_qualis():
    return render_template('qualis.html'), load_qualis()


@app.route('/resultado_por_docente')
def resultado_por_docente():  
    
    listar = lista()
    #prof = busca_prof()
    totalNotas = soma_nota()
    contadorEstratos = contador_estratos()
    return render_template("resultados_por_docente.html", listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)

@app.route('/listar')
def listar():
    contadorEstratos = contador_estratos()
    listar = lista()
    totalNotas = soma_nota()
    return render_template("resultados_por_docente.html", listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)

@app.route('/corrige_notas', methods=['POST','GET'])
def corrige_notas():
    titulosRepetidos = titulos_qualis()
    
    for tits in titulosRepetidos:
        for t in tits:
            rep = titulo_repetido(t)
            if rep == 0:
                continue
            else:
                for r in rep:
                    estrato = r[2]
                    nota_temp = busca_pontuacao_estrato(estrato)
                    nota = float(nota_temp[0])
                    update_notas(nota,r[0])
            reps = qualis_repetidos(titulo=t)
            for r in reps:
                print(r)
                if r[0] == t:
                    media = float(r[1]) / float(r[3])
                    update_qualis_repetido(titulo=r[0],valor=str(media))
                    # showinfo(title="VALIDADO",message="Corrigido com Sucesso!")
                    break
    return redirect('/configuracoes')

@app.route('/contadores',methods=["POST","GET"])
def contadores():
    if request.method == 'POST':
        busca = request.form['query']
        print(busca)
        cont = contador(busca)
        print("all list")
        # os.remove('arq.json')
        totalNotas = soma_nota_docente(busca)

    return jsonify({'htmlresponse': render_template('tabela_notas.html',cont=cont, totalNotas=totalNotas)})

@app.route('/producao_intelectual/<docente>',methods=["POST","GET"])
def producao_intelectual(docente):
    listar = lista_docente(docente)
    
    return jsonify({'htmlresponse': render_template('producao_intelectual.html', listar=listar)})

@app.route('/grafico',methods=['POST','GET'])
def gerar_grafico():
    busca = request.form['query']
    
        
    graficos(busca)
    with open('arq.json','r') as file:
        data = json.load(file)


    fig = px.bar(data,x='Ano',y='Quantidade', color='Estratos', barmode='stack')
    

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # print(graphJSON)
    names = []
    values = []
    pizza_por_docente(busca)
    with open ('pizza_docente.json','r') as piz:
        d = json.load(piz)
        names.append(d[0]['Conferencia'].capitalize())
        names.append(d[0]['Periodico'].capitalize())
        values.append(d[0]['PercConferencia'])
        values.append(d[0]['PercPeriodico'])
        
    figs = px.pie(names=names,values=values)
    
    graph = json.dumps(figs, cls=plotly.utils.PlotlyJSONEncoder)
    
    return jsonify({'htmlresponse': render_template('graficos.html',graphJSON=graphJSON,graph=graph)})
  
@app.route("/visualiza_dados/<id>", methods=['POST','GET'])
def visualizaDados(id):
    mostra = mostra_dados_faltantes(id)
    retorna =  {'dados': id}
    return jsonify(mostra=mostra)

@app.route("/visualizar_dados/<titulo>",methods=['POST'])
def visualizarDados(titulo):
    mostra = titulo_repetido(titulo)
    retorna =  {'dados': titulo}
    return jsonify(mostra=mostra)

@app.route("/edita_publicacao/<id>",methods=['POST','GET'])
def edita_publicacao(id):
    mostra = mostra_publicacao(id)
    return render_template('edita_publicacao.html',mostra=mostra)

@app.route("/edita_publicacao_docente/<id>",methods=['POST','GET'])
def edita_publicacao_docente(id):
    mostra = mostra_publicacao(id)
    return render_template('edita_publicacao_docente.html',mostra=mostra)

@app.route('/atualiza',methods=['POST'])
def atualiza():
    if request.method=="POST":
        id = request.form['id']
        # docente = request.form['nome_docente']
        # titulo = request.form['titulo']
        nome_evento = request.form['nome_evento']
        doi = request.form['doi']
        sigla = request.form['sigla']
        estratos = request.form['estratos']
        estratos = estratos.upper()
        
        nota_temp = busca_pontuacao_estrato(estratos)
        nota = nota_temp[0] 

        
        versao = lista_por_id(id)    
        
        atualizar(id, doi, sigla, nome_evento, estratos, nota, versao[11])
        
        flash("Atualizado com Sucesso! ")
    return resultado_total()

@app.route('/atualiza_docente',methods=['POST'])
def atualiza_docente():
    if request.method=="POST":
        id = request.form['id']
        docente = request.form['hidden_nome_docente']
        # titulo = request.form['titulo']
        nome_evento = request.form['nome_evento']
        doi = request.form['doi']
        sigla = request.form['sigla']
        estratos = request.form['estratos']
        estratos = estratos.upper()
        
        nota_temp = busca_pontuacao_estrato(estratos)
        nota = nota_temp[0]
        
        versao = lista_por_id(id)    
        
        atualizar(id, doi, sigla, nome_evento, estratos, nota, versao[11])
        
        flash("Atualizado com Sucesso! ")
    return resultado_docente(docente)

@app.route('/resultado_docente',methods=['POST'])
def resultado_docente(docente):
    return resultado_editado(docente)

def resultado_editado(docente):  
    
    listar = lista()
    #prof = busca_prof()
    totalNotas = soma_nota()
    contadorEstratos = contador_estratos()
    return render_template("resultados_por_docente.html", docente=docente, listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)


@app.route("/deletarDocente/<docente>",methods=['POST'])
def deletarDocente(docente):
    deletar_docente(docente)
    
    return render_template('resultados_por_docente.html')

@app.route("/mostra_grafo", methods=['POST','GET'])
def mostra_grafo():
    if request.method == "POST":
        tipo = request.form['query']
        
        g = grafico_colaboracao()
        grafo = tipo_grafo(tipo,g)
        return tipo
    
@app.route("/wordcloud")
def wordcloud():
    page = "nuvem"
    return render_template("loading.html",page=page)

@app.route("/nuvem")
def nuvem():
    nuvem_de_palavras()
    prof = busca_prof()
    return render_template('nuvem.html',prof=prof)

@app.route("/nuvem_docente", methods=['POST','GET'])
def nuvem_docente():
    docente = request.form['query']
    nuvem_por_docente(docente)
    return render_template('nuvem.html')

@app.route("/configuracoes")
def configuracoes():
    valor = lista_pontuacoes()
    return render_template('notas.html',valor=valor)

@app.route("/tabela_qualis",methods=['POST'])
def tabela_qualis():
    nota = request.form.getlist('nota')
    estrato = request.form.getlist('estrato')
    notas = []
    for n in nota:
        
        notas.append(float(n.replace(",",".")))
    
    dados = {}
    dados = zip(estrato,notas)
    print(dados)
    
    for dado in dados:
        update_pontuacoes(dado[0],dado[1])
    return recalcula_notas()

def recalcula_notas():
    titulos = lista()
    
    for t in titulos:
        estratos = t[9]
        nota_temp = busca_pontuacao_estrato(estratos)
        nota = float(nota_temp[0])
        update_notas(nota,t[4])
        # for t in tits:
        #     rep = titulo_repetido(t)
        #     if rep == 0:
        #         continue
        #     else:
        #         for r in rep:
        #             estrato = r[2]
        #             nota_temp = busca_pontuacao_estrato(estrato)
        #             nota = nota_temp[0]
        #             update_notas(nota,r[0])
    flash("Tabela atualizada com sucesso!")
    return configuracoes()

if __name__ == "__main__":
    database.tabela_resultados()
    database.tabela_pontuacoes()
    database.insert_pontuacoes()

    app.run(host='0.0.0.0')
