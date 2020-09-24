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
tk_palabras = []
tk_menor = []
tk_mayor = []
tk_coma = []
tk_texto = []
tk_numero = []
tk_booleano = []
tk_igual = []
tk_negacion = []
tk_asterisco = []

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
    elif re.match('(L|l)(O|o)(A|a)(D|d)', firstInstruction) != None:

        try:
            automatas.Load(groups, tk_id, instruction)
        except:
            print('=== OCURRIO UN ERROR AL CARGAR LOS DATOS ===')
    
    elif re.match('(S|s)(E|e)(L|l)(E|e)(C|c)(T|t)', firstInstruction) != None:

        tk_palabras.append('SELECT')
        automatas.Select(groups, instruction, tk_id, tk_palabras, tk_menor, tk_mayor, tk_coma, tk_texto, tk_numero, tk_booleano, tk_igual, tk_negacion, tk_asterisco)

    elif re.match('(E|e)(X|x)(I|i)(T|t)', firstInstruction):
        cicle = False
    else:
        print('=== LA INSTRUCCION NO ES VALIDA ===')