# -*- coding: utf-8
# @mtrpires
# Raspador de dados do Bolsa Família no Portal da Transparência do governo federal brasileiro
# http://www.portaltransparencia.gov.br
#

import os

from raspafamiliaFunctions import getEstado
from raspafamiliaFunctions import setParamsEstados
from raspafamiliaFunctions import salvaMunicipios
from raspafamiliaFunctions import salvaMunCSV
from raspafamiliaFunctions import changePage
from raspafamiliaFunctions import salvaSopa
from raspafamiliaFunctions import numeroPaginas
from raspafamiliaFunctions import criaPastaEstado
from raspafamiliaFunctions import setParamsMunicipios
from raspafamiliaFunctions import salvaMunicipios
from raspafamiliaFunctions import listaMunicipios
from raspafamiliaFunctions import salvaMunCSV
from raspafamiliaFunctions import salvaFavorecidos
from raspafamiliaFunctions import salvaFavCSV
from random import uniform
from time import sleep

urlEstados = 'http://www.portaltransparencia.gov.br/PortalTransparenciaPesquisaAcaoMunicipio.asp?'
urlMunicipios = 'http://www.portaltransparencia.gov.br/PortalTransparenciaPesquisaAcaoFavorecido.asp?'
ano = 2014

estados = [
    'BA', 'DF', 'PR', 'RS', 'TO', 'PA', 'PE', 'RN', 'RO', 
    'RJ', 'AC', 'AM', 'AL', 'CE', 'AP', 'GO', 'ES', 'MG', 
    'PI', 'MA', 'SP', 'MT', 'MS', 'SC', 'SE', 'RR', 'PB'\
]

#estados = ['PA']

for siglaEstado in estados:
    print "Passando pelo estado", siglaEstado
    paramsEstados = setParamsEstados(ano, siglaEstado)
    sopaEstados = salvaSopa(urlEstados, paramsEstados)
    print "Sopa estadual pronta!", type(sopaEstados)
    resultsEstados = numeroPaginas(sopaEstados)
    print "Encontrei", resultsEstados, "páginas de estados. Vamos lá?"

    for estado in range(resultsEstados+1)[1:]:
        print "Estou na página (%s)[%d/%s]" % (siglaEstado, estado, resultsEstados)
        #randomSleep = uniform(1, 3)
        print "Salvando HTML com municípios..."
        municipios = salvaMunicipios(sopaEstados)
        print "HTML salvo!"
        
        salvaMunCSV(siglaEstado, municipios)
        
        print "Gerando lista de municípios para páginapágina (%s)[%d/%s]" % (siglaEstado, estado, resultsEstados)
        listaCidades = listaMunicipios(municipios)
        print "Essa é a lista de municípios:", listaCidades
        
        for cidade in listaCidades:
            print "Passando pela cidade", cidade
            paramsMunicipios = setParamsMunicipios(ano, cidade, municipios)
            sopaMunicipios = salvaSopa(urlMunicipios, paramsMunicipios)
            print "Sopa municipal pronta!", type(sopaMunicipios)
            resultsMunicipios = numeroPaginas(sopaMunicipios)
            print "Encontrei", resultsMunicipios, "páginas para o município %s. Vamos lá?" % cidade.encode('utf-8')

            for municipio in range(resultsMunicipios+1)[1:]:
                print "Estou na página (%s)[%d/%s]" % (cidade.encode('utf-8'), municipio, resultsMunicipios)
                
                favorecidos = salvaFavorecidos(sopaMunicipios)
                salvaFavCSV(siglaEstado, cidade, favorecidos)
                
                paramsMunicipios = changePage(paramsMunicipios)
                sopaMunicipios = salvaSopa(urlMunicipios, paramsMunicipios)

        #print "Aguardando próxima página por", randomSleep, "segundos."
        #sleep(randomSleep)
        paramsEstados = changePage(paramsEstados)
        
        print "Mudando de página estadual..."
        sopaEstados = salvaSopa(urlEstados, paramsEstados)

