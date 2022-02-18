from dataclasses import replace
from operator import index
import os
import sys


class Parser:

    def __init__(self):

        #Parser initialization...
        os.chdir(sys.path[0])

        #Parser class variables
        self.commands = ""
        self.blocks = []
        self.checked_blocks = []
        self.def_variables = {}
        self.def_functions = {}

        #Aditional non-terminal symbols for reference
        self.rotate_constants = (":left", ":right", ":around")
        self.cardinal_constants = (":north", ":south", ":east", ":west")
        self.balloons_chips = ("Balloons", "Chips")
        self.move_constants = (":left", ":right", ":front", ":back")

    def set_commands(self, file_name):
        with open(file_name) as command_file:
            self.commands = command_file.read()
 
    def parse(self):        
        self.delete_tabs()
        self.check_parenthesis()
        self.detect_blocks()
        self.evaluate_blocks()

    def delete_tabs(self):
        self.commands = self.commands.replace("\n","")


    def check_parenthesis(self) -> bool:
        """Función de revisión inicial que determina que los paréntesis estén 
        balanceados y emparejados correctamente."""
        parenthesis_stack = []

        for char_new in self.commands:
            if char_new == "(" or char_new == ")":
                parenthesis_stack.append(char_new)

            if char_new == ")":
                char_old_index = len(parenthesis_stack)-2
                char_old = parenthesis_stack[char_old_index]

                if char_old == "(":
                    parenthesis_stack.pop()
                    parenthesis_stack.pop()

        return len(parenthesis_stack) == 0        


    def detect_blocks(self):
        parenthesis_stack = []
        count = 0
        for char in self.commands:
            if char == "(" or char == ")":
                parenthesis_stack.append((char, count))
                
            if len(parenthesis_stack)-1 >= 1 and parenthesis_stack[len(parenthesis_stack)-1][0] == ")" and parenthesis_stack[len(parenthesis_stack)-2][0]=="(":
                
                start_index = parenthesis_stack[len(parenthesis_stack)-2][1]
                end_index = parenthesis_stack[len(parenthesis_stack)-1][1]
                self.blocks.append(self.commands[start_index:end_index+1])
                parenthesis_stack.pop()
                parenthesis_stack.pop()

            count += 1
            

    def evaluate_blocks(self):

        block_index = 0
        for block in self.blocks:
            checked_block = self.evaluate_production(block, block_index)
            self.checked_blocks.append(checked_block)
            block_index += 1


    def evaluate_production(self, block, block_index) -> tuple:

         #Tupla que determina si el bloque es válido [0] y el grupo al que pertenece [1]
        block_definition = (False, None) 

        
        block = block[1:len(block)-1]
        block = self.replaceInternalBlocks(block)
        instruction = block.split(" ")


        #Command evaluation
        if "defvar" in block and len(instruction) == 3:   #Regla de producción -- Definición de variables
            if instruction[0] == "defvar" and type(instruction[1]) == str and self.isNumber(instruction[2]):
                block_definition = (True, "COMMAND")
                self.def_variables[instruction[1]] = instruction[2]

        if "=" in block and len(instruction) == 3:
            if instruction[0] == "=" and type(instruction[1]) == str and self.isNumber(instruction[2]):
                if self.isVariable(instruction[1]):
                    block_definition = (True, "COMMAND")

        if "move" in block and len(instruction) == 2:
            if instruction[0] == "move" and (self.isNumber(instruction[1]) or self.isVariable(instruction[1])):
                block_definition = (True, "COMMAND")

        if "turn" in block and len(instruction) == 2:
            if instruction[0] == "turn" and instruction[1] in self.rotate_constants:
                block_definition = (True, "COMMAND")

        if "face" in block and len(instruction) == 2:
            if instruction[0] == "face" and instruction[1] in self.cardinal_constants:
                block_definition = (True, "COMMAND")

        if "put" in block and len(instruction) == 3:
            if instruction[0] == "put" and instruction[1] in self.balloons_chips and (self.isNumber(instruction[2]) or self.isVariable(instruction[2])):
                block_definition = (True, "COMMAND")

        if "pick" in block and len(instruction) == 3:
            if instruction[0] == "pick" and instruction[1] in self.balloons_chips and (self.isNumber(instruction[2]) or self.isVariable(instruction[2])):
                block_definition = (True, "COMMAND")

        if "move-dir" in block and len(instruction) == 3:
            if instruction[0] == "move-dir" and (self.isNumber(instruction[1]) or self.isVariable(instruction[1])) and instruction[2] in self.move_constants:
                block_definition = (True, "COMMAND")

        if "run-dirs" in block and len(instruction) == 2:
            if instruction[0] == "run-dirs" and self.getPreviousBlockType(block_index, 1) == "DIRECTION-LIST":
                block_definition = (True, "COMMAND")

        if "move-face" in block and len(instruction) == 3:
             if instruction[0] == "move-face" and (self.isNumber(instruction[1]) or self.isVariable(instruction[1])) and instruction[2] in self.cardinal_constants:
                 block_definition = (True, "COMMAND")

        if "skip" in block and len(instruction) == 1:
            if instruction[0] == "skip":
                block_definition = (True, "COMMAND")

    
        #Conditional evaluation
        if "if" in block and len(instruction) == 4:
            if instruction[0] == "if" and self.getPreviousBlockType(block_index, 3) == "CONDITION"  and self.getPreviousBlockType(block_index, 2) == "COMMAND" and self.getPreviousBlockType(block_index, 1) == "COMMAND":
                block_definition = (True, "COMMAND", "CONDITIONAL")

        #Condition evaluation
        if "facing-p" in block and len(instruction) == 2:
            if instruction[0] == "facing-p" and instruction[1] in self.cardinal_constants:
                block_definition = (True, "CONDITION")

        if "can-put-p" in block and len(instruction) == 3:
            if instruction[0] == "can-put-p" and instruction[1] in self.balloons_chips and (self.isNumber(instruction[2]) or self.isVariable(instruction[2])):
                block_definition = (True, "CONDITION")

        if "can-pick-p" in block and len(instruction) == 3:
            if instruction[0] == "can-pick-p" and instruction[1] in self.balloons_chips and (self.isNumber(instruction[2]) or self.isVariable(instruction[2])):
                block_definition = (True, "CONDITION")

        if "can-move-p" in block and len(instruction) == 2:
            if instruction[0] == "can-move-p" and instruction[1] in self.cardinal_constants:
                block_definition = (True, "CONDITION")

        if "not" in block and len(instruction) == 2:
            if instruction[0] == "not" and self.getPreviousBlockType(block_index, 1) == "CONDITION":
                block_definition = (True, "CONDITION")

        
        #Special blocks evaluation
        elif instruction[0] in self.move_constants:
            for i in instruction:
                if i in self.move_constants:
                    block_definition = (True, "DIRECTION-LIST")
                else:
                    block_definition = (False, None)
                    break

        return block_definition    


    def replaceInternalBlocks(self, block):

        ignore = False
        replaced_block = ""

        for char in block:
            if char == "(":
                ignore = True

            elif char == ")":
                ignore = False
                replaced_block += "BLOCK"
                
            elif not ignore:
                replaced_block += char    

        return replaced_block

    ### HELPER METHODS ###

    def isNumber(self, number) -> bool:
        check = True
        try:
            float(number)   
        except:
            check = False; 
        return check


    def isVariable(self, name)->bool:
        check = False
        if name in self.def_variables.keys():
            check = True
        return check


    def getPreviousBlockType(self, actualBlockIndex , stepBehind):
        return self.checked_blocks[actualBlockIndex - stepBehind][1]

parser = Parser()
parser.set_commands("invalidCommands.txt")
parser.parse()
print(parser.checked_blocks)