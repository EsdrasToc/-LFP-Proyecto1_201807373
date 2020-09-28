import Clases
import re
import automatas
import IOFunctions

currentGroup = None
groups = []
cicle = True
initialInstruction = ''
instruction = []

tokens = []

def setCurrentGroup(group):
    currentGroup = group

#Ejecucion de instrucciondes#
def decision():
    if re.match('(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)', instruction[0]) != None:
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                groups.append(Clases.Group(i))
    elif re.match('(L|l)(O|o)(A|a)(D|d)', instruction[0]) != None:
        set_id = ''
        boolean = False
        
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                if boolean:
                    for j in groups:
                        print(j.nombre)
                        if j.nombre == set_id:
                            j.addInformation(i)
                else:
                    set_id = i
                    boolean = True
    elif re.match('(U|u)(S|s)(E|e)', instruction[0])!= None:
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                for j in groups:
                    if j.nombre == i:
                        return j
                        print(currentGroup)
                        break
    elif re.match('(P|p)(R|r)(I|i)(N|n)(T|t)', instruction[0]) != None:
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                IOFunctions.Color(i)
    elif re.match('(S|s)(E|e)(L|l)(E|e)(C|c)(T|t)', instruction[0])!= None:
        boolean1 = False
        boolean2 = False
        verAtributos = []
        atributos = None #nombre de "columna"
        comparador = None # <, >...
        contenido = None # string, bool, float
        operador = '' #or and
        for i in instruction:
            print(str(type(i)))

            
            if str(i).upper() == "WHERE":
                atributos = []
                comparador = []
                contenido = []
                boolean1 = True
                continue

            if re.match('!|<|>|=', str(i)) != None:
                boolean2 = True
                comparador.append(i)
                continue

            if re.match('((O|o)(R|r))|((A|a)(N|n)(D|d))', str(i)) != None:
                operador = i
                continue

            if str(i) == "*":
                verAtributos = None
                print('entro aca')
                continue

            if automatas.verificacionReservada(i) == False:
                if boolean1 == False:
                    verAtributos.append(i)
                else:
                    if boolean2 == False:
                        atributos.append(i)
                    else:
                        contenido.append(i)
                        boolean2 = False
            
        for i in IOFunctions.Select(verAtributos, atributos, comparador, contenido, operador, currentGroup):
            print(i)

    elif re.match('(R|r)(E|e)(P|p)(O|o)(R|r)(T|t)', instruction[0]) != None:
        pass
    return None

while cicle == True:

    initialInstruction = input('$')
    
    if re.match('(E|e)(X|x)(I|i)(T|t)', initialInstruction):
        cicle = False
        continue

    instruction = automatas.readInstruction(initialInstruction, tokens)

    if decision() != None:
        currentGroup = decision()
        print(currentGroup.nombre)