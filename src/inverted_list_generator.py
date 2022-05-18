import configparser
import glob
import logging
import os
import xml.etree.ElementTree as ET
from collections import OrderedDict
from os import walk

# LOG format Configurations
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%d %b %H:%M:%S'
list_of_files = glob.glob('/log/*.log') # * means all if need specific format
latest_file = max(list_of_files, key=os.path.getctime)
logging.basicConfig(filename=latest_file, level=logging.INFO, format=FORMAT, datefmt=DATEFMT, filemode="a")


# A função desse módulo é criar as listas invertidas simples.
"""
1) O Gerador Lista Invertida deverá ler um arquivo de configuração
    a. O nome do arquivo é GLI.CFG
    b. Ele contém dois tipos de instruções
        i. LEIA=<nome de arquivo>
        ii. ESCREVA=<nome de arquivo>
        iii. Podem ser uma ou mais instruções LEIA
        iv. Deve haver uma e apenas uma instrução ESCREVA
        v. A instrução ESCREVA aparece depois de todas as instruções LEIA

2) O Gerador Lista Invertida deverá ler um conjunto de arquivos em formato XML
    a. Os arquivos a serem lidos serão indicados pela instrução LEIA no arquivo de configuração
    b. O formato é descrito pelo arquivo cfc2.dtd.
    c. O conjunto de arquivos será definido por um arquivo de configuração
    d. Os arquivos a serem lidos são os fornecidos na coleção

3) Só serão usados os campos RECORDNUM, que contém identificador do texto e ABSTRACT, que contém o texto a ser classificado
    a. Atenção: Se o registro não contiver o campo ABSTRACT deverá ser usado o campo EXTRACT
    
4) O Gerador Lista Invertida deverá gerar um arquivo
    a. O arquivo a ser gerado será indicado na instrução ESCREVA do arquivo de configuração
    b. O arquivo deverá ser no formato cvs
        i. O caractere de separação será o “;”, ponto e vírgula
    c. Cada linha representará uma palavra
    d. O primeiro campo de cada linha conterá a palavra em letras maiúsculas, sem acento
    e. O segundo campo de cada linha apresentará uma lista (Python) de identificadores de documentos onde a palavra aparece
    f. Se uma palavra aparece mais de uma vez em um documento, o número do documento aparecerá o mesmo número de vezes na lista
    g. Exemplo de uma linha
        i. FIBROSIS ; [1,2,2,3,4,5,10,15,21,21,21]
"""
def run(params = {}):
    logging.info('Initiating inverted list generator\n')

    configFile = os.getcwd() + '\src\config\GLI.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    filesPathParam = config.get('PATH', 'LEIA')
    filesPath = os.getcwd() + filesPathParam
    filenames = next(walk(filesPath), (None, None, []))[2]  # [] if no file

    articles = OrderedDict()

    for xmlFile in filenames:
        fullFileName = filesPath + xmlFile
        tree = ET.parse(fullFileName)
        root = tree.getroot()
        #print(len(tree.getroot()))
        for record in root.findall('RECORD'):
            recordNum = record.find("RECORDNUM").text
            try:
                textContent = record.find("ABSTRACT").text
            except:
                try:
                    textContent = record.find("EXTRACT").text
                except:
                    logging.warning(f"Was not possible to extract any content from this article: {recordNum}")
            articles[recordNum] = textContent


    #print(articles)
    logging.info('Ending invert list generator\n')

if __name__ == "__main__":
    run()
