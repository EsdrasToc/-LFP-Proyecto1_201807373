import Clases
import RI
import automatas

general = Clases.General()
initialInstruction = ''
instruction = []

while general.cicle:

    initialInstruction = input('$')

    RI.decision(automatas.readInstruction(initialInstruction, general.tokens), general)