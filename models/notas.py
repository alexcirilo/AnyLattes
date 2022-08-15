def get_periodicos():
    #preparação
    periodicos_recuperados = open("periodicos.txt","r")
    texto_recuperado = periodicos_recuperados.read()
    lista = texto_recuperado.split("$$$")
    l = []
    for n in lista:
        l.append(n.split("#$"))
    return l

def get_conferencias():
    #preparação
    conferencias_recuperadas = open("conferencias.txt","r")
    texto_recuperado = conferencias_recuperadas.read()
    lista = texto_recuperado.split("$$$")
    l = []
    for n in lista:
        l.append(n.split("#$"))
    return l

def get_nota_conferencia(sigla, nome = "", sigla_anais = "", nome_anais = ""):
    for c in get_conferencias():
        if (c[0] and c[1] and c[2]):
            if (sigla.upper().replace(" ","") == c[0].upper().replace(" ","") or nome.upper().replace(" ","") == c[1].upper().replace(" ","")):
                return c[2]
                break
            if (sigla_anais.upper().replace(" ","") == c[0].upper().replace(" ","") or nome_anais.upper().replace(" ","") == c[1].upper().replace(" ","")):
                return c[2]
                break
            if (nome.upper().replace(" ","") == c[0].upper().replace(" ","") or nome_anais.upper().replace(" ","") == c[0].upper().replace(" ","")):
                return c[2]
                break
    print("Conferência não encontrada no Qualis: ",sigla, "--",  nome, "--", sigla_anais, "--", nome_anais)
    return False

def get_nota_periodico(issn, nome = ""):
    for c in get_periodicos():
        if (c[0] and c[1] and c[2]):
            if (issn == c[0] or nome.upper().replace(" ","") == c[1].upper().replace(" ","")):
                return c[2]
                break
    print("Periódico não encontrado no Qualis: ",issn, nome)
    return False
"""
#testes com conferencias
print("nota do XXX = ", get_nota_conferencia("XXXX"))
print("nota do CVPR = ", get_nota_conferencia("CVPR"))
print("nota do IHC = ", get_nota_conferencia("IHC"))
print("nota do ICM = ", get_nota_conferencia("ICM"))
print("nota do ISIC = ", get_nota_conferencia("-", "International Symposium on Integrated Circuits"))
print("nota do WCGA = ", get_nota_conferencia("-", "WORKSHOP DE COMPUTAÇÃO EM CLOUDS E APLICAÇÕES"))
print("nota do SIMPDA = ", get_nota_conferencia("-", "INTERNATIONAL SYMPOSIUM ON DATA-DRIVEN PROCESS DISCOVERY AND ANALYSIS"))
#testes com periódicos
print("nota do INTERACTIONS (IMPRESSO) = ", get_nota_periodico("-", "INTERACTIONS (IMPRESSO)")) 
print("nota do INTERNATIONAL JOURNAL OF AGRICULTURAL AND ENVIRONMENT", get_nota_periodico("1947-3206"))

"""