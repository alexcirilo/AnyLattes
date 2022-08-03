from app import db

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
    
    def __init__(self,nome, titulo,ano_inicio, natureza,coordenador,financiamento,integrantes) :
        self.nome = nome
        self.titulo = titulo
        self.ano_inicio = ano_inicio
        self.natureza = natureza
        self.coordenador = coordenador
        self.financiamento = financiamento
        self.integrantes = integrantes
        
db.create_all()