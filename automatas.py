import re
import IOFunctions
import Clases

#==============#
#CREANDO TOKENS#
#==============#
palabras = ['CREATE','SET','LOAD','INTO','FILES','USE','SELECT','WHERE','LIST','ATTRIBUTES','PRINT',
'IN','MAX','MIN','SUM','COUNT','REPORT','TO','SCRIPT','TOKENS','REGEX', 'AND', 'OR']

#=================================================#
#AUTOMATA ENCARGADO DE LA LECTURA DE ARCHIVOS .AON#
#=================================================#

def readAON(path):
    texto=''
    with open(path, "r") as f:
        for line in f:
            texto = texto + line.replace('\n', "")
    
    estado=0
    indice=0
    switchEspacios = False
    tk_atributo = ""
    tk_num = ""
    tk_string = ""
    tk_bool = ""
    listadoF=[]
    listado={}
    while indice < len(texto):

        if (switchEspacios == False) and (texto[indice] == ' '):
            indice+=1
            continue 

        if estado==0:
            if texto[indice] == '(':
                estado=1
            else:
                break
        elif estado==1:
            if texto[indice] == '<':
                estado = 2
            else:
                break
        elif estado==2:
            tk_atributo=''
            tk_bool = ''
            tk_num = ''
            tk_string = ''
            if texto[indice]=='[':
                estado = 3
            else:
                break
        elif estado==3:
            if texto[indice] == ']':
                break
            if re.match('(.)*', texto[indice])!=None:
                tk_atributo = tk_atributo + texto[indice]
                estado = 4
            else:
                break
        elif estado==4:
            if texto[indice] == ']':
                estado = 5
                
            elif re.match('(.)*', texto[indice])!=None:
                tk_atributo = tk_atributo + texto[indice]
                estado = 4
            else:
                break
        elif estado==5:
            if texto[indice] == '=':
                estado = 6
            else:
                break
        elif estado==6:
            if texto[indice] == '+':
                estado = 7
                tk_num = tk_num + texto[indice]
            elif texto[indice] == '-':
                estado = 8
                tk_num = tk_num + texto[indice]
            elif re.match('[0-9]', texto[indice]):
                estado = 9
                tk_num = tk_num + texto[indice]
            elif texto[indice] == '"':
                estado = 10
                switchEspacios = True
            elif re.match('[a-z]|[A-Z]', texto[indice])!= None:
                estado = 13
                tk_bool = tk_bool + texto[indice]
            else:
                break
        elif estado==7:
            if re.match('[0-9]', texto[indice]):
                estado = 9
                tk_num = tk_num + texto[indice]
            else:
                break
        elif estado==8:
            if re.match('[0-9]', texto[indice]):
                estado = 9
                tk_num = tk_num + texto[indice]
            else:
                break
        elif estado==9:
            if re.match('[0-9]', texto[indice]):
                estado = 9
                tk_num = tk_num + texto[indice]
            elif texto[indice] == '.':
                estado = 9
                tk_num = tk_num + texto[indice]
            elif texto[indice] == ',':
                listado[tk_atributo] = float(tk_num)
                listado.update(listado)
                estado = 2
            elif texto[indice] == '>':
                estado = 14
                listado[tk_atributo] = float(tk_num)
                listado.update(listado)
            else:
                break
        elif estado==10:
            if texto[indice] == '"':
                switchEspacios = False
                estado = 12
            else:
                estado = 11
                tk_string = tk_string + texto[indice]
        elif estado==11:
            if texto[indice] == '"':
                switchEspacios = False
                estado = 12
            else:
                estado = 11
                tk_string = tk_string + texto[indice]
        elif estado==12:
            if texto[indice] == ',':
                estado = 2
                listado[tk_atributo] = tk_string
                listado.update(listado)
            elif texto[indice] == '>':
                estado = 14
                listado[tk_atributo] = tk_string
                listado.update(listado)
            else:
                break
        elif estado==13:
            if re.match('[a-z]|[A-Z]', texto[indice])!=None:
                estado = 13
                tk_bool = tk_bool + texto[indice]
            elif texto[indice] == ',':
                estado = 2
                listado.update(listado)
                if(re.match('(F|f)(A|a)(L|l)(S|s)(E|e)',tk_bool)):
                    listado[tk_atributo] = False
                else:
                    listado[tk_atributo] = True
            elif texto[indice] == '>':
                estado = 14
                if(re.match('(F|f)(A|a)(L|l)(S|s)(E|e)',tk_bool)):
                    listado[tk_atributo] = False
                else:
                    listado[tk_atributo] = True
                listado.update(listado)
            else:
                break
        elif estado==14:
            listadoF.append(listado)
            listado = None
            listado = {}
            if texto[indice] == ')':
                estado = 15
            elif texto[indice] == ',':
                estado = 1
            else:
                break
        elif estado==15:
            if re.match('(.)*', texto[indice]):
                estado = 16

        indice+=1
    
    return listadoF

#===========================================#
#AUTOMATA CREADO PARA LEER LAS INSTRUCCIONES#
#===========================================#

def readInstruction(instruction, tokens):
    estado = 0
    i = 0
    text = ''
    instructionBlocs = []
    
    while i < len(instruction):
        if estado == 0:
            if instruction[i] == '*':
                tokens.append({'tk_asterisco' : '*'})
                instructionBlocs.append('*')
            elif re.match('[a-z]|[A-Z]|_', instruction[i]) != None:
                text = text + instruction[i]
                estado =1
            elif re.match('=|<|>|!', instruction[i]) != None:
                estado = 2
                text = text +instruction[i]
            elif instruction[i] == "[":
                tokens.append({'tk_corcheteApertura' : '['})
                estado = 9
        elif estado == 1:
            if re.match('[a-z]|[A-Z]|_|[0-9]|\.', instruction[i]) != None:
                text = text + instruction[i]
                if i == len(instruction)-1:
                    if verificacionReservada(text):
                        tokens.append({'tk_palabra' : text})
                        instructionBlocs.append(text)
                    else:
                        tokens.append({'tk_identificador' : text})
                        instructionBlocs.append(text)
            elif  instruction[i] == " " or instruction[i] == ",":
                estado = 0
                if verificacionReservada(text):
                    tokens.append({'tk_palabra' : text})
                    instructionBlocs.append(text)
                else:
                    tokens.append({'tk_identificador' : text})
                    instructionBlocs.append(text)
                
                if instruction[i] == ',':
                    tokens.append({'tk_coma' : ','})
                text = ''
        elif estado == 2:
            if re.match('=|<|>|!', instruction[i]) != None:
                text = text + instruction[i]
            elif instruction[i] == " ":
                tokens.append({'tk_operador' : text})
                instructionBlocs.append(text)
                text = ''
                estado = 3
        elif estado == 3:
            if instruction[i] == '"':
                estado = 4
            elif re.match('[a-z]|[A-Z]', instruction[i]) != None:
                estado = 8
                text = text + instruction[i]
            elif re.match('[0-9]', instruction[i]) != None:
                text = text+instruction[i]
                estado = 6
                if i == len(instruction)-1:
                    tokens.append({'tk_numero' : float(text)})
                    instructionBlocs.append(float(text))
        elif estado == 4:
            if instruction[i] == '"':
                estado = 5
                tokens.append({'tk_texto' : text})
                instructionBlocs.append(text)
                text = ''
            else:
                text = text+instruction[i]
        elif estado == 5:
            if instruction[i] == " ":
                estado = 0
        elif estado == 6:
            if re.match('[0-9]', instruction[i]) != None:
                text = text + instruction[i]
                if i == len(instruction)-1:
                    tokens.append({'tk_numero' : float(text)})
                    instructionBlocs.append(float(text))
            elif instruction[i] == ".":
                text = text + instruction[i]
                estado = 7
            elif instruction[i] == " ":
                tokens.append({'tk_numero' : float(text)})
                instructionBlocs.append(float(text))
                estado = 0
                text = ''
        elif estado == 7:
            if re.match('[0-9]', instruction[i]) != None:
                text = text + instruction[i]
                if i == len(instruction)-1:
                    tokens.append({'tk_numero' : float(text)})
                    instructionBlocs.append(float(text))
            elif instruction[i] == " ":
                tokens.append({'tk_numero' : float(text)})
                instructionBlocs.append(float(text))
                estado = 0
                text = ''
        elif estado == 8 :
            if re.match('[a-z]|[A-Z]', instruction[i])!= None:
                text = text + instruction[i]
                if i == len(instruction)-1:
                    if re.match('(T|t)(R|r)(U|u)(E|e)', text) != None:
                        tokens.append({'tk_boolean' : True})
                        instructionBlocs.append(True)
                    else:
                        tokens.append({'tk_boolean' : False})
                        instructionBlocs.append(False)
            elif instruction[i] == " ":
                estado = 0
                if re.match('(T|t)(R|r)(U|u)(E|e)', text) != None:
                    tokens.append({'tk_boolean' : True})
                    instructionBlocs.append(True)
                else:
                    tokens.append({'tk_boolean' : False})
                    instructionBlocs.append(False)
                text = ''
        elif estado == 9:
            if instruction[i] ==']':
                estado = 0
                tokens.append({'tk_regex' : text})
                instructionBlocs.append(text)
                text = ''
                tokens.append({'tk_corcheteCierre':']'})
            else:
                text = text + instruction[i]
        i += 1
    
    return(instructionBlocs)

#========================================================#
#SE ENCARGA DE VERIFICAR SI ES UNA PALABRA RESERVADA O NO#
#========================================================#
def verificacionReservada(text):
    for i in palabras:
        if i == str(text).upper():
            return True
    return False