import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
import wordcloud
from models.consulta import *
import os

def nuvem_geral():
    texto = []
    res = lista()

    nltk.download('stopwords')

    researchers_words = ' '
    pt_words = list(nltk.corpus.stopwords.words('portuguese'))
    en_words = list(wordcloud.STOPWORDS)
    stop = pt_words + en_words


    stop.append('based')
    stop.append('using')
    stop.append('use')
    stop.append('study')
    stop.append('baseado')
    stop.append('usando')
    stop.append('dizem')
    stop.append('estudo')

    for r in res:
        texto.append(r[4])

    # print(texto)
    
    if type(texto) == list:
        for text in texto:
            if text != None:
                researchers_words = researchers_words + text + ' '
        wc = WordCloud(width = 3000, height = 2000,stopwords=stop, min_word_length=2,random_state=1,collocations=False).generate(researchers_words)

    # Remove the axis and display the data as image
    plt.figure(1,figsize=(20,15),dpi=100)
    plt.axis("off")
    plt.imshow(wc, interpolation = "bilinear")  
    wc.to_file('static/images/nuvem_de_palavras.png')
    plt.clf()
    plt.cla()
    #plt.savefig('static/images/nuvem_de_palavras.png',transparent= True)

def nuvem_especifica(docente):
    dir = 'static/images/nuvem_docente'
    
    if os.path.isdir(dir):
        for f in os.listdir(dir):
            os.remove(os.path.join(dir,f))  
    
        os.rmdir('static/images/nuvem_docente')
    
    texto = []
    res = lista_especifica(docente)

    # nltk.download('stopwords')

    researchers_words = ' '
    pt_words = list(nltk.corpus.stopwords.words('portuguese'))
    en_words = list(wordcloud.STOPWORDS)
    stop = pt_words + en_words


    stop.append('based')
    stop.append('using')
    stop.append('use')
    stop.append('study')
    stop.append('baseado')
    stop.append('usando')
    stop.append('dizem')
    stop.append('estudo')
    stop.append('utilizando')

    for r in res:
        texto.append(r[1])

    # print(texto)
    
    if type(texto) == list:
        for text in texto:
            if text != None:
                researchers_words = researchers_words + text + ' '
        wc = WordCloud(width = 2000, height = 1500,stopwords=stop, min_word_length=2,random_state=1,collocations=False).generate(researchers_words)

    # Remove the axis and display the data as image
    plt.figure(1,figsize=(20,15),dpi=100)
    plt.axis("off")
    plt.imshow(wc, interpolation = "bilinear")  
    os.mkdir('static/images/nuvem_docente')
    wc.to_file('static/images/nuvem_docente/'+docente+'.png')
    plt.clf()
    plt.cla()
    # plt.savefig('static/images/nuvem_docente/'+docente+'.png',transparent= True)