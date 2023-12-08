# -*- coding: utf-8 -*-
# import mysql.connector
from flask import Flask,jsonify, redirect, render_template, request, flash, url_for, session
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
# from flask_sqlalchemy import SQLAlchemy
from zipfile import ZipFile
from flask_session import Session
from datetime import timedelta


app = Flask(__name__)
app.app_context().push()
app.permanent_session_lifetime = timedelta(seconds=90)



# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml', 'XML','pdf','xls','xlsx','zip','ZIP'}  # extensões validas

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

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    
logado = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template('telas_erros/404.html')

@app.route("/")
def index():
    username = None
    if 'login' in session:
        username = session['login']
    return render_template('login.html',username=username)
    # global logado
    
    # if logado == True:
    #     username = None
    #     if 'login' in session:
    #         username = session['login']
    #         print(username)
    #         return render_template('index.html', username=username)
    #     else:
    #         print(username)
    #         return render_template('login.html')
        # return redirect(url_for('home'))
    
    
    logado = False
    if logado == False:
        return render_template('login.html')


def validar_login(sessao):
    global logado
    if sessao == False or sessao == None:
        logado = False
        return redirect('/')
         

@app.route("/login", methods=['POST','GET'])
def check_login():
    validar_login(session.permanent)
    
    global logado 
    # if logado == True:
    #     return render_template('index.html')
    
    if logado == False:
        if request.method == 'POST' and request.form['login'] != '':
            login = request.form['login']
            senha = request.form['password']
            usuario_logado = usuario(login,senha)
            
            if usuario_logado != None:
                if login == usuario_logado[2] and senha == usuario_logado[3]:
                    flash("Usuário "+usuario_logado[1]+" Logado")
                    session["name"] = usuario_logado[1]
                    session.permanent = True
                    logado = True
                    return redirect(url_for("home"))
            else:
                logado = False
                flash('Usuário ou senha incorreta.')
                return redirect("/")
        else:
            return render_template('login.html')
    flash('Erro no redirecionamento da página')
    return redirect("/")


@app.route("/logout")
def logout():
    validar_login(session.permanent)
    global logado
    logado = False
    session.permanent = False
    flash("Logout efetuado com sucesso!")
    return redirect(url_for("index"))

# @app.route("/signup")
# def signup():
#     global logado 
#     if logado == False:
#         return render_template("signup.html")
#     else:
#         return redirect(url_for('login'))

# @app.route("/novo_usuario", methods=['POST','GET'])
# def novo_usuario():
#     if request.method == 'POST':
#         nome = request.form['nome']
#         login = request.form['login']
#         senha = request.form['senha']
        
#         if nome == None or login == None or senha == None:
#             flash("Os campos não podem ser enviados vazios. ")
#             return redirect('/signup')
            
#         else:
#             result = valida_usuario(nome, login)
#             if result == 0:
#                 salvar_usuario(nome,login,senha)
#                 flash("Usuário "+nome+ " foi salvo com sucesso!")
#                 return redirect(url_for("login"))
#             else:
#                 flash("Usuario "+nome+" encontra-se cadastrado, tente recuperar a senha")
#                 return redirect("/")

#     flash('Erro no redirecionamento da página') 
#     return redirect("/")

# @app.route("/esqueci_senha")
# def tela_esqueci_senha():
#     return render_template('esqueci_senha.html')
    

# @app.route("/esqueci_senha_", methods=['POST'])
# def esqueci_senha():
#     if request.method == 'POST':
#         nome = request.form['nome']
#         login = request.form['login']
#         senha = request.form['senha']
        
#         if nome == None or login == None or senha == None:
#             flash("Os campos não podem ser enviados vazios. ")
#             return redirect('/esqueci_senha')
#         else:
#             result = valida_usuario(nome, login)
            
#             if result != 0:
#                 atualiza_usuario(nome,login,senha)
#                 flash("Usuario "+nome+" atualizado com sucesso!")
#                 return redirect("/")
#             else:
#                 flash("Usuário não encontrado! Cadastre novo usuário para acessar o sistema.")
#                 return redirect("/")
#     flash('Erro no redirecionamento da página')
#     return redirect("/")
            
    
        
@app.route("/home")
def home():
    global logado
    if session.permanent == True:    
        if logado == True:
            return render_template('index.html')
        if logado == False or logado == None:
            return redirect('/')
    return redirect("/")


@app.route("/imports", methods=['GET','POST']) #upload arquivos qualis
def imports():
    validar_login(session.permanent)
    global logado
    # if session.permanent == True:
    if logado == True:
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
    if logado == False:
        return redirect('/')


@app.route("/upload", methods=['GET', 'POST']) #upload currículos
def upload():
    validar_login(session.permanent)
    global logado
    if logado == True:
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
                        f = file.filename.rsplit('.',1)[1].lower()
                        dir = 'curriculos/'
                        if f == 'xml' or f == 'XML':
                            file.save(os.path.join(
                            app.config['UPLOAD_FOLDER'], filename))
                            flash('File(s) uploaded successfully')
                        elif f == 'zip' or f == 'ZIP':
                            nomeArquivoZip = file.filename.replace('.zip','')
                            print(nomeArquivoZip)
                            
                            with ZipFile(file,'r') as z:
                                z.extractall()
                                
                                os.rename('curriculo.xml',dir + nomeArquivoZip+'.xml')
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
    if logado == False:
        return redirect('/')


@app.route('/resultado_total')
def resultado_total():
    validar_login(session.permanent)
    global logado
    if logado == True:
    
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
    if logado == False:
        return redirect('/')


@app.route("/projetos/inicio=<inicio>&fim=<fim>", methods=['POST'])
def projetos(inicio,fim):
    validar_login(session.permanent)
    global logado
    if logado == True:
        if request.method == 'POST':
            anos = []
            result = []
            ano_inicio = inicio
            ano_fim = fim
            
            for r in range(int(ano_inicio),int((ano_fim))+1):
                anos.append(r)
                r+1

        return import_project(anos)
    if logado == False:
        return redirect('/')

@app.route("/tabela_periodicos_e_qualis")
def gerar_tabela_qualis():
    validar_login(session.permanent)
    global logado
    if logado == True:
        return render_template('qualis.html'), load_qualis()
    if logado == False:
        return redirect('/')


@app.route('/resultado_por_docente')
def resultado_por_docente():  
    validar_login(session.permanent)
    global logado
    if logado == True:
        listar = lista()
        #prof = busca_prof()
        totalNotas = soma_nota()
        contadorEstratos = contador_estratos()
        return render_template("resultados_por_docente.html", listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)
    if logado == False:
        return redirect('/')

@app.route('/listar')
def listar():
    validar_login(session.permanent)
    global logado
    if logado == True:
        contadorEstratos = contador_estratos()
        listar = lista()
        totalNotas = soma_nota()
        return render_template("resultados_por_docente.html", listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)
    if logado == False:
        return redirect('/')

@app.route('/corrige_notas', methods=['POST','GET'])
def corrige_notas():
    validar_login(session.permanent)
    global logado
    if logado == True:
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
    if logado == False:
        return redirect('/')

@app.route('/contadores',methods=["POST","GET"])
def contadores():
    validar_login(session.permanent)
    global logado
    if logado == True:
        if request.method == 'POST':
            busca = request.form['query']
            print(busca)
            cont = contador(busca)
            print("all list")
            # os.remove('arq.json')
            totalNotas = soma_nota_docente(busca)

        return jsonify({'htmlresponse': render_template('tabela_notas.html',cont=cont, totalNotas=totalNotas)})
    if logado == False:
        return redirect('/')

@app.route('/producao_intelectual/<docente>',methods=["POST","GET"])
def producao_intelectual(docente):
    validar_login(session.permanent)
    global logado
    if logado == True:
        listar = lista_docente(docente)
        
        return jsonify({'htmlresponse': render_template('producao_intelectual.html', listar=listar)})
    if logado == False:
        return redirect('/')

@app.route('/grafico',methods=['POST','GET'])
def gerar_grafico():
    validar_login(session.permanent)
    global logado
    if logado == True:
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
    if logado == False:
        return redirect('/')
  
@app.route("/visualiza_dados/<id>", methods=['POST','GET'])
def visualizaDados(id):
    validar_login(session.permanent)
    global logado
    if logado == True:
        mostra = mostra_dados_faltantes(id)
        retorna =  {'dados': id}
        return jsonify(mostra=mostra)
    if logado == False:
        return redirect('/')

@app.route("/visualizar_dados/<titulo>",methods=['POST'])
def visualizarDados(titulo):
    validar_login(session.permanent)
    global logado
    if logado == True:
        mostra = titulo_repetido(titulo)
        retorna =  {'dados': titulo}
        return jsonify(mostra=mostra)
    if logado == False:
        return redirect('/')

@app.route("/edita_publicacao/<id>",methods=['POST','GET'])
def edita_publicacao(id):
    validar_login(session.permanent)
    global logado
    if logado == True:
        mostra = mostra_publicacao(id)
        return render_template('edita_publicacao.html',mostra=mostra)
    if logado == False:
        return redirect('/')

@app.route("/edita_publicacao_docente/<id>",methods=['POST','GET'])
def edita_publicacao_docente(id):
    validar_login(session.permanent)
    global logado
    if logado == True:
        mostra = mostra_publicacao(id)
        return render_template('edita_publicacao_docente.html',mostra=mostra)
    if logado == False:
        return redirect('/')

@app.route('/atualiza',methods=['POST'])
def atualiza():
    validar_login(session.permanent)
    global logado
    if logado == True:
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
    if logado == False:
        return redirect('/')

@app.route('/atualiza_docente',methods=['POST'])
def atualiza_docente():
    validar_login(session.permanent)
    global logado
    if logado == True:
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
    if logado == False:
        return redirect('/')

@app.route('/resultado_docente',methods=['POST'])
def resultado_docente(docente):
    validar_login(session.permanent)
    global logado
    if logado == True:
        return resultado_editado(docente)
    if logado == False:
        return redirect('/')

def resultado_editado(docente):  
    validar_login(session.permanent)
    global logado
    if logado == True:
        listar = lista()
        #prof = busca_prof()
        totalNotas = soma_nota()
        contadorEstratos = contador_estratos()
        return render_template("resultados_por_docente.html", docente=docente, listar = listar, totalNotas = totalNotas, contadorEstratos = contadorEstratos)
    if logado == False:
        return redirect('/')


@app.route("/deletarDocente/<docente>",methods=['POST'])
def deletarDocente(docente):
    validar_login(session.permanent)
    global logado
    if logado == True:
        deletar_docente(docente)
        
        return render_template('resultados_por_docente.html')
    if logado == False:
        return redirect('/')

@app.route("/mostra_grafo", methods=['POST','GET'])
def mostra_grafo():
    validar_login(session.permanent)
    global logado
    if logado == True:
        if request.method == "POST":
            tipo = request.form['query']
            
            g = grafico_colaboracao()
            grafo = tipo_grafo(tipo,g)
            return tipo
    if logado == False:
        return redirect('/')
    
@app.route("/wordcloud")
def wordcloud():
    validar_login(session.permanent)
    global logado
    if logado == True:
        page = "nuvem"
        return render_template("loading.html",page=page)
    if logado == False:
        return redirect('/')

@app.route("/nuvem")
def nuvem():
    validar_login(session.permanent)
    global logado
    if logado == True:
        nuvem_de_palavras()
        prof = busca_prof()
        return render_template('nuvem.html',prof=prof)
    if logado == False:
        return redirect('/')

@app.route("/nuvem_docente", methods=['POST','GET'])
def nuvem_docente():
    validar_login(session.permanent)
    global logado
    if logado == True:
        docente = request.form['query']
        nuvem_por_docente(docente)
        return render_template('nuvem.html')
    if logado == False:
        return redirect('/')

@app.route("/configuracoes")
def configuracoes():
    validar_login(session.permanent)
    global logado
    if logado == True:
        valor = lista_pontuacoes()
        return render_template('notas.html',valor=valor)
    if logado == False:
        return redirect('/')

@app.route("/tabela_qualis",methods=['POST','GET'])
def tabela_qualis():
    validar_login(session.permanent)
    global logado
    if logado == True:
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
    if logado == False:
        return redirect('/')

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
    database.tabela_usuarios()
    database.insert_usuario()

    app.run(host='0.0.0.0', debug=True)
