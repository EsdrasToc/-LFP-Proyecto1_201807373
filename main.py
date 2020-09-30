import Clases
import RI

general = Clases.General()
initialInstruction = ''
instruction = []

while general.cicle:

    initialInstruction = input('$')

    RI.decision(automatas.readInstruction(initialInstruction, general.tokens), general)