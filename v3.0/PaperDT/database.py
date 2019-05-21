import mysql.connector
 
#seguridad
class Database():
    conn = None
    db = None

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="papertype"
            )
            self.db = self.conn.cursor()
        except Exception as e:
            print(e)
       
    def getItem(self,id):
        sql = "SELECT * FROM items where id = %s"
        val = (id,)
        self.db.execute(sql, val)
        result = self.db.fetchone()
        return result

    def insertItem(self,id,x1,x2,y1,y2,center,text,type):
        sql = "INSERT INTO items (id, x1,x2,y1,y2,center,text,type) VALUES (%s, %s, %s, %s, %s, '%s', '%s', '%s')"
        val = (int(id),int(x1),int(x2),int(y1),int(y2),str(center),str(text),str(type))
        self.db.execute(sql, val)
        self.conn.commit()
        print("INSERTADO")

    def updateItem(self,id,x1,x2,y1,y2,center,text,type):
        sql = "UPDATE items set x1 = %s, x2 = %s, y1 = %s, y2= %s, center = '%s', text = '%s', type = '%s' where id = '%s'"
        val = (int(x1),int(x2),int(y1),int(y2),str(center),str(text),str(type),int(id))
        self.db.execute(sql, val)
        self.conn.commit()
        print("ACTUALIZADO")

    def updateModel():
        print("Actualizando el modelo")





