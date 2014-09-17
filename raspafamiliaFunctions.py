# -*- coding: utf-8
# @mtrpires
# Raspador de dados do Bolsa Família no Portal da Transparência do governo federal brasileiro
# http://www.portaltransparencia.gov.br
#

import urllib
import urlparse
import re
import csv
import os

from bs4 import BeautifulSoup
from random import uniform
from time import sleep

def getEstado(siglaEstado):
    '''
    Função para recuperar nome, número e código do estado.
    siglaEstado: string (exemplo: 'AC', 'MG', 'RJ')
    
    retorna: lista com informações sobre estado.
    '''
    valorEstado = {
        'AC': ['ACRE', 1, 8127412000], 
        'AL': ['ALAGOAS', 2, 33806137200],
        'AP': ['AMAPÁ', 4, 4768085200], 
        'AM': ['AMAZONAS', 3, 32231278400],
        'BA': ['BAHIA', 5, 136024686800], 
        'CE': ['CEARÁ', 6, 82439236400],
        'DF': ['DISTRITO FEDERAL', 7, 5840827200], 
        'ES': ['ESPÍRITO SANTO', 8, 13167373200],
        'GO': ['GOIÁS', 9, 23075033600], 
        'MA': ['MARANHÃO', 10, 83715957600],
        'MT': ['MATO GROSSO', 13, 13108917600], 
        'MS': ['MATO GROSSO DO SUL', 12, 10624422400],
        'MG': ['MINAS GERAIS', 11, 81235922400], 
        'PA': ['PARÁ', 14, 72721885400],
        'PB': ['PARAÍBA', 15, 40496233000], 
        'PR': ['PARANÁ', 18, 27456416000],
        'PE': ['PERNAMBUCO', 16, 83930496800], 
        'PI': ['PIAUÍ', 17, 38155014200],
        'RJ': ['RIO DE JANEIRO', 19, 60707060800], 
        'RN': ['RIO GRANDE DO NORTE', 20, 26743066800],
        'RS': ['RIO GRANDE DO SUL', 23, 31262276200], 
        'RO': ['RONDÔNIA', 21, 8221430200],
        'RR': ['RORAIMA', 22, 3902949800], 
        'SC': ['SANTA CATARINA', 24, 9740575400],
        'SP': ['SÃO PAULO', 26, 92322968400], 
        'SE': ['SERGIPE', 25, 19879721000],
        'TO': ['TOCANTINS', 27, 10923766000]
    }
    return valorEstado[siglaEstado]

def setParamsEstados(ano, siglaEstado, pagina=1):
    '''
    Define os parâmetros de busca com base numa silga que acessa 
    informações num dicionário de estados.
    ano: integer
    siglaEstado: string (exemplo, 'AC', 'MG')
    pagina: integer
    
    retorna: string de parâmetros compreensível 
    por navegadores de internet
    '''
    siglaEstado = siglaEstado # exemplo: AC, MG, RR etc
    valorEstado = getEstado(siglaEstado)
    queryParams = {
    		'Exercicio': '%d' % ano,
    		'valorEstado': '%d' % valorEstado[2],
            'codigoEstado': '%d' % valorEstado[1],
            'nomeEstado': '%s' % valorEstado[0],
            'valoracao': '1054629150000',
#            'NomeAcao': 'Transferência de Renda Diretamente às Famílias em Condição de Pobreza e Extrema Pobreza Lei nº 10836 de 2004',
            'paramValor': '19061311479771',
            'codigoFuncao': '08',
            'siglaEstado': siglaEstado,
            'codigoAcao': '8442',
            'Pagina': pagina,
        }
    # urllib.urlencode converte elementos do queryParams em x=y& pairs
    params = urllib.urlencode(queryParams)

    return params

def setParamsMunicipios(ano, nomeMunicipio, municipios, pagina=1):
    '''
    Define os parâmetros de busca com base numa silga que acessa 
    informações num dicionário de estados.
    ano: integer
    siglaEstado: string (exemplo, 'AC', 'MG')
    municipios
    pagina: positive integer (default == 1)
    
    retorna: string de parâmetros compreensível 
    por navegadores de internet
    '''
    params = municipios[nomeMunicipio][1]
    paramsReversed = urlparse.parse_qsl(params)
    paramsDict = dict(paramsReversed)
    queryParams = {
    		'Exercicio': '%d' % ano,
            'siglaEstado': paramsDict['siglaEstado'],
            'nomeEstado': '%s' % paramsDict['nomeEstado'],
    		'valorEstado': '%s' % paramsDict['valorEstado'],
            'codigoEstado': '%s' % paramsDict['codigoEstado'],
            'nomeMunicipio': '%s' % paramsDict['nomeMunicipio'],
            'valorMunicipio': '%s' % paramsDict['valorMunicipio'],
            'codigoMunicipio': '%s' % paramsDict['codigoMunicipio'],
            'valoracao': '1054629150000',
#            'NomeAcao': 'Transferência de Renda Diretamente às Famílias em Condição de Pobreza e Extrema Pobreza Lei n 10836 de 2004',
            'paramValor': '19061311479771',
            'codigoFuncao': '08',
            'codigoAcao': '8442',
            'Pagina': pagina,
        }
    # urllib.urlencode converte elementos do queryParams em x=y& pairs
    params = urllib.urlencode(queryParams)

    return params  

def salvaMunicipios(soup):
    '''
    Salva informações sobre municípios num dicionário.
    soup: objeto BeautifulSoup com os resultados da página
    
    retorna: dicionário com municípios  
    '''
    municipios = {}
    #encontra div com a tabela
    listagem = soup.find('div', id='listagem')
    #salva tabela
    tabela = listagem.find('table')
    #encontra as linhas da tabela
    linhas = tabela.findAll('tr')
    #salva municípios no dicionário, pula cabeçalho
    for i in linhas[1:]:
        try:
            cols = i.findAll('td')
            municipios[cols[0].find('a').getText()] =\
            [cols[1].getText().strip(), cols[0].find('a', href=True)['href']]
        except IndexError:
            print "Ops."
            raise
    
    return municipios

def listaMunicipios(municipios):
    '''
    Gera lista de municípios da página atual. Lista é usada para acessar 
    lista de favorecidos e capturar informações
    municipios: dicionário gerado por salvaMunicipios
    
    retorna: dicionário com lista de municípios
    '''
    return [key for key in municipios]

def salvaMunCSV(siglaEstado, municipios):
    '''
    Salva informações sobre municípios no CSV
    municipios: dicionário gerado por salvaMunicipios()
    
    retorna: dicionário
    '''
    try:
        criaPastaEstado(siglaEstado)
        with open('%s/%s.csv' % (siglaEstado, siglaEstado), 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            for key, value in municipios.items():
                csv_writer.writerow([key.encode('utf-8'), value[0]])
            csv_file.close()
        print "Dados sobre municípios foram acrescentados ao arquivo CSV."
    except:
        print "Não foi possível gravar arquivo CSV."
        raise
    return municipios

def salvaFavorecidos(soupMunicipios):
    '''
    Salva informações sobre favorecidos num dicionário.
    soupMunicipios: objeto BeautifulSoup com os resultados da página
    municipios: dicionário com municípios
    
    retorna: dicionário com favorecidos  
    '''
    favorecidos = {}
    #encontra div com a tabela
    listagem = soupMunicipios.find('div', id='listagem')
    #salva tabela
    tabela = listagem.find('table')
    #encontra as linhas da tabela
    linhas = tabela.findAll('tr')
    #salva municípios no dicionário, pula cabeçalho
    for i in linhas[1:]:
        try:
            cols = i.findAll('td')
            favorecidos[cols[1].getText()] =\
            [cols[0].getText(), cols[2].getText().strip()]
        except IndexError:
            print "Ops."
            raise
    
    return favorecidos

def salvaFavCSV(siglaEstado, cidade, favorecidos):
    '''
    Salva informações sobre favorecidos no CSV
    favorecidos: dicionário gerado por salvafavorecidos()
    siglaEstado: sigla do estado ao qual o município pertence
    cidade: nome do município
    
    retorna: dicionário
    '''
    try:
        with open('%s/%s.csv' % (siglaEstado, cidade), 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            for key, value in favorecidos.items():
                csv_writer.writerow([key.encode('utf-8'), value[0], value[1]])
            csv_file.close()
        print "Dados sobre favorecidos foram acrescentados ao arquivo CSV."
    except:
        print "Não foi possível gravar arquivo CSV dos favorecidos de", cidade
        raise
    return favorecidos

def changePage(params):
    '''
    Muda o parâmetro "Pagina", de modo que seja possível
    fazer a transição de páginas na interface do portal
    da transparência e acessar mais dados.
    params: string, encodada para ser usada por browsers
    
    returns: string, encodada para ser usada por browsers
    '''
    # urlparse does the job of reversing the encoded url
    paramsReversed = urlparse.parse_qsl(params)
    # Then, paramsReversed is converted to a dictionary
    paramsDict = dict(paramsReversed)
    # The 'Pagina' value is converted to an integer
    paramsDict['Pagina'] = int(paramsDict['Pagina'])
    # And incremented by 1
    paramsDict['Pagina'] += 1
    # The new parameters are encoded back to be used
    # by the browser.
    newParams = urllib.urlencode(paramsDict)

    return newParams

def salvaSopa(baseURL, params):
    '''
    Baixa o arquivo HTML com os resultados
    e transforma num objeto BeautifulSoup.
    baseURL: string, endereço de internet
    params: string, encodada com parâmetros de procura
    
    retorna: objeto BeautifulSoup como HTML da página de interesse
    '''
    data = urllib.urlopen(baseURL+params)
    soup = BeautifulSoup(data)
    
    return soup

def numeroPaginas(soup):
    '''
    Encontra o número de páginas.
    soup: objeto BeautifulSoup com o HTML da página
    
    retorna: integer
    '''
    search = soup.find('p', attrs={'class': 'paginaAtual'}).getText()
    results = re.search(r'/(\d+)', search).group(1)
    
    return int(results)

def criaPastaEstado(siglaEstado):
    '''
    Cria pasta para estado, onde ficarão as pastas dos municípios.
    estado: string (ex. 'AC', 'MG' etc)
    
    retorna: string
    '''
    try:
        if not os.path.exists(siglaEstado):
            os.makedirs(siglaEstado)
            print "Diretório do estado", getEstado(siglaEstado)[0], "criado com sucesso!"
        else:
            print "Diretório do estado", getEstado(siglaEstado)[0], "já existe!"
    except:
        print "Erro na função criaPastaEstado."
        raise
