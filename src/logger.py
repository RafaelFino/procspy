from datetime import datetime
import logging

# Background Colors to log messages
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    DEBUG = '\033[90m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger:
    def init(log_name: str):        
        logging.basicConfig(filename=log_name, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    def debug(message):
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}[{datetime.now()}] {bcolors.DEBUG}{message}")
        logging.info(message)

    def info(message):
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}[{datetime.now()}] {bcolors.OKCYAN}{message}")
        logging.debug(message)

    def error(message):
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}[{datetime.now()}] {bcolors.FAIL}{message}")
        logging.error(message, exc_info=True)

    def success(message):
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}[{datetime.now()}] {bcolors.OKGREEN}{message}")
        logging.info(message)

    def warning(message):
        print(f"{bcolors.BOLD}{bcolors.OKBLUE}[{datetime.now()}] {bcolors.WARNING}{message}")
        logging.warning(message)