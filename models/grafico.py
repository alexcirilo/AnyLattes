import json
from models.docente import contador
from models.consulta import *

def graficos(busca):
    nota = contador(busca)
    employee = []
    content = {}
    for n in nota:
        content = {'Ano': n[0], 'Estratos': n[1], 'Quantidade':n[2]}
        employee.append(content)
        content = {}

    json_object = json.dumps(employee,indent=4)
    with open("arq.json","w") as outfile:
        outfile.write(json_object)
        
def pizza():
    valor = perc()
    employee = []
    content = {}
    
    for n in valor:
        content = {'Total':n[0],'Periodico':n[1],'Conferencia':n[2],'PercConferencia':n[4], 'PercPeriodico':n[3] }
        employee.append(content)
        content = {}
        
    json_object = json.dumps(employee, indent=4)
    with open ("pizza.json", "w") as outfile:
        outfile.write(json_object)
    