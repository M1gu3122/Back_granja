import pymysql
import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host="bwn3szb1llqmpbpcjwho-mysql.services.clever-cloud.com",
        user="unxbcce7majnekgx",
        password="jgFBRuK72ic2mXEubGk4",
        database="bwn3szb1llqmpbpcjwho",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor,
    )
