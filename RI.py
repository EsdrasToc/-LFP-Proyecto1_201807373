import re
import automatas
import Clases
import IOFunctions

#Ejecucion de instrucciondes#
def decision(instruction, general):
    #if re.match('(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)', instruction[0]) != None:
    if instruction[0].upper() == "CREATE":
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                #groups.append(Clases.Group(i))
                general.groups.append(Clases.Group(i))
    #elif re.match('(L|l)(O|o)(A|a)(D|d)', instruction[0]) != None:
    elif instruction[0].upper() == "LOAD":
        set_id = ''
        boolean = False
        
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                if boolean:
                    for j in general.groups:
                        if j.nombre == set_id:
                            j.addInformation(i)
                else:
                    set_id = i
                    boolean = True
    #elif re.match('(U|u)(S|s)(E|e)', instruction[0])!= None:
    elif instruction[0].upper() == "USE":
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                for j in general.groups:
                    if j.nombre == i:
                        general.setCurrentGroup(j)
                        break
    #elif re.match('(P|p)(R|r)(I|i)(N|n)(T|t)', instruction[0]) != None:
    elif instruction[0].upper() == "PRINT":
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                IOFunctions.Color(i)
    #elif re.match('(S|s)(E|e)(L|l)(E|e)(C|c)(T|t)', instruction[0])!= None:
    elif instruction[0].upper() == "SELECT":
        boolean1 = False
        boolean2 = False
        verAtributos = []
        atributos = None #nombre de "columna"
        comparador = None # <, >...
        contenido = None # string, bool, float
        operador = '' #or and
        for i in instruction:

            
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

            #if re.match('((O|o)(R|r))|((A|a)(N|n)(D|d))', str(i)) != None:
            if str(i).upper() == "OR" or str(i).upper() == "AND":
                operador = i
                continue

            if str(i) == "*":
                verAtributos = None
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
            
        for i in IOFunctions.Select(verAtributos, atributos, comparador, contenido, operador, general):
            print(i)

    elif instruction[0].upper() == "LIST":
        auxDict = {}
        for i in general.currentGroup.data:
            auxDict.update(i)
        
        j = 1
        for i in auxDict:
            print(str(j) + ". " + i)
            j += 1
    elif instruction[0].upper() == "SCRIPT":
        boolean = False
        #texto = ''
        #instrucciones = []
        instruccion = ''
        instructionList = []
        
        for i in instruction:
            print(i)
            texto = ''
            instrucciones = None
            instrucciones = []
            if i.upper() != "SCRIPT":
                with open(i, "r") as f:
                    for line in f:
                        texto = texto + line.replace('\n', "")
                    j = 0
                    while j < len(texto):
                        instruccion = instruccion + texto[j]
                        if texto[j] == ";" or j == len(texto)-1:
                            instrucciones.append(instruccion.replace(';', ""))
                            instruccion = ''
                        j += 1
                
                for j in instrucciones:
                    print("$" + j)
                    decision(automatas.readInstruction(j, general.tokens), general)
                    general.tokens.append({'tk_puntoComa' : ';'})
                general.tokens.pop()
                        
    elif instruction[0].upper() == 'EXIT':
        general.setCicle(False)

    elif instruction[0].upper() == 'REPORT':
        if instruction[1].upper() == 'TOKENS':
            IOFunctions.reportTokens(general.tokens)

    elif instruction[0].upper() == "MIN":
        attributes = []
        for i in instruction:
            if i == "*":
                attributes = None
                break
            if i.upper() != "MIN":
                attributes.append(i)
        
        for i in IOFunctions.Min(general.currentGroup.data, attributes):
            print(i)

    elif instruction[0].upper() == "MAX":
        attributes = []
        for i in instruction:
            if i == "*":
                attributes = None
                break
            if i.upper() != "MAX":
                attributes.append(i)
        
        for i in IOFunctions.Max(general.currentGroup.data, attributes):
            print(i)

    elif instruction[0].upper() == "SUM":
        attributes = []
        for i in instruction:
            if i == "*":
                attributes = None
                break
            if i.upper() != "SUM":
                attributes.append(i)
        
        for i in IOFunctions.Sum(general.currentGroup.data, attributes):
            print(i)

    elif instruction[0].upper() == "COUNT":
        attributes = []
        for i in instruction:
            if i == "*":
                attributes = None
                break
            if i.upper() != "COUNT":
                attributes.append(i)
        
        for i in IOFunctions.Count(general.currentGroup.data, attributes):
            print(i)

    else:
        print("Instruccion no valida")