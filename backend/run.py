from homePortal.app import app
import sys

def start():
    debug = True
    host = "0.0.0.0"
    app.run(host, debug = debug)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            start()
    else:
            print("usage:\n\n\t run.py [ start ]")
else:
    print("as")
