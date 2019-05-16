import tracker as t

def main():
    ot = t.ObjectTracker()
    ot.start(1)
    ot.trackContainers()
  
if __name__== "__main__":
  main()
