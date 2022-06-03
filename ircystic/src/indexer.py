import logging
import glob
import os
import configparser
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
# configFileGLI = os.getcwd() + '\ircystic\src\config\GLI.cfg'
# configGLI = configparser.ConfigParser()
# configGLI.read(configFileGLI)
#
# gliFile = os.getcwd() + configGLI.get('DEFAULT', 'WRITE')

configFile = os.getcwd() + '\ircystic\src\config\INDEX.cfg'
config = configparser.ConfigParser()
config.read(configFile)

def run(params={}):

    #logging.info("\nInitiating indexer\n")


    #logging.info("\nEnding indexer\n")
    return


if __name__ == "__main__":
    run()
