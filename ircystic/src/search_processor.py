import logging
import glob
import os
import configparser
import xml.etree.ElementTree as ET
from collections import OrderedDict
import csv

import ircystic.src.shared.sentence_handler as sHandler

"""
This code aims to transform query files (xml) to have the same pattern from Inverted List.
"""


# LOG format Configurations
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%d %b %H:%M:%S'
list_of_files = glob.glob('/log/*.log')  # * means all if need specific format
latest_file = max(list_of_files, key=os.path.getctime)
logging.basicConfig(filename=latest_file, level=logging.INFO, format=FORMAT, datefmt=DATEFMT, filemode="a")


def sentenceHandle(sentence, params):
    configFile = os.getcwd() + '\ircystic\src\config\INDEX.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)

    # Remove Line break
    sentence = sHandler.remove_line_break_in_string(sentence)

    # remove punctuation
    sentence = sHandler.remove_punctutaion(sentence)

    two_leters_or_more = params['MIN_WORD_LENGTH'] if 'MIN_WORD_LENGTH' in params.keys() else config.get('DEFAULT','MIN_WORD_LENGTH')
    if two_leters_or_more:
        sentence = sHandler.all_words_three_or_more(sentence)

    only_letters = params['ONLY_LETTERS'] if 'ONLY_LETTERS' in params.keys() else config.get('DEFAULT', 'ONLY_LETTERS')
    if only_letters:
        sentence = sHandler.remove_number_in_string(sentence)

    ignore_stop_words = params['IGNORE_STOP_WORDS'] if 'IGNORE_STOP_WORDS' in params.keys() else config.get('DEFAULT','IGNORE_STOP_WORDS')
    if ignore_stop_words:
        sentence = sHandler.remove_stop_word(sentence)

    use_stemmer = params['USE_STEMMER'] if 'USE_STEMMER' in params.keys() else config['DEFAULT'].getboolean('USE_STEMMER')
    if use_stemmer:
        sentence = sHandler.stemmer(sentence)
    exit()

    return sentence


def write_csv_files(queriestDict):

    config = configparser.ConfigParser()

    configFile = os.getcwd() + '\ircystic\src\config\PC.cfg'
    config.read(configFile)

    # output files
    processed_queries_file = os.getcwd() + config.get('PATH', 'CONSULTAS')
    expected_results_file = os.getcwd() + config.get('PATH', 'ESPERADOS')
    #raw_queries_file = os.getcwd() + config.get('OutputFiles', 'RAW_QUERIES')
    #tokenized_queries_file = os.getcwd() + config.get('OutputFiles', 'TOKENIZED_QUERIES')

    # writing output
    expected_results_file_only_doc_ids = expected_results_file.replace('.csv', '_only_doc_ids.csv')

    expected_results                   = open(expected_results_file, 'w')
    query_vectors                      = open(processed_queries_file, 'w')
    expected_results_only_doc_ids      = open(expected_results_file_only_doc_ids, 'w')
    #raw_queries = open(os.getcwd() + '/' + raw_queries_file, 'w')
    #tokenized_queries = open(os.getcwd() + '/' + tokenized_queries_file, 'w')

    w_expected_results                 = csv.writer(expected_results,delimiter=";",lineterminator='\n')
    w_query_vectors                    = csv.writer(query_vectors,delimiter=";",lineterminator='\n')
    w_expected_results_only_doc_ids    = csv.writer(expected_results_only_doc_ids,delimiter=";",lineterminator='\n')
    #w_raw_queries                      = csv.writer(raw_queries,delimiter=";")
    #w_tokenized_queries                = csv.writer(tokenized_queries,delimiter=";")

    for key,val in queriestDict.items():
        #w_expected_results_only_doc_ids.writerow([key,map(lambda x: x[0],val['queryResults'])])
        #w_expected_results.writerow([key,val['vector']])
        w_query_vectors.writerow([key,val['queryText']])
        #w_raw_queries.writerow([key,val['raw_text']])
        #w_tokenized_queries.writerow([key,val['tokens']])

    # must close these explicitly because i'm not using the 'with open(...) as outfile' construct
    expected_results.close()
    query_vectors.close()
    expected_results_only_doc_ids.close()
    #raw_queries.close()
    #tokenized_queries.close()

def run(params={}):

    config = configparser.ConfigParser()

    configFile = os.getcwd() + '\ircystic\src\config\PC.cfg'
    config.read(configFile)

    queriesFiles = os.getcwd() + config.get('PATH', 'LEIA')

    tree = ET.parse(queriesFiles)
    root = tree.getroot()

    queriestDict = OrderedDict()

    for query in root.findall('QUERY'):

        queryNumber = query.find("QueryNumber").text.strip()

        try:
            queryText = query.find("QueryText").text.strip()
            queryText = sentenceHandle(queryText, params)
            queryResultsQtd = query.find("Results").text.strip()

            queryResults = OrderedDict()

            for item in query.find("Records").findall('Item'):
                document = item.text.strip()
                score = item.attrib['score'].strip()
                queryResults[score]=document

            queriestDict[queryNumber] = {'queryText':queryText, 'queryResultsQtd':queryResultsQtd, 'queryResults ':queryResults }

        except:
            logging.warning(f"Was not possible to extract content from this query correctly: {queryNumber}")
            continue

    #write_csv_files(queriestDict)
    for item in queriestDict.items():
        print(item)
        exit()


if __name__ == "__main__":
    logging.info("\nBeginning search processor module run\n")
    run()
    logging.info("\nEnding search processor module run\n")
