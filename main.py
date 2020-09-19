import Clases
import re
import automatas

currentGroup = None
groups = []
cicle = True
instruction = ''
firstInstruction = ''

##### AQUI SE GUARDAN LOS TOKENS #####
tk_id = []

#CICLO PARA LECTURA DE INSTRUCCIONES#
while cicle == True:
    instruction = input('$')
    instruction = instruction.lstrip()
    i = 0
    firstInstruction = ''
    spaceCondition = True
    
    while i < len(instruction):
        if re.match('[a-z]|[A-Z]', instruction[i]) != None:
            firstInstruction = firstInstruction + instruction[i]
            spaceCondition = False
        elif re.match('[a-z]|[A-Z]', instruction[i]) == None and spaceCondition == False:
            break
        i = i+1
    
    instruction = instruction.replace(firstInstruction, '')
    if re.match('(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)', firstInstruction):
        reply = automatas.Create_Use(instruction)
        if reply != None:
            groups.append(Clases.Group(reply))
            tk_id.append(reply)
        else:
            print('=== SE HA PRODUCIDO UN ERROR ===')
    elif re.match('(U|u)(S|s)(E|e)', firstInstruction) != None:
        reply = automatas.Create_Use(instruction)
        if reply != None:
            find = False
            tk_id.append(reply)
            for i in groups:
                if i.nombre == reply:
                    currentGroup = i
                    find = True
                    break
            if find == False:
                print('=== NO SE ENCONTRO UN SET CON ESTE NOMBRE ===')
            else:
                print('=== USTED ESTA UTILIZANDO EL SET '+ currentGroup.nombre +' ===')
        else:
            print('=== SE HA PRODUCIDO UN ERROR ===')
    
    elif re.match('(E|e)(X|x)(I|i)(T|t)', firstInstruction):
        cicle = False
    else:
        print('=== LA INSTRUCCION NO ES VALIDA ===')