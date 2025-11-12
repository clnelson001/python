import sys
called_from_main = False

def greet(name="elsewhere"):
    if called_from_main:
        return "Hello from "+sys.argv[0]
    return "Hello from "+name

if __name__ == "__main__":
    called_from_main = True
    print(greet())