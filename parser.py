import os
import sys


class Parser:

    def __init__(self):
        os.chdir(sys.path[0])
        self.commands = ""
        self.blocks = []
        self.checked_blocks = []

        self.def_variables = {}
        self.def_functions = {}

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

        for block in self.blocks:
            checked_block = self.evaluate_production(block)
            self.checked_blocks.append(checked_block)


    def evaluate_production(self, block) -> tuple:

        block_definition = (False, None) #Tupla que determina si el bloque es válido [0] y el grupo al que pertenece [1]

        #Command evaluation
        block = block[1:len(block)-1]
        instruction = block.split(" ")

        if "defvar" in block and len(instruction) == 3:   #Regla de producción -- Definición de variables
            if instruction[0] == "defvar" and type(instruction[1]) == str and self.isNumber(instruction[2]):
                block_definition = (True, "DEFVAR")
                self.def_variables[instruction[1]] = instruction[2]

        elif "=" in block and len(instruction) == 3:
            if instruction[0] == "=" and type(instruction[1]) == str and self.isNumber(instruction[2]):
                if self.isVariable(instruction[1]):
                    block_definition = (True, "ASSINGVAR")

        elif "move" in block and len(instruction) == 2:
            if instruction[0] == "move" and (self.isNumber(instruction[1]) or self.isVariable(instruction[1])):
                block_definition = (True, "MOVE")
            
        return block_definition    

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

parser = Parser()
parser.set_commands("invalidCommands.txt")
parser.parse()
print(parser.checked_blocks)