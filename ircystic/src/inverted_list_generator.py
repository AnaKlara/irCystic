import configparser
import glob
import logging
import os
import xml.etree.ElementTree as ET
from collections import OrderedDict
from os import walk
import csv
import toolz.dicttoolz as dictionaryTools
from nltk.tokenize import word_tokenize


import ircystic.src.shared.sentence_handler as sHandler


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
    f. Se uma palavra aparece mais de uma vez em um documento, o número do documento aparecerá mais de um vez na lista
    g. Exemplo de uma linha
        i. FIBROSIS ; [1,2,2,3,4,5,10,15,21,21,21]
"""
def run(params = {}):
    logging.info('Initiating inverted list generator\n')

    configFile = os.getcwd() + '\ircystic\src\config\GLI.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)

    filesPathParam = params['LEIA'] if 'LEIA' in params.keys() else config.get('DEFAULT', 'READ')
    filesPath = os.getcwd() + filesPathParam
    filenames = next(walk(filesPath), (None, None, []))[2]  # [] if no file

    outputFileParam =  params['ESCREVA'] if 'ESCREVA' in params.keys() else config.get('DEFAULT', 'WRITE')
    outputFileParam = os.getcwd() + outputFileParam

    recordContentDict  = OrderedDict()

    for xmlFile in filenames:
        fullFileName = filesPath + xmlFile
        tree = ET.parse(fullFileName)
        root = tree.getroot()
        #print(len(tree.getroot()))
        for record in root.findall('RECORD'):
            recordNum = record.find("RECORDNUM").text
            recordNum = recordNum.strip()
            try:
                textContent = record.find("ABSTRACT").text
                recordContentDict[recordNum] = textContent
            except:
                try:
                    textContent = record.find("EXTRACT").text
                    recordContentDict[recordNum] = textContent
                except:
                    logging.warning(f"Was not possible to extract any content from this article: {recordNum}")
                    continue

    configFile = os.getcwd() + '\ircystic\src\config\INDEX.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)

    # Remove Line break
    recordContentDict = dictionaryTools.valmap(sHandler.remove_line_break_in_string, recordContentDict)

    # remove punctuation
    recordContentDict = dictionaryTools.valmap(sHandler.remove_punctutaion, recordContentDict)

    two_leters_or_more = params['MIN_WORD_LENGTH'] if 'MIN_WORD_LENGTH' in params.keys() else config.get('DEFAULT', 'MIN_WORD_LENGTH')
    if two_leters_or_more:
        recordContentDict = dictionaryTools.valmap(sHandler.all_words_three_or_more, recordContentDict)

    only_letters = params['ONLY_LETTERS'] if 'ONLY_LETTERS' in params.keys() else config.get('DEFAULT', 'ONLY_LETTERS')
    if only_letters :
        recordContentDict = dictionaryTools.valmap(sHandler.remove_number_in_string, recordContentDict)


    ignore_stop_words = params['IGNORE_STOP_WORDS'] if 'IGNORE_STOP_WORDS' in params.keys() else config.get('DEFAULT', 'IGNORE_STOP_WORDS')
    if ignore_stop_words:
        recordContentDict =  dictionaryTools.valmap(sHandler.remove_stop_word, recordContentDict)


    # Transform words to UPPERCASE
    recordContentDict = dictionaryTools.valmap(sHandler.changing_cases, recordContentDict)

    recordContentDictTokenized = dictionaryTools.valmap(word_tokenize, recordContentDict)

    #print("\n\n\n Example: \n")
    #print(recordContentDictTokenized['01238'])
    #print("\n\n\n\n\n")

    #use_stemmer = filesPathParam = params['USE_STEMMER'] if 'USE_STEMMER' in params.keys() else config.get('DEFAULT', 'USE_STEMMER')
    #if use_stemmer:
        #recordContentDictTokenized

    all_words = []
    for key, token_list in recordContentDictTokenized.items():
        all_words += token_list

    # catch unique values
    all_words = list(set(all_words))

    wordFrequencyDict  = OrderedDict()
    for word in all_words:
        #print(f"Searching for the word: {word}")
        for key, token_list in recordContentDictTokenized.items():
            if token_list.count(word) != 0:
                if not word in wordFrequencyDict .keys():
                    wordFrequencyDict [word] = []
                for i in range(token_list.count(word)):
                    wordFrequencyDict [word].append(key)


    with open(outputFileParam, 'w') as csvfile:
        writer = csv.writer(csvfile,delimiter=';',lineterminator = '\n')
        writer.writerow(['Word','Documents'])
        for item in wordFrequencyDict.items():
            writer.writerow(item)
    logging.info('Ending invert list generator\n')

if __name__ == "__main__":
    run()
