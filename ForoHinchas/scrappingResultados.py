# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup


def get_html(url):
    f = urllib2.urlopen(url)
    s = f.read()
    return s


def get_index(jornada):
    url = "http://www.marca.com/eventos/marcador/futbol/2016_17/primera/jornada_" + jornada + "/"
    html_doc = get_html(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    lista = soup.find('ul', {'class': 'lista-partidos-jornada'})
    partidos = lista.find_all('span', {'class': 'score-data'})
    cronicas = lista.find_all('ul', {'class': 'enlaces-redaccion'})

    jornadaresultados=[]
    contador = 0
    for p in partidos:
     partido=[]
     left_team = p.find('strong', {'class': 'left-team'}).getText()
     rigth_team =  p.find('strong', {'class': 'right-team'}).getText()
     aux = p.find('span', {'class': 'score playing'}).getText().split('\n')[2]
     print aux
     score_left = p.find('span', {'class' : 'score playing'}).next_element.next_element.getText()
     score_rigth = p.find('span', {'class': 'score playing'}).next_element.next_element.next_element.next_element.next_element.getText()
     score = score_left + "-" + score_rigth
     cronica = cronicas[contador].a['href']
     partido.append(left_team.encode('utf-8'))
     partido.append(rigth_team.encode('utf-8'))
     partido.append(score)
     partido.append(cronica)


     jornadaresultados.append(partido)
     contador = contador + 1

    return jornadaresultados

def buscarPorEquipo(equipo,jornada):
    resultados = get_index(jornada)

    for partido in resultados:
        if(partido[0] == equipo):
            return partido
        elif(partido[1] == equipo):
            return partido
        else:
            continue


#
busqueda = buscarPorEquipo('Atlético', '9')
print busqueda
print type(busqueda)













