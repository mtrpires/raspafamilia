raspafamilia
============
Raspador de dados do Portal da Transparência dos dados do programa Bolsa Família do governo federal Brasileiro

Introdução
---
O raspafamilia é um simples raspador em Python (2.7) que captura dados dos beneficiários do programa Bolsa Família a partir do Portal da Transparência do governo federal brasileiro. 

Apesar de o portal oferece o download completo da base de dados em um único arquivo CSV, o raspador divide os dados em pastas para cada estado, um arquivo CSV consolidado para cada unidade da federação e um arquivo CSV para cada município, facilitando a analise localizada e distribuição de dados.

O código foi desenvolvido com vistas a executar o básico para a realização do download de dados. Ainda não há muitas opções de flexibilização. A rotina foi feita para ser executada de uma vez (são mais de 30 milhões de beneficiários...) e levará muito tempo para finalizar.

Utilização
---
O arquivo "raspador.py" permite a edição do ano em que se deseja baixar as informações dos beneficiários. Basta executar o script na sua linha de comando e o raspador irá criar pastas com as iniciais dos estados. O resultado final é uma série de diretórios com arquivos CSV consolidados para os dados daquele estado e uma série de outros arquivos CSV com informações dos beneficiários, por nome, separados pelos nomes dos municípios.

Para executar o script, basta digitar na sua linha de comando:

```python
$ python raspador.py
```

Melhorias/To do
---
####Inclusão de cabeçalhos
  Os arquivos CSV gerados pelo raspador não possuem cabeçalhos. É preciso incluir rotina que garanta a inclusão deles.
####Processamento paralelo
  Como são mais de 30 milhões de beneficiários, pode fazer mais sentido fazer a raspagem em paralelo, uma rotina por estado, apesar de que isso pode sobrecarregar o servidor e não ser recomendado.
####Resume
  Se por qualquer motivo o raspador interromper sua execução, não há nenhum recurso que permita a reinicialização a partir de onde foi parado.
####Opções via linha de comando
  A seleção do ano, por exemplo, precisa ser editada diretamente dentro do script. Isso não é desejável.
####Housekeeping
  Existem algumas soluções tortas que precisam ser limpas e readequadas.


Disclaimer
---
Fiz esse raspador em algumas horas, por diversão, aprendizado e para ajudar amigos, sem a qualquer pretenção de fazer um trabalho brilhante. Sei que o melhor a se fazer é baixar a base de dados completa e acessá-la localmente utilizando um servidor SQL. 

Além disso, sou jornalista de formação e aprendi a programar sozinho. Apesar de sempre procurar escrever da forma mais clara e procurar as rotinas menos burocráticas, é certo que você encontrará soluções desengonçadas e grosseiras (como urllib, por exemplo). Toda e qualquer crítica construtiva é bem-vinda.
