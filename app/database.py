import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host="hopper.proxy.rlwy.net",
        user="root",
        password="ttjIMaodEIILskmUKpuXVpbCBFiwcJTZ",
        database="railway",
        port=56046,
        cursorclass=pymysql.cursors.DictCursor,
    )
