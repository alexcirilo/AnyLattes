import json
from models.docente import contador

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