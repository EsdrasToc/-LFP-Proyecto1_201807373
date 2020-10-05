import Clases
import RI
import automatas

general = Clases.General()
initialInstruction = ''
instruction = []

while general.cicle:

    initialInstruction = input('$')
    try:
        RI.decision(automatas.readInstruction(initialInstruction, general.tokens), general)
    except:
        print('HA OCURRIDO UN ERROR CON LA INSTRUCCION')