import logging
import glob
import os
import configparser

# LOG format Configurations
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATEFMT = '%d %b %H:%M:%S'
list_of_files = glob.glob('/log/*.log')  # * means all if need specific format
latest_file = max(list_of_files, key=os.path.getctime)
logging.basicConfig(filename=latest_file, level=logging.INFO, format=FORMAT, datefmt=DATEFMT, filemode="a")


configFile = os.getcwd() + '\ircystic\src\config\busca.cfg'
config = configparser.ConfigParser()
config.read(configFile)

def run(params={}):
    print("Search")

if __name__ == "__main__":
    logging.info("\nBegining search module run\n")
    run()
    logging.info("\nEnding search module run\n")
