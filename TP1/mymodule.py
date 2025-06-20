def afficher_hello_world():
    print("Hello World")

# def helloWorld(msg:str)->None:
#     print(f"Hello: {msg}")

# def sum(a, b):
#     return a + b

def sum (x:int, y:int) -> int:
    return x + y

def helloWorld(msg:str)->None:
    print(f"Hello: {msg}")
    #Another way to do it and test if the function is called
    print("hello :\t", msg)
    print(fr"hello :\t {msg}")
    print(r"hello :\t {msg}")

#create a class printer
class Printer: 
    def __init__(self, name:str):
        self.name = name #name of the printer

    def print(self, msg:str):
        print(f"Printer {self.name}: {msg}") #display the message with the name of the printer
    pass