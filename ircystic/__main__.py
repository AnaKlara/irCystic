import configparser
import logging
import time
from datetime import datetime
from datetime import timedelta
import os


from ircystic.src.inverted_list_generator import run as inverted_list_generator
from ircystic.src.indexer import run as indexer
from ircystic.src.search_processor import run as query_processor
from ircystic.src.search import run as search


FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%d %b %H:%M:%S'
LOG_FILENAME = os.getcwd() + datetime.now().strftime('\ircystic\src\log\%H.%M.%S__%d-%m-%Y.log')

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=FORMAT, datefmt=DATEFMT, filemode="a")

if __name__ == "__main__":
    logging.info("Starting processing\n\n")

    configFile = os.getcwd() + '\ircystic\init.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)

    params = dict()
    params["USE_STEMMER"] = config.get('CUSTOMIZED_PARAMS', 'USE_STEMMER')
    params['MIN_WORD_LENGTH'] = config.get('CUSTOMIZED_PARAMS', 'MIN_WORD_LENGTH')
    params['ONLY_LETTERS'] = config.get('CUSTOMIZED_PARAMS', 'ONLY_LETTERS')
    params['IGNORE_STOP_WORDS'] = config.get('CUSTOMIZED_PARAMS', 'IGNORE_STOP_WORDS')


    # run modules
    start_time = time.time()

    #inverted_list_generator(params)
    #indexer()
    query_processor()
    search()

    elapsed_time = time.time() - start_time

    m = 'Total elapsed time: ' + str(timedelta(seconds=elapsed_time))
    print(m)
    logging.info(m)
