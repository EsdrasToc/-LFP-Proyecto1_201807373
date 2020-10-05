import re
import automatas
import Clases
import IOFunctions

#==========================#
#EJECUCION DE INSTRUCCIONES#
#==========================#

def decision(instruction, general):
    if instruction[0].upper() == "CREATE":
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                general.groups.append(Clases.Group(i))
    elif instruction[0].upper() == "LOAD":
        set_id = ''
        boolean = False
        
        try:
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
        except:
            print('OCURRIO UN ERROR')
    elif instruction[0].upper() == "USE":
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                for j in general.groups:
                    if j.nombre == i:
                        general.setCurrentGroup(j)
                        break
    elif instruction[0].upper() == "PRINT":
        for i in instruction:
            if automatas.verificacionReservada(i):
                continue
            else:
                IOFunctions.Color(i)
    elif instruction[0].upper() == "SELECT":
        for i in Select(instruction, general):
            print(i)

    elif instruction[0].upper() == "LIST":
        auxDict = {}
        try:
            for i in general.currentGroup.data:
                auxDict.update(i)
        
            j = 1
            for i in auxDict:
                print(str(j) + ". " + i)
                j += 1
        except:
            print('NO SE HA SELECCIONADO UN SET PARA UTILIZAR')
    elif instruction[0].upper() == "SCRIPT":
        boolean = False
        instruccion = ''
        
        for i in instruction:
            texto = ''
            instrucciones = None
            instrucciones = []
            if i.upper() != "SCRIPT":
                try:
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
                        try:
                            decision(automatas.readInstruction(j, general.tokens), general)
                        except:
                            print('NO SE PUDO EJECUTAR LA INSTRUCCION')
                        general.tokens.append({'tk_puntoComa' : ';'})
                    general.tokens.pop()
                except:
                    print('NO SE HA PODIDO LEER EL SCRIPT --- '+i+' ---')        
    elif instruction[0].upper() == 'EXIT':
        print('#==========================#')
        print('#====== HASTA PRONTO ======#')
        print('#==========================#')
        general.setCicle(False)

    elif instruction[0].upper() == 'REPORT':
        if instruction[1].upper() == 'TOKENS':
            try:
                IOFunctions.reportTokens(general.tokens)
            except:
                print('NO PUDO REPORTAR LOS TOKENS')
        else:
            nombre = ""
            auxiliar_instruction = []
            for i in instruction:
                if str(i).upper() == 'REPORT' or str(i).upper() == 'TO':
                    continue
                else:
                    if nombre == "":
                        nombre = i
                        continue
                    else:
                        auxiliar_instruction.append(i)
            
            if auxiliar_instruction[0].upper() == 'SELECT':
                try:
                    IOFunctions.reportHTMLWSelect(Select(auxiliar_instruction, general), nombre)
                except:
                    print('HA OCURRIDO UN ERROR EN LA CONSULTA')
            else:
                try:
                    IOFunctions.reportHTMLWMMSC(MMSC(auxiliar_instruction, general), nombre)
                except:
                    print('HA OCURRIDO UN ERROR EN LA OPERACION')
    elif instruction[0].upper() == "MIN":
        
        try:
            for i in MMSC(instruction, general):
                print(i)
        except:
            print('OCURRIO UN ERROR EN LA OPERACION')

    elif instruction[0].upper() == "MAX":
        try:
            for i in MMSC(instruction, general):
                print(i)
        except:
            print('OCURRIO UN ERROR EN LA OPERACION')
    elif instruction[0].upper() == "SUM":
        try:
            for i in MMSC(instruction, general):
                print(i)
        except:
            print('OCURRIO UN ERROR EN LA OPERACION')
    elif instruction[0].upper() == "COUNT":
        try:
            for i in MMSC(instruction, general):
                print(i)
        except:
            print('OCURRIO UN ERROR EN LA OPERACION')
    else:
        print("Instruccion no valida")

#========================================================================#
#SE ENCARGA DE SEPARAR LAS PALABRAS CUANDO LA INSTRUCCION ES UNA CONSULTA#
#========================================================================#

def Select(instruction, general):
    boolean1 = False
    boolean2 = False
    regex = False
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

        if str(i).upper() =='REGEX':
            regex = True
            continue

        if regex:
            contenido.append(i)
            break

        if re.match('!|<|>|=', str(i)) != None:
            boolean2 = True
            comparador.append(i)
            continue

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

    if regex:
        return IOFunctions.SelectWREGEX(verAtributos, atributos, contenido, general)
    else:        
        return IOFunctions.Select(verAtributos, atributos, comparador, contenido, operador, general)

#=============================================#
#LEE LA INSTRUCCION PARA MAX, MIN, SUM Y COUNT# 
#=============================================#

def MMSC(instruction, general):
    attributes = []
    for i in instruction:
        if i == "*":
            attributes = None
            break
        if i.upper() != "MIN" and i.upper() != "MAX" and i.upper() != "SUM" and i.upper() != "COUNT":
            attributes.append(i)
    
    if instruction[0].upper() == 'MIN':
        return IOFunctions.Min(general.currentGroup.data, attributes)
    elif instruction[0].upper() == 'MAX':
        return IOFunctions.Max(general.currentGroup.data, attributes)
    elif instruction[0].upper() == 'SUM':
        return IOFunctions.Sum(general.currentGroup.data, attributes)
    elif instruction[0].upper() == 'COUNT':
        return IOFunctions.Count(general.currentGroup.data, attributes)
