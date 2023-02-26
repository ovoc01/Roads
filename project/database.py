import psycopg2

class Connection:
    
    def getPostgreSQL():
        return psycopg2.connect(database="roads",
                        host="localhost",
                        user="tendry",
                        password=" ",
                        port="5432")