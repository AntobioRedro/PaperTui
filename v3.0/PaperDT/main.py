import tracker as t
import recognizer as r

def main():
    obt = t.ObjectTracker()
    obt.start(1)
    obt.trackContainers()

if __name__== "__main__":
  main()