# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup


def get_html(url):
    f = urllib2.urlopen(url)
    s = f.read()
    return s


def left_team(p):
    left_t = p.find('strong', {'class': 'left-team'}).getText()
    return left_t


def rigth_team(p):
    rigth_t = p.find('strong', {'class': 'right-team'}).getText()
    return rigth_t


def score_left(p):
    score_l = p.find('span', {'class': 'score playing'}).next_element.next_element.getText()
    return str(score_l)


def score_rigth(p):
    score_r = p.find('span', {
        'class': 'score playing'}).getText().split('\n')[2]
    return str(score_r)


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
     score = score_left(p) + "-" + score_rigth(p)
     cronica = cronicas[contador].a['href']
     partido.append(str(left_team(p).encode('utf-8')))
     partido.append(str(rigth_team(p).encode('utf-8')))
     partido.append(str(score))
     partido.append(str(cronica))


     jornadaresultados.append(partido)
     contador = contador + 1

    return jornadaresultados