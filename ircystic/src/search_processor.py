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


"""
O objetivo desse módulo é transformar o arquivo de consultas fornecido ao padrão de palavras que estamos
utilizando.

1) O Processador de Consultas deverá ler um arquivo de configuração
    a. O arquivo é criado por vocês
    b. O nome do arquivo é PC.CFG
    c. Ele contém dois tipos de instruções
        i. LEIA=<nome de arquivo>
        ii. CONSULTAS=<nome de arquivo>
        iii. ESPERADOS=<nome de arquivo>
        iv. As instruções são obrigatórias, aparecem uma única vez e nessa ordem.

2) O Processador de Consultas deverá ler um arquivo em formato XML
    a. O arquivo a ser lido será indicado pela instrução LEIA no arquivo de configuração
    i. O formato é descrito pelo arquivo “cfc2-query.dtd”.
    ii. O arquivo a ser lido é “cfquery.xml”.

3) O Processador de Consultas deverá gerar dois arquivos
    a. Os arquivos deverão ser no formato cvs
        i. O caractere de separação será o “;”, ponto e vírgula
            1. Todos os caracteres “;” que aparecerem no arquivo original devem ser eliminados
        ii. A primeira linha do arquivo cvs deve ser o cabeçalho com o nome dos campos
    b. O primeiro arquivo a ser gerado será indicado na instrução CONSULTAS do arquivo de configuração
        i. Cada linha representará uma consulta
            1. O primeiro campo de cada linha conterá o número da consulta
                a. Campo QueryNumber
            2. O segundo campo de cada linha conterá uma consulta processada em letras maiúsculas, sem acento
                a. A partir do campo QueryText
            3. Cada aluno poderá escolher como criar sua consulta
    c. O segundo arquivo a ser gerado será indicado na instrução ESPERADOS
        i. Cada linha representará uma consulta
            1. O primeiro campo de cada linha conterá o número da consulta
                a. Campo QueryNumber
            2. O segundo campo conterá um documento
                a. Campo DocNumber
            3. O terceiro campo conterá o número de votos do documento
                a. Campo DocVotes
            4. Uma consulta poderá aparecer em várias linhas, pois podem possuir vários documentos como resposta
            5. As linhas de uma consulta devem ser consecutivas no arquivo
            6. Essas contas devem ser feitas a partir dos campos Records, Item e do atributo Score de Item
                a. Considerar qualquer coisa diferente de zero como um voto
"""

configFile = os.getcwd() + '\ircystic\src\config\PC.cfg'
config = configparser.ConfigParser()
config.read(configFile)

def run(params={}):
    print("Search processor")

if __name__ == "__main__":
    logging.info("\nBegining search processor module run\n")
    run()
    logging.info("\nEnding search processor module run\n")
