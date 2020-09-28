import re
import IOFunctions
import Clases

#==============#
#CREANDO TOKENS#
#==============#
palabras = ['CREATE','SET','LOAD','INTO','FILES','USE','SELECT','WHERE','LIST','ATTRIBUTES','PRINT',
'IN','MAX','MIN','SUM','COUNT','REPORT','TO','SCRIPT','TOKENS','REGEX', 'AND', 'OR']

#===========================================#
#AUTOMATA CREADO PARA LEER LAS INSTRUCCIONES#
#===========================================#

def readInstruction(instruction, tokens):
    estado = 0
    i = 0
    text = ''
    #tokens = []
    instructionBlocs = []
    
    while i < len(instruction):
        if estado == 0:
            if instruction[i] == '*':
                tokens.append({'tk_asterisco' : '*'})
                instructionBlocs.append('*')
            if re.match('[a-z]|[A-Z]|_', instruction[i]) != None:
                text = text + instruction[i]
                estado =1
            elif re.match('=|<|>|!', instruction[i]) != None:
                estado = 2
                text = text +instruction[i]
        elif estado == 1:
            if re.match('[a-z]|[A-Z]|_|[0-9]|\.|\*', instruction[i]) != None:
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
        i += 1
        
    return(instructionBlocs)

def verificacionReservada(text):
    for i in palabras:
        if i == str(text).upper():
            return True
    return False



