import xml.etree.cElementTree as ET

class ModelGenerator():
    database = None

    def __init__(self,db):
        print("Model Generator started")
        self.database = db

    def updateModel(self):
        self.database.clearModel()
        items = self.database.getItems()
        containers = self.database.getContainers()

        #print("Updating Model")
        #print("# items: ",len(items))
        #print("# containers: ",len(containers))
        for item in items:
            for container in containers:
                if ( (item[1] >= container[1]) and (item[3] >= container[3]) and (item[2] <= container[2]) and (item[4] <= container[4]) ):                    
                    #print("item ",item[0], " contenido en ", container[0])
                    found = self.database.getContainment(container[0],item[0])                                    
                    if (found==None):
                        self.database.insertContainment(container[0],item[0])
                    
    def exportPng(self):
        print("Generating PNG")

    def exportXML(self):
        pritn("Exporting XML")