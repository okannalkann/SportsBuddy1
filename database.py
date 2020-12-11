import mysql.connector


class Database:
    
    def __init__(self, host, port, user, passwd, db):
        self.con = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=db
            )
        self.cursor=self.con.cursor()


    def get_table(self,table):
        query = "SELECT * FROM mydb."+str(table)
        self.cursor.execute(query)
        myresult = self.cursor.fetchall()
        return myresult

    def add_to_table(self,table,name,photo):
        query = "INSERT INTO mydb."+str(table)+" (sport_name, sport_photo) VALUES (%s, %s)"
        val = (name,photo)
        self.cursor.execute(query, val)
        self.con.commit()
        print(self.cursor.rowcount, "record inserted.")

    def delete_to_table(self,table,sport_name):
        query = "DELETE FROM mydb."+str(table)+" WHERE sport_name = '"+sport_name+"'"
        self.cursor.execute(query)
        self.con.commit()
        print(self.cursor.rowcount, "record deleted.")
