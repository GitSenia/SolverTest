import sys

from dotenv import load_dotenv
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='app.log',
    filemode='a',
    encoding='utf-8'
)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
    '%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def log_uncaught_exceptions(exctype, value, traceback):
    logging.critical("Uncaught exception", exc_info=(exctype, value, traceback))
sys.excepthook = log_uncaught_exceptions


load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DATABASE=os.getenv('DBNAME')

USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD_DB')

url_test='https://lms.bsuir.by/mod/quiz/attempt.php?attempt=589701&cmid=324848'
url_login="https://lms.bsuir.by/login/index.php"
mid="324848"  #id курса в данном случае ОМО 324848
id_db="298405"
id_APEC="305095"
id_SAio="321506"