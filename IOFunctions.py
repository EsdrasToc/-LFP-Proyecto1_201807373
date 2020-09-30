import re
from colorama import Fore

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
                #print('tk_parI = (')
            else:
                break
        elif estado==1:
            if texto[indice] == '<':
                estado = 2
                #print('tk_menor = <')
            else:
                break
        elif estado==2:
            tk_atributo=''
            tk_bool = ''
            tk_num = ''
            tk_string = ''
            if texto[indice]=='[':
                estado = 3
                #print('tk_corchI = [')
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
                #print("tk_atributo = " + tk_atributo)
                #print('tk_corchF = ]')
                
            elif re.match('(.)*', texto[indice])!=None:
                tk_atributo = tk_atributo + texto[indice]
                estado = 4
            else:
                break
        elif estado==5:
            if texto[indice] == '=':
                estado = 6
                #print('tk_equal = =')
            else:
                break
        elif estado==6:
            if texto[indice] == '+':
                estado = 7
                #print('tk_sign = +')
                tk_num = tk_num + texto[indice]
            elif texto[indice] == '-':
                estado = 8
                tk_num = tk_num + texto[indice]
                #print('tk_sign = -')
            elif re.match('[0-9]', texto[indice]):
                estado = 9
                tk_num = tk_num + texto[indice]
            elif texto[indice] == '"':
                estado = 10
                #print('tk_comillas = "')
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
                #print('tk_num = '+tk_num)
                #print('tk_coma = ,')
                listado[tk_atributo] = float(tk_num)
                listado.update(listado)
                estado = 2
            elif texto[indice] == '>':
                estado = 14
                listado[tk_atributo] = float(tk_num)
                listado.update(listado)
                #print('tk_num = '+tk_num)
                #print('tk_mayor = >')
            else:
                break
        elif estado==10:
            if texto[indice] == '"':
                #print('tk_string = '+tk_string)
                #print('tk_comillas = "')
                switchEspacios = False
                estado = 12
            else:
                estado = 11
                tk_string = tk_string + texto[indice]
        elif estado==11:
            if texto[indice] == '"':
                #print('tk_string = "'+tk_string+'"')
                #print('tk_comillas = "')
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
                #print('tk_coma = ,')
            elif texto[indice] == '>':
                estado = 14
                listado[tk_atributo] = tk_string
                listado.update(listado)
                #print('tk_mayor = >')
            else:
                break
        elif estado==13:
            if re.match('[a-z]|[A-Z]', texto[indice])!=None:
                estado = 13
                tk_bool = tk_bool + texto[indice]
            elif texto[indice] == ',':
                estado = 2
                #listado[tk_atributo] = bool(tk_bool)
                listado.update(listado)
                if(re.match('(F|f)(A|a)(L|l)(S|s)(E|e)',tk_bool)):
                    listado[tk_atributo] = False
                else:
                    listado[tk_atributo] = True
                #print('================='+listado)
                #print('tk_bool = '+tk_bool)
                #print('tk_coma = ,')
            elif texto[indice] == '>':
                estado = 14
                #listado[tk_atributo] = bool(tk_bool)
                if(re.match('(F|f)(A|a)(L|l)(S|s)(E|e)',tk_bool)):
                    listado[tk_atributo] = False
                else:
                    listado[tk_atributo] = True
                listado.update(listado)
                #print('tk_bool = '+tk_bool)
                #print('tk_mayor = >')
            else:
                break
        elif estado==14:
            listadoF.append(listado)
            listado = None
            listado = {}
            if texto[indice] == ')':
                estado = 15
                #print('tk_parF = )')
            elif texto[indice] == ',':
                estado = 1
                #print('tk_coma = ,')
            else:
                break
        elif estado==15:
            if re.match('(.)*', texto[indice]):
                estado = 16

        indice+=1
    
    return listadoF

#===============================#
#FUNCION PARA ESCRIBIR CON COLOR#
#===============================#
def Color(color):
    if  re.match('(P|p)(I|i)(N|n)(K|k)', color) != None:
        print(Fore.MAGENTA)
        return 'PINK'
    elif re.match('(B|b)(L|l)(U|u)(E|e)', color) != None:
        print(Fore.BLUE)
        return 'BLUE'
    elif re.match('(R|r)(E|e)(D|d)', color) != None:
        print(Fore.RED)
        return 'RED'
    elif re.match('(G|g)(R|r)(E|e)(E|e)(N|n)', color) != None:
        print(Fore.GREEN)
        return 'GREEN'
    elif re.match('(Y|y)(E|e)(L|l)(L|l)(O|o)(W|w)', color) != None:
        print(Fore.YELLOW)
        return 'YELLOW'
    elif re.match('(O|o)(R|r)(A|a)(N|n)(G|g)(E|e)', color) != None:
        print(Fore.LIGHTRED_EX)
        return 'ORANGE'
    else:
        return None

#===========================================#
#FUNCION PARA ESCRIBIR REGISTROS SOLICITADOS#
#===========================================#
def Select(verAtributos, atributo, comparador, contenido, operador, general):

    #return currentGroup.data
    data = []
    data2 = []

    if comparador == None:
        if verAtributos != None:
            data = seleccionarAtributos(general.currentGroup.data, verAtributos)
            return data
        else:
            return general.currentGroup.data
    else:
        if re.match('(O|o)(R|r)', operador) != None:
            for i in general.currentGroup.data:
                if Comparar(i, atributo[0], comparador[0], contenido[0]) or Comparar(i, atributo[1], comparador[1], contenido[1]):
                    data.append(i)
        elif re.match('(A|a)(N|n)(D|d)', operador) != None:
            for i in general.currentGroup.data:
                if Comparar(i, atributo[0], comparador[0], contenido[0]) and Comparar(i, atributo[1], comparador[1], contenido[1]):
                    data.append(i)
        elif re.match('(X|x)(O|o)(R|r)', operador) != None:
            for i in general.currentGroup.data:
                if xor(Comparar(i, atributo[0], comparador[0], contenido[0]),Comparar(i, atributo[1], comparador[1], contenido[1])):
                    data.append(i)
        else:
            for i in general.currentGroup.data:
                if Comparar(i, atributo[0], comparador[0], contenido[0]):
                    data.append(i)


        if verAtributos != None:
            data2 = seleccionarAtributos(data, verAtributos)
            return data2
        else:
            return data


def seleccionarAtributos(initialData, verAtributos):
    data = []
    for i in initialData:
        dataObject = {}
        for j  in verAtributos:
            dataObject.update(i[j])
        data.append(dataObject)
        dataObject = None
    
    return data

def xor(bool1, bool2):
    if (not bool1 and bool2) or (bool1 and not bool2):
        return True
    else:
        return False

def Comparar(registro ,atributo, comparador, contenido):
    if comparador == "=":
        if registro[atributo] == contenido:
            return True
    elif comparador == "<=":
        if registro[atributo] <= contenido:
            return True
    elif comparador == ">=":
        if registro[atributo] >= contenido:
            return True
    elif comparador == "!=":
        if registro[atributo] != contenido:
            return True
    elif comparador == "<":
        if registro[atributo] < contenido:
            return True
    elif comparador == ">":
        if registro[atributo] > contenido:
            return True
    
    return False

#=====================#
#CREAR HTML CON TOKENS#
#=====================#
def reportTokens(tokens):
    text1 = '<!DOCTYPE html><html><head><title>Reporte</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous"></head><body><table class="table table-striped table-dark"><thead><tr><th scope="col">#</th><th scope="col">TOKEN</th><th scope="col">CONTENIDO</th><th scope="col">DESCRIPCION</th></tr></thead><tbody>'
    text3 = '</tbody></table></body></html>'
    text2 = ''
    description = ''
    id = 1
    for i in tokens:
        token_names = None
        token_names = list(i.keys())
        for j in token_names:
            if j == 'tk_palabra':
                description = "Palabra reservada, es decir, palabra perteneciente al lenguaje"
            elif j == 'tk_identificador':
                description = "Utilizada para identificar atributos o archivos"
            elif j == 'tk_numero':
                description = "Token cuyo fin es reconocer numeros"
            elif j == 'tk_texto':
                description = "Cadenas de texto"
            elif j == 'tk_boolean':
                description = 'Los valores booleanos son Verdadero o Falso'
            elif j == 'tk_operador':
                description = 'Todos aquellos simbolos que se utilizan para operar o comparar'
            elif j == 'tk_asterisco':
                description = 'signo asterisco utilizado para referirse a todos'
            elif j == 'tk_coma':
                description = 'la coma es utilizada para separar identificadores'
            elif j == 'tk_puntoComa':
                description = 'Finalizador de instrucciones en instrucciones dadas por archivo .SIQL'
            else:
                description = 'faltante'
            
            text2 = text2 + '<tr><th scope="row">'+str(id)+'</th><td>'+str(token_names[0])+'</td><td>'+str(i[token_names[0]])+'</td><td>'+description+'</td></tr>'

        id += 1
    
    with open('REPORTE_TOKENS.html', "w") as report:
        report.write(text1+text2+text3)

def Min(data, attributes):
    auxiliar = None
    inicio = True
    resultados = []

    if attributes == None:
        dictAux = {}
        for j in data:
            dictAux.update(j)
        attributes = list(dictAux.keys())

    for i in attributes:
        auxiliar = None
        for j in data:
            if j[i] == None:
                continue

            if inicio:
                auxiliar = j[i]
                inicio = False
            else:
                if j[i] < auxiliar:
                    auxiliar = j[i]
        resultados.append({i : auxiliar})
        inicio = True
    
    return resultados

def Max(data, attributes):
    auxiliar = None
    inicio = True
    resultados = []

    if attributes == None:
        dictAux = {}
        for j in data:
            dictAux.update(j)
        attributes = list(dictAux.keys())

    for i in attributes:
        auxiliar = None
        for j in data:
            if j[i] == None:
                continue
            
            if inicio:
                auxiliar = j[i]
                inicio = False
            else:
                if j[i] > auxiliar:
                    auxiliar = j[i]
        resultados.append({i : auxiliar})
        inicio = True
    
    return resultados

def Sum(data, attributes):
    resultados = []

    if attributes == None:
        dictAux = {}
        for j in data:
            dictAux.update(j)
        attributes = list(dictAux.keys())

    for i in attributes:
        sumatoria = 0
        for j in data:
            if j[i] == None:
                continue
            
            if str(type(j[i])) == "<class 'float'>":
                sumatoria += j[i]
        resultados.append({i : sumatoria})
    
    return resultados

def Count(data, attributes):
    resultados = []

    if attributes == None:
        dictAux = {}
        for j in data:
            dictAux.update(j)
        attributes = list(dictAux.keys())

    for i in attributes:
        k = 0
        for j in data:
            if j[i] == None:
                continue
            else:
                k += 1
        resultados.append({i : k})
    
    return resultados