import tracker as t

def main():
    obt = t.ObjectTracker()
    obt.start(1)
    obt.trackContainers()

if __name__== "__main__":
  main()