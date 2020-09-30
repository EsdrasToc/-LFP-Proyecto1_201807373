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
            self.data.append(i)

class General:
    def __init__(self):
        self.currentGroup = None
        self.groups = []
        self.tokens = []
        self.cicle = True
    
    def setCurrentGroup(self, group):
        self.currentGroup = group

    def setCicle(self, cicle):
        self.cicle = cicle