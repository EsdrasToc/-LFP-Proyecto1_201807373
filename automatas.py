import re
import IOFunctions
import Clases

#===============================================================#
#Automata encargado de encontrar los id para crear o usar un set#
#===============================================================#
def Create_Use(instruction):
    id =''
    i = 0
    estado = 0

    while i< len(instruction):
        if estado == 0:
            if re.match('s|S', instruction[i]) != None:
                estado = 1
        elif estado == 1:
            if re.match('e|E', instruction[i]) != None:
                estado = 2
            else:
                break
        elif estado == 2:
            if re.match('T|t', instruction[i]) != None:
                estado = 3
            else:
                break
        elif estado == 3:
            if instruction[i] == " ":
                estado = 4
            else:
                break
        elif estado == 4:
            if re.match('_|[a-z]|[A-Z]', instruction[i]) != None:
                estado = 5
                id = id + instruction[i]
            elif re.match('[0-9]', instruction[i]) != None:
                break
        elif estado == 5:
            if re.match('_|[a-z]|[A-Z]|[0-9]', instruction[i]) != None:
                id = id + instruction[i]
            else:
                estado = 6
                break
        i += 1

    if estado != 5:
        return None
    else:
        return id

#=========================================#
#AUTOMATA CREADO PARA EL COMANDO LOAD INTO#
#=========================================#
def Load(groups, tk_id, instruction):
    estado = 0
    id = []
    listId = ''
    fileId = ''
    i=0

    while i < len(instruction):
        if estado == 0:
            if re.match('(I|i)', instruction[i]) != None:
                estado = 1
        elif estado == 1:
            if re.match('(N|n)', instruction[i]) != None:
                estado = 2
            else:
                break
        elif estado == 2:
            if re.match('(T|t)', instruction[i]) != None:
                estado = 3
            else:
                break
        elif estado == 3:
            if re.match('(O|o)', instruction[i]) != None:
                estado = 4
            else:
                break
        elif estado == 4:
            if instruction[i] == " ":
                estado = 5
            else:
                break
        elif estado == 5:
            if re.match('[A-Z]|[a-z]|_', instruction[i]) != None:
                estado = 6
                listId = listId + instruction[i]
        elif estado == 6:
            if re.match('[A-Z]|[a-z]|_|[0-9]', instruction[i]) != None:
                listId = listId + instruction[i]
            elif instruction[i] == " ":
                estado = 7
            else:
                break
        elif estado == 7:
            if re.match('(F|f)', instruction[i]) != None:
                estado = 8
        elif estado == 8:
            if re.match('(I|i)', instruction[i]) != None:
                estado = 9
            else:
                break
        elif estado == 9:
            if re.match('(L|l)', instruction[i]) != None:
                estado = 10
            else:
                break
        elif estado == 10:
            if re.match('(E|e)', instruction[i]) != None:
                estado = 11
            else:
                break
        elif estado == 11:
            if re.match('(S|s)', instruction[i]) != None:
                estado = 12
            else:
                break
        elif estado == 12:
            if instruction[i] == " ":
                estado = 13
            else:
                break
        elif estado == 13:
            if re.match('[a-z]|[A-Z]', instruction[i]) != None:
                fileId = fileId + instruction[i]
                estado = 14
            else:
                break
        elif estado == 14:
            if (instruction[i] == '.') or (re.match('[a-z]|[A-Z]|[0-9]|_', instruction[i]) != None):
                fileId = fileId+instruction[i]
                if i == len(instruction)-1:
                    id.append(fileId)
            elif instruction[i] == ',':
                estado = 12
                id.append(fileId)
                #fileId = None
                fileId = ''
            else:
                estado = 16
                break
        else:
            break

        i+=1

    if estado == 14:
        #print('==== set: ' + listId)
        for j in id:
            print('==== documentos ' + j)
        
        for i in groups:
            print(i.nombre)
            if i.nombre == listId:
                for j in id:
                    i.addInformation(j)
                    tk_id.append(j)
                break
    else:
        print('ERROR SINTACTICO')
    tk_id.append(listId)

#======================================#
#AUTOMATA CREADO PARA EL COMANDO SELECT#
#======================================#
def Select(groups, instruction, tk_id,tk_palabras,tk_menor,tk_mayor,tk_coma,tk_texto,tk_numero,tk_booleano,tk_igual,tk_negacion, tk_asterisco):
    
    estado = 0
    i = 0 
    identificador = ''
    lstVerAtributos = [] #listado de atributos a mostrar
    lstContenido = [] #listado de condiciones (texto, numeros o booleanos)
    lstAtributos = [] #listado de nombres de atributos para condicion
    lstCondicion = [] #listado de condiciones
    conector = '' #or | and
    contenido ='' # contenido de atributo
    condicion = '' # < | > | <= | >= | != | =

    while i < len(instruction):
        #print(estado)
        if estado == 0 :
            if re.match('_|[a-z]|[A-Z]',instruction[i]) != None:
                identificador = identificador + instruction[i]
                estado = 1
            elif instruction[i] == '*':
                lstVerAtributos = None
                tk_asterisco.append('*')
                estado = 2
        elif estado == 1 :
            if instruction[i] == ',':
                estado = 0 
                tk_coma.append(',')
                lstVerAtributos.append(identificador)
                tk_id.append(identificador)
                identificador = ''
            elif re.match('_|[a-z]|[A-Z]|[0-9]', instruction[i]) != None:
                identificador = identificador + instruction[i]
            elif instruction[i] == " ":
                estado = 2
                lstVerAtributos.append(identificador)
                tk_id.append(identificador)
                identificador = ''
        elif estado == 2 :
            if re.match('w|W', instruction[i]) != None:
                estado = 3 
        elif estado == 3 :
            if re.match('h|H', instruction[i]) != None:
                estado = 4
            else:
                break
        elif estado == 4 :
            if re.match('E|e', instruction[i]) != None:
                estado = 5
            else:
                break
        elif estado == 5 :
            if re.match('R|r', instruction[i]) != None:
                estado = 6
            else:
                break
        elif estado == 6 :
            if re.match('E|e', instruction[i]) != None:
                estado = 7
            else:
                break
        elif estado == 7 :
            if instruction[i] == " ":
                tk_palabras.append('WHERE')
                estado = 8 
            else:
                break
        elif estado == 8 :
            if re.match('_|[a-z]|[A-Z]|[0-9]',instruction[i]) != None:
                estado = 9
                identificador = ''
                identificador = identificador + instruction[i]
        elif estado == 9 :
            if re.match('_|[a-z]|[A-Z]|[0-9]',instruction[i]) != None:
                identificador = identificador + instruction[i]
            elif instruction[i] == " ":
                estado = 10
                tk_id.append(identificador)
                lstAtributos.append(identificador)
        elif estado == 10 :
            if instruction[i] == '=':
                estado = 12
                condicion = '='
                tk_igual.append('=')
            elif re.match('<|>|!', instruction[i]) != None:
                estado = 11
                condicion = instruction[i]
                if instruction[i] == '<':
                    tk_menor.append('<')
                elif instruction[i] == '>':
                    tk_mayor.append('>')
                elif instruction[i] == '!':
                    tk_negacion.append('!')
        elif estado == 11:
            if instruction[i] == "=":
                estado = 12
                condicion = condicion + instruction[i]
            elif instruction[i] == " ":
                estado = 13
                lstCondicion.append(condicion)
        elif estado == 12:            
            if instruction[i] == " ":
                estado = 13
                lstCondicion.append(condicion)
                condicion = ''
        elif estado == 13:
            if instruction[i] == '"':
                estado = 14
            elif re.match('-|/+|[0-9]', instruction[i]) != None:
                estado = 15
                contenido = contenido + instruction[i]
            elif re.match('(T|t)|(F|f)', instruction[i]) != None:
                contenido = contenido + instruction[i]
                estado = 16
        elif estado == 14 :
            if instruction[i] == '"':
                if i == len(instruction)-1:
                    lstContenido.append(contenido)
                    tk_texto.append(contenido)
                    estado = 18
            else:
                contenido = contenido + instruction[i]
        elif estado == 15:
            if re.match('[0-9]', instruction[i]) != None:
                contenido = contenido + instruction[i]
                if i == len(instruction)-1:
                    lstContenido.append(float(condicion))
                    tk_numero.append(float(contenido))
            elif instruction == ".":
                contenido = contenido + instruction[i]
                estado = 17
            elif instruction[i] == " ":
                estado = 19
                lstContenido.append(float(condicion))
                tk_numero.append(float(contenido))
            else:
                break
        elif estado == 16 :
            if re.match('[A-Z]|[a-z]', instruction[i]) != None:
                contenido = contenido + instruction[i]
                if i == len(instruction)-1:
                    lstContenido.append(bool(contenido))
                    tk_booleano.append(bool(contenido))
            elif instruction[i] == " ":
                estado = 19
                lstContenido.append(bool(contenido))
                tk_booleano.append(bool(contenido))
                contenido = ''
            else:
                break
        elif estado == 17:
            if re.match('[0-9]', instruction[i]) != None:
                contenido = contenido + instruction[i]
                if i == len(instruction)-1 :
                    lstContenido.append(float(contenido))
                    tk_numero.append(float(contenido))
            elif instruction[i] == " ":
                estado = 19
                lstContenido.append(float(contenido))
                tk_numero.append(float(contenido))
                contenido = ''
            else:
                break
        elif estado == 18:
            if instruction[i] == " ":
                estado = 19
                lstContenido.append(contenido)
                tk_texto.append(contenido)
                contenido = ''
            else:
                break
        elif estado == 19:
            if re.match('O|o', instruction[i]) != None:
                estado = 20
            elif re.match('A|a', instruction[i]) != None:
                estado = 21
        elif estado == 20:
            if re.match('R|r', instruction[i]) != None:
                estado = 23
                conector = 'OR'
            else:
                break
        elif estado == 21:
            if re.match('N|n', instruction[i]) != None:
                estado = 22
            else:
                break
        elif estado == 22:
            if re.match('D|d', instruction[i]) != None:
                estado = 23
                conector = 'AND'
            else:
                break
        elif estado == 23:
            tk_palabras.append(conector)
            if instruction[i] == " ":
                estado = 8

        i += 1

    print('==================atributos a mostrar')
    if lstVerAtributos != None:
        for j in lstVerAtributos:
            print(j)
    else:
        for j in tk_asterisco:
            print(j)
    print('==================palabras reservadas encontradas')
    for j in tk_palabras:
        print(j)

    print('==================condiciones')
    for j in lstCondicion:
        print(j)
    print('==================atributos')
    for j in lstAtributos:
        print(j)
    print('==================contenido')
    for j in lstContenido:
        print(j)