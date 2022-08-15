# RODAR ESSE ARQUIVO APENAS QUANDO O QUALIS MUDAR!!
# OS ARQUIVOS periodicos.txt e conferencias.txt serão atualizados

import xlrd
import os
from flask import redirect

def load_qualis():
    print('\nImportanto periódicos...')

    os.system("pdftotext -raw arquivos/QUALIS_novo.pdf")
    
    os.system("iconv -f iso-8859-1 -t utf-8 arquivos/QUALIS_novo.txt > arquivos/temp_periodicos.txt")

    f = open("arquivos/temp_periodicos.txt", "r")
    texto = f.read()
    texto = texto.replace("\x0c", "\n")
    lista = str(texto).split("\n")
    periodicos = ""
    for indice, l in enumerate(lista):
        issn = l[0:9]
        nome = ""
        nota = ""
        #se está na mesma linha
        if (len(l) > 2 and l != "ISSN TITULO ESTRATO"):
            nome = l[10:len(l)]
            nota = l[len(l)-2:len(l)]
            final = nome[len(nome)-2:len(nome)]
            if (final in ("A1","A2", "A3", "A4", "B1", "B2", "B3", "B4", "NP")):
                nome = l[10:len(l)-3]
            elif (final == " C"):
                nome = l[10:len(l)-2]
                nota = "C"
            elif (final in ("ÁC", "EC")):
                nota = "C"
            else:
                nota = lista[indice+1]
            #periodicos.append([issn, nome, nota])
            periodicos += str(issn)+ "#$" + str(nome) + "#$"+ str(nota)+"$$$"


    print("Fim da importação de periódicos!")

    print("Criando arquivo com as periódicos...")
    annexsentence=open("arquivos/periodicos.txt","a")
    annexsentence.write(periodicos)
    annexsentence.close()
    print("Arquivo com as periódicos criado!")


    os.system("rm arquivos/QUALIS_novo.txt arquivos/temp_periodicos.txt")


    conferencias = []
    texto = ""
    print('Importanto conferências...')
    planilha = xlrd.open_workbook('arquivos/QualisEventosComp.xls')
    lista = planilha.sheet_by_index(1)
    for linha in range(lista.nrows):
        if linha != 0: 
            l = lista.row_values(linha)
            sigla = l[0]
            nome = l[1]
            nota = l[8]
            texto += str(sigla)+ "#$" + str(nome) + "#$"+ str(nota)+"$$$"
    print("Fim da importação de conferências!")


    print("Criando arquivo com as conferencias...")
    annexsentence=open("arquivos/conferencias.txt","a")
    annexsentence.write(texto)
    annexsentence.close()
    print("Arquivo com as conferencias criado!")
    redirect('qualis.html')

