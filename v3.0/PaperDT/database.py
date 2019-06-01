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
            print("Database connection established")
            self.clean()
        except Exception as e:
            print(e)


    def getItems(self):
        sql = "SELECT id,x1,x2,y1,y2 FROM items"
        self.db.execute(sql)
        result = self.db.fetchall()
        return result

    def getContainers(self):
        sql = "SELECT id,x1,x2,y1,y2 FROM containers"
        self.db.execute(sql)
        result = self.db.fetchall()
        return result

    def clean(self): 
        sql = "DELETE FROM items"
        self.db.execute(sql)
        self.conn.commit()

        sql = "DELETE FROM containers"
        self.db.execute(sql)
        self.conn.commit()

        sql = "DELETE FROM model"
        self.db.execute(sql)
        self.conn.commit()
    
    def clearModel(self):
        sql = "DELETE FROM model"
        self.db.execute(sql)
        self.conn.commit()

    def removeExtras(self,n):
        sql = "DELETE FROM items where id > %s"
        val = (n,)
        self.db.execute(sql,val)
        self.conn.commit()

    def removeExtrasContainers(self,n):
        sql = "DELETE FROM containers where id > %s"
        val = (n,)
        self.db.execute(sql,val)
        self.conn.commit()

    def getItem(self,id):
        sql = "SELECT * FROM items where id = %s"
        val = (id,)
        self.db.execute(sql, val)
        result = self.db.fetchone()
        return result

    def getContainer(self,id):
        sql = "SELECT * FROM containers where id = %s"
        val = (id,)
        self.db.execute(sql, val)
        result = self.db.fetchone()
        return result

    def insertContainer(self,id,x1,x2,y1,y2,type):
        sql = "INSERT INTO containers (id, x1,x2,y1,y2,type) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (int(id),int(x1),int(x2),int(y1),int(y2),str(type))
        self.db.execute(sql, val)
        self.conn.commit()
        print("INSERTADO")

    def insertItem(self,id,x1,x2,y1,y2,center,text,type):
        sql = "INSERT INTO items (id, x1,x2,y1,y2,center,text,type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (int(id),int(x1),int(x2),int(y1),int(y2),str(center),str(text),str(type))
        self.db.execute(sql, val)
        self.conn.commit()
        print("INSERTADO")

    def updateItem(self,id,x1,x2,y1,y2,center,text,type):
        sql = "UPDATE items set x1 = %s, x2 = %s, y1 = %s, y2= %s, center = %s, text = %s, type = %s where id = %s"
        val = (int(x1),int(x2),int(y1),int(y2),str(center),str(text),str(type),int(id))
        self.db.execute(sql, val)
        self.conn.commit()
        print("ACTUALIZADO")
    
    def updateContainer(self,id,x1,x2,y1,y2,type):
        sql = "UPDATE containers set x1 = %s, x2 = %s, y1 = %s, y2= %s, type = %s where id = %s"
        val = (int(x1),int(x2),int(y1),int(y2),str(type),int(id))
        self.db.execute(sql, val)
        self.conn.commit()
        print("ACTUALIZADO")

    def updateText(self,id,text):
        sql = "UPDATE items set text = %s where id = '%s'"
        val = (str(text),int(id))
        self.db.execute(sql, val)
        self.conn.commit()
        print("TEXTO ACTUALIZADO")

    def updateType(self,id,text):
        sql = "UPDATE items set type = %s where id = '%s'"
        val = (str(text),int(id))
        self.db.execute(sql, val)
        self.conn.commit()
        print("TIPO ACTUALIZADO")

    def updateModel(self):
        print("Actualizando el modelo")

    def getContainment(self,container,item):
        sql = "SELECT * FROM model where container_id = %s and item_id = %s"
        val = (container,item)
        self.db.execute(sql, val)
        result = self.db.fetchone()
        print(item,container,result)
        return result

    def insertContainment(self,container,item):
        sql = "INSERT INTO model (container_id,item_id) VALUES (%s, %s)"
        val = (int(container),int(item))
        self.db.execute(sql, val)
        self.conn.commit()
        print("INSERTADO")




