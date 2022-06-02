import logging
import glob
from collections import OrderedDict
import os
import configparser
import toolz.dicttoolz as dictionaryTools
import ircystic.src.shared.sentence_handler as sHandler
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import ircystic.src.shared.porterStemmer as PorterStemmer


# LOG format Configurations
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%d %b %H:%M:%S'
list_of_files = glob.glob('/log/*.log')  # * means all if need specific format
latest_file = max(list_of_files, key=os.path.getctime)
logging.basicConfig(filename=latest_file, level=logging.INFO, format=FORMAT, datefmt=DATEFMT, filemode="a")

# O propósito desse módulo é criar o modelo vetorial, dadas as listas invertidas simples.

"""
1) O indexador será configurado por um arquivo INDEX.CFG
    a. O arquivo conterá apenas uma linha LEIA, que terá o formato
        i. LEIA=<nome de arquivo>
    b. O arquivo conterá apenas uma linha ESCREVA, que terá o formato
        i. ESCREVA=<nome de arquivo>

2) O Indexador deverá implementar um indexador segundo o Modelo Vetorial
    a. O Indexador deverá utilizar o tf/idf padrão
        i. O tf pode ser normalizado como proposto na equação 2.1 do Cap. 2 do Modern Information Retrieval
    b. O indexador deverá permitir a alteração dessa medida de maneira simples
    c. O Indexador deverá possuir uma estrutura de memória deve de alguma forma representar a matriz termo documento
    d. O Indexador deverá classificar toda uma base transformando as palavras apenas da seguinte forma:
        i. Apenas palavras de 2 letras ou mais
        ii. Apenas palavras com apenas letras
        iii. Todas as letras convertidas para os caracteres ASCII de A até Z, ou seja, só letras maiúsculas e nenhum outro símbolo
    e. A base a ser indexada estará na instrução LEIA do arquivo de configuração

3) O sistema deverá salvar toda essa estrutura do Modelo Vetorial para utilização posterior
"""


def run(recordContentDict, params={}):

    logging.info("\nInitiating indexer\n")
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

    use_stemmer = filesPathParam = params['USE_STEMMER'] if 'USE_STEMMER' in params.keys() else config.get('DEFAULT', 'USE_STEMMER')

    all_words = []
    for key, token_list in recordContentDictTokenized.items():
        all_words += token_list

    # catch unique values
    all_words = list(set(all_words))

    index = OrderedDict()
    for word in all_words:
        #print(f"Searching for the word: {word}")
        for key, token_list in recordContentDictTokenized.items():
            if token_list.count(word) != 0:
                if not word in index.keys():
                    index[word] = []
                for i in range(token_list.count(word)):
                    index[word].append(key)


    logging.info("\nEnding indexer\n")
    return (index)


if __name__ == "__main__":
    run()
