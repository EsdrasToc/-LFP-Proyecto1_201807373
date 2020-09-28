import IOFunctions

class Group:
    nombre = ''
    def __init__(self, nombre):
        self.nombre = nombre
        self.data = []

    def setNombre(self, nombre):
        self.nombre = nombre
    
    def addInformation(self, path):
        #self.data.append(IOFunctions.readAON(path))
        for i in IOFunctions.readAON(path):
            print(i)
            self.data.append(i)

#class Token:
 #   tk = ''