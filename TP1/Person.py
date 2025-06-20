class Person :
    def __init__(self, name:str, age:int, address:str="TBD"):
        self.name = name #name of the person
        self.age = age #age of the person
        self.address= address
        self.lectures=[]
    def __str__(self):
        return f"New Person : {self.name} is {self.age} years old and the address is {self.address}" #display the name and age of the person
    def __repr__(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        return f"Person({self.name}, {self.age})" 