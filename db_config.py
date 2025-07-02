# db_config.py

import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Sarvesh123!",
        database="ruby"
    )