import os
import glob
import xml.etree.ElementTree as ET
import xlwt


cont = 0
curriculos = []
for f in glob.glob('curriculos-facomp/*'):    #Lista os arquivos xml do mesmo diretório que o programa
    curriculos.append(f)
    cont = cont+1 
    
curriculos.sort()

anos_validos = [ "2017", "2018", "2019", "2020"]

workbook = xlwt.Workbook()
worksheet = workbook.add_sheet(u'Formacao')  #Cria aba Planilha
worksheet.write(0, 0, u'nome')
worksheet.write(0, 1, u'titulo')
worksheet.write(0, 2, u'ano inicio')
worksheet.write(0, 3, u'natureza')
worksheet.write(0, 4, u'coordenador')
worksheet.write(0, 5, u'financiamento')
worksheet.write(0, 6, u'integrantes')

i = 1
print('\nCurrículos importados: '+str(cont)) #Imprime os currículos que serão importados
for m in range(0, len(curriculos)):
    tree = ET.parse(curriculos[m])
    root = tree.getroot()
    coord = ""
    print()
    for t in root.iter('DADOS-GERAIS'):   
        print("#"+t.attrib['NOME-COMPLETO'])
        coord = t.attrib['NOME-COMPLETO']
    
    integrantes = []
    financiamento = []
    temp = 0    
    for t in root.iter('PARTICIPACAO-EM-PROJETO'): 
        #print(t)
        
        
        entra = False
        
        coordenador = ""
        
        for v in t.iter(): 
            #print(v)
            if v.tag == 'PROJETO-DE-PESQUISA' and not v.attrib['ANO-FIM']:
                print(v.attrib)
                projeto = v.attrib['NOME-DO-PROJETO']
                ano_inicio = v.attrib['ANO-INICIO'] 
                ano_fim = v.attrib['ANO-FIM'] or "Atual"
                natureza = v.attrib['NATUREZA'] 
                entra = True
                
                #print(i, 0, coord)
                print(i, 1, projeto)
                #print(i, 2, ano_inicio)
                #print(i, 3, natureza)
                
                worksheet.write(i, 0, coord)
                worksheet.write(i, 1, projeto)
                worksheet.write(i, 2, ano_inicio)
                worksheet.write(i, 3, natureza)
                temp = i
                i = i+1
                financiamento = []
                coordenador = ""

            if entra and v.tag == 'INTEGRANTES-DO-PROJETO':
                integrantes.append(v.attrib['NOME-COMPLETO'])
                #print(v.attrib['NOME-COMPLETO'],v.attrib['FLAG-RESPONSAVEL'], coordenador)
                if v.attrib['FLAG-RESPONSAVEL'] == "SIM" and coordenador == "":
                    coordenador = v.attrib['NOME-COMPLETO']
                    worksheet.write(temp, 4, coordenador)
                    #print(temp, 4, coordenador)

            if entra and v.tag == 'FINANCIADOR-DO-PROJETO':
                financiamento.append(v.attrib['NOME-INSTITUICAO'])

        #print(entra, temp, 6, ', '.join(set(integrantes)))   
        if entra:
            #print(', '.join(set(integrantes)))
            worksheet.write(temp, 6, ', '.join(set(integrantes)))
        if entra:
            #print(', '.join((set(financiamento))))
            worksheet.write(temp, 5, ', '.join((set(financiamento))))
            
workbook.save('projetos.xls')