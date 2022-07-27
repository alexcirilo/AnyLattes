from fileinput import filename
from genericpath import isdir
import os
from flask import Flask, redirect, render_template, request, flash
from werkzeug.utils import secure_filename


# configurações de upload arquivos

ALLOWED_EXTENSIONS = {'xml','XML'} #extensões validas

#verifica se pasta existe
if os.path.isdir('curriculos'):
    UPLOAD_FOLDER = 'curriculos'
else:
    os.mkdir('curriculos')
    UPLOAD_FOLDER = 'curriculos'

app = Flask(__name__)
app.secret_key = 'files' #chave para validar sessão quando ocorre alteração de dados de cookie

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER #atribuição da pasta



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods = ['GET','POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        print (files)
        for file in files:
            if file.filename == '':
                flash("No Selected file(s)")
            else:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    flash('File(s) uploaded successfully')
                else:
                    flash("Não foi possível efetuar upload. Arquivo com extensão inválida")
        return redirect('/')
        
if __name__ == "__main__":
    app.run()