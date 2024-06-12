import os

BASE_URL = os.environ.get('BASE_URL')
USER = os.environ['POSTGRES_USER']
PASSWORD = os.environ['POSTGRES_PASSWORD']
HOST = os.environ['POSTGRES_HOST']
PORT = os.environ['POSTGRES_PORT']
DB_NAME = os.environ['POSTGRES_DB_NAME']
DB_TYPE = os.environ['DB_TYPE']
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
POOL_RECYCLE = int(os.environ['POOL_RECYCLE'])
DB_POOL_SIZE = int(os.getenv('DB_POOL_SIZE', default='250'))
DB_MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', default='100'))
