import tracker as t
import ocr as tr
import database as db

def main():
    ot = t.ObjectTracker()
    ot.start(1)
    ot.trackContainers()
    #database = db.Database()
    #database.getItem(0)
    #ocr = tr.TextRecognizer()
    #ocr.getText("temp/0.png")

if __name__== "__main__":
  main()
