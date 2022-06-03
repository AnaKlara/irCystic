import logging
import glob
import os
import configparser
from collections import OrderedDict
import csv
import math

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

#https://www.datasciencecentral.com/information-retrieval-document-search-using-vector-space-model-in/
"""

configFile = os.getcwd() + '\ircystic\src\config\INDEX.cfg'
config = configparser.ConfigParser()
config.read(configFile)

# Return the number of times a given term appears in a given document
def _get_raw_term_frequency(term,document_identifier,inverted_index):
    frequency = len([ id for id in inverted_index[term] if id == document_identifier] )
    return(frequency)


def run(params={}):

    logging.info("\nInitiating indexer\n")

    inverted_index_file = os.getcwd() + config.get('PATH', 'READ')

    inverted_index = OrderedDict()

    with open(inverted_index_file, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)
        for row in reader:
            token = row[0].strip()
            document_occurrences = row[1].lstrip('[').rstrip(']').replace("'", "").split(',')
            inverted_index[token] = document_occurrences

    weighting_function = config.get('DEFAULT', 'WEIGHT_FUNCTION')
    if weighting_function != 'tf-idf':
        raise ValueError("Invalid weighting function. Available function is tf-idf")

    words_list = inverted_index.keys()

    documents_list = []
    for key , value in inverted_index.items():
        documents_list += value
    documents_list = list(set(documents_list))

    count_documents = len(documents_list)

    inverse_document_frequencies = OrderedDict()

    for term,hits in inverted_index.items():
        # use set to remove duplicate documents
        doc_count = len(set(hits))
        inverse_document_frequencies[term] = math.log(count_documents/doc_count)


    # finished gathering the pieces, now for the actual matrix
    document_term_matrix = OrderedDict()

    for document_id in documents_list:

        term_weights = list()

        for word in words_list:
            idf = inverse_document_frequencies[word]
            tf = _get_raw_term_frequency(word, document_id, inverted_index)

            tf_idf = round(tf * idf, 3)

            term_weights.append(tf_idf)

        document_term_matrix[document_id] = term_weights

    document_term_dict_file = os.getcwd() + config.get('PATH', 'WRITE')

    with open(document_term_dict_file, "w") as outfile:
        w = csv.writer(outfile, delimiter=";",lineterminator = '\n')

        for key, val in document_term_matrix.items():
            w.writerow([key, val])

    logging.info("\nEnding indexer\n")
    return


if __name__ == "__main__":
    run()
