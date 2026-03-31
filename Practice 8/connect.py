import psycopg2
from config import params

def get_connection():
    return psycopg2.connect(**params)