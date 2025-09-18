import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        # mysql://root:MeUqMeSQfSRgleonPpcZOPCtHUyTGfiR@mainline.proxy.rlwy.net:30108/railway
        host="mainline.proxy.rlwy.net",
        user="root",
        password="MeUqMeSQfSRgleonPpcZOPCtHUyTGfiR",
        database="railway",
        port=30108,
        cursorclass=pymysql.cursors.DictCursor,
    )

