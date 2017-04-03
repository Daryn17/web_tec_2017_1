import psycopg2
import pprint

def dropDB():
    conection = psycopg2.connect("dbname='webScraping' user='postgres' host='localhost' password='123'")
    objQuery = conection.cursor()
    objQuery.execute('DELETE FROM public."bookTable";')
    conection.commit()
    objQuery.close()
    conection.close()

dropDB()