import IOFunctions
import automatas
#===========================================================================#
#LA CLASE GROUP SE ENCARGA DE ALMACENAR LOS SET, ES DECIR UN GROUP ES UN SET#
#===========================================================================#
class Group:
    nombre = ''
    def __init__(self, nombre):
        self.nombre = nombre
        self.data = []

    def setNombre(self, nombre):
        self.nombre = nombre
    
    def addInformation(self, path):
        try:
            for i in automatas.readAON(path):
                self.data.append(i)
        except:
            print('OCURRIO UN ERROR AL LEER EL ARCHIVO --- '+path+' ---')

#==========================================================================================#
#EN LA CLASE GENERAL SE GUARDAN LOS LISTADOS Y EL SET QUE SE UTILIZARAN PARA CADA OPERACION#
#==========================================================================================#
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

        