import tracker as t
import ocr as tr

def main():
    #ot = t.ObjectTracker()
    #ot.start(1)
    #ot.trackContainers()
    ocr = tr.TextRecognizer()
    ocr.getText("temp/0.png")

if __name__== "__main__":
  main()
