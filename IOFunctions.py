import re
from colorama import Fore

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
def SelectWREGEX(verAtributos, atributo, contenido, general):
    regex = contenido[0]
    regex = re.compile(str(regex))
    data = []

    print(contenido[0])
    
    for i in general.currentGroup.data:
        try:
            if regex.search(str(i[atributo[0]])) != None:
                if str(regex.search(i[atributo[0]]).span()) != '(0, 0)':
                    data.append(i)
        except:
            continue

    if verAtributos != None:
        data = seleccionarAtributos(data, verAtributos)
        return data
    else:
        return data

def Select(verAtributos, atributo, comparador, contenido, operador, general):

    data = []
    data2 = []

    if comparador == None:
        if verAtributos != None:
            data = seleccionarAtributos(general.currentGroup.data, verAtributos)
            return data
        else:
            return general.currentGroup.data
    else:
        #if re.match('(O|o)(R|r)', operador) != None:
        if str(operador).upper() == 'OR':
            for i in general.currentGroup.data:
                try:
                    if Comparar(i, atributo[0], comparador[0], contenido[0]) or Comparar(i, atributo[1], comparador[1], contenido[1]):
                        data.append(i)
                except:
                    continue
        #elif re.match('(A|a)(N|n)(D|d)', operador) != None:
        elif str(operador).upper() == 'AND':
            for i in general.currentGroup.data:
                try:
                    if Comparar(i, atributo[0], comparador[0], contenido[0]) and Comparar(i, atributo[1], comparador[1], contenido[1]):
                        data.append(i)
                except:
                    continue
        #elif re.match('(X|x)(O|o)(R|r)', operador) != None:
        elif str(operador).upper() == 'XOR':
            for i in general.currentGroup.data:
                try:
                    if xor(Comparar(i, atributo[0], comparador[0], contenido[0]),Comparar(i, atributo[1], comparador[1], contenido[1])):
                        data.append(i)
                except:
                    continue
        else:
            for i in general.currentGroup.data:
                try:
                    if Comparar(i, atributo[0], comparador[0], contenido[0]):
                        data.append(i)
                except:
                    continue

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
            try:
                dataObject.update({j : i[j]})
            except:
                continue
        data.append(dataObject)
        dataObject = None
    
    return data

def xor(bool1, bool2):
    if (not bool1 and bool2):
        return True
    elif (bool1 and not bool2):
        return True
    else:
        return False

def Comparar(registro ,atributo, comparador, contenido):
    try:
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
    except:
        return False
    
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
            elif j == 'tk_regex':
                description = 'Almacena una expresion regular'
            elif j == 'tk_corcheteApertura':
                description = 'Idica el inicio de una regex'
            elif j == 'tk_corcheteCierre':
                description = 'Indica el final de una regex'
            else:
                description = 'faltante'
            
            try:
                text2 = text2 + '<tr><th scope="row">'+str(id)+'</th><td>'+str(token_names[0])+'</td><td>'+str(i[token_names[0]])+'</td><td>'+description+'</td></tr>'
            except:
                continue
        id += 1
    
    with open('REPORTE_TOKENS.html', "w") as report:
        report.write(text1+text2+text3)

#=========================#
#ENCUENTRA EL VALOR MINIMO#
#=========================#

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
            try:
                if j[i] == None:
                    continue

                if inicio:
                    auxiliar = j[i]
                    inicio = False
                else:
                    if j[i] < auxiliar:
                        auxiliar = j[i]
            except:
                continue
        resultados.append({i : auxiliar})
        inicio = True
    
    return resultados

#=========================#
#ENCUENTRA EL VALOR MAXIMO#
#=========================#

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
            try:
                if j[i] == None:
                    continue
                
                if inicio:
                    auxiliar = j[i]
                    inicio = False
                else:
                    if j[i] > auxiliar:
                        auxiliar = j[i]
            except:
                continue
        resultados.append({i : auxiliar})
        inicio = True
    
    return resultados

#====================#
#REALIZA LA SUMATORIA#
#====================#

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
            try:
                if j[i] == None:
                    continue
                
                if str(type(j[i])) == "<class 'float'>":
                    sumatoria += j[i]
            except:
                continue
        resultados.append({i : sumatoria})
    
    return resultados

#================================================#
#REALIZA EL CONTEO DE LOS ATRIBUTOS SELECCIONADOS#
#================================================#
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
            try:
                if j[i] == None:
                    continue
                else:
                    k += 1
            except:
                continue
        resultados.append({i : k})
    
    return resultados

#=============================#
#ESCRITURA DE REPORTES EN HTML#
#=============================#
def reportHTMLWSelect(data,nombre):

    dictAux = {}
    for j in data:
        dictAux.update(j)
    attributes = list(dictAux.keys())

    text1 = '<!DOCTYPE html><html><head><title>Reporte</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous"></head><body><table class="table table-striped table-dark"><thead><tr><th scope="col">#</th>'
    text3 = '</tbody></table></body></html>'
    text2 = ''
    id = 1
    for i in attributes:
        text1 = text1 +'<th scope="col">'+str(i)+'</th>'
    text1 = text1+'</tr></thead><tbody>'

    for i in data:
        text2 = text2+'<tr><th scope="row">'+str(id)+'</th>'
        for j in attributes:
            try:
                text2 = text2 +'<td>'+ str(i[j])+'</td>'
            except:
                text2 = text2 +'<td>'+ 'NULL'+'</td>'
        text2 = text2 + '</tr>'
        id += 1

    with open(nombre, "w") as report:
        report.write(text1+text2+text3)

def reportHTMLWMMSC(data,nombre):
    dictAux = {}
    for j in data:
        dictAux.update(j)
    attributes = list(dictAux.keys())

    text1 = '<!DOCTYPE html><html><head><title>Reporte</title><link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous"></head><body><table class="table table-striped table-dark"><thead><tr><th scope="col">#</th><th scope="col">Atributo</th><th scope="col">Resultado</th></tr></thead><tbody>'
    text3 = '</tbody></table></body></html>'
    text2 = ''
    id = 1

    for i in attributes:
        try:
            text2 = text2+'<tr><th scope="row">'+str(id)+'</th>'
            text2 = text2 +'<td>'+ i +'</td>'
            text2 = text2 +'<td>'+ str(dictAux[i])+'</td></tr>'
            
            id += 1
        except:
            continue
    try:    
        with open(nombre, "w") as report:
            report.write(text1+text2+text3)
    except:
        print('NO SE PUDO ESCRIBIR EL REPORTE')