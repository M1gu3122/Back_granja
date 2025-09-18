import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
       
        host="mainline.proxy.rlwy.net",
        user="root",
        password="MeUqMeSQfSRgleonPpcZOPCtHUyTGfiR",
        database="railway",
        port=30108,
        cursorclass=pymysql.cursors.DictCursor,
    )


