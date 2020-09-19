import re
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