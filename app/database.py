import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="granja",
        # port=54667,
        cursorclass=pymysql.cursors.DictCursor,
    )
