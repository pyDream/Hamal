__author__ = 'YANGYQ11'
import MySQLdb

def database_init(grant_user, grant_passwd, dbname='', host='localhost', user='root', passwd=''):
    conn = MySQLdb.connect(host, user, passwd)
    cursor = conn.cursor()

    cursor.execute("create database %s" % dbname)
    cursor.execute("create database %s" % dbname)
    cursor.execute("create database %s" % dbname)
    conn.commit()

    cursor.close()
    conn.close()