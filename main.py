import configparser
import logging
import time
from datetime import datetime
from datetime import timedelta

from src.inverted_list_generator import run as inverted_list_generator
# from src.query_processor import run as run_query_processor
# from src.search import run as run_search

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%d %b %H:%M:%S'
LOG_FILENAME = datetime.now().strftime('./src/log/%H.%M.%S__%d-%m-%Y.log')
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=FORMAT, datefmt=DATEFMT, filemode="a")


# This function is called when this file is run as a python module, i.e.
#   when users run python -m <module_Name>
def run_all_modules(params):
    start_time = time.time()

    inverted_list_generator()
    # run_query_processor()
    # run_search()

    elapsed_time = time.time() - start_time

    m = 'Total elapsed time: '+str(timedelta(seconds=elapsed_time))
    print(m)
    logging.info(m)


if __name__ == "__main__":
    logging.info("Starting processing\n\n")

    configFile = 'init.cfg'
    config = configparser.ConfigParser()
    config.read(configFile)
    #print(config.sections())

    params = dict()
    params["USE_STEMMER"] = config.get('CUSTOMIZED_PARAMS', 'USE_STEMMER')
    params['TOKEN_LENGTH_THRESHOLD'] = config.get('CUSTOMIZED_PARAMS', 'TOKEN_LENGTH_THRESHOLD')
    params['ONLY_LETTERS'] = config.get('CUSTOMIZED_PARAMS', 'ONLY_LETTERS')
    params['IGNORE_STOP_WORDS'] = config.get('CUSTOMIZED_PARAMS', 'IGNORE_STOP_WORDS')

    run_all_modules(params)
