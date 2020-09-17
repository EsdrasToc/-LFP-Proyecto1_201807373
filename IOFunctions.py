import re

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
