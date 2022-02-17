import os
import sys


class Parser:

    def __init__(self):
        os.chdir(sys.path[0])
        self.commands = ""

    def set_commands(self, file_name):
        with open(file_name) as command_file:
            self.commands = command_file.read()
            print(self.commands)

    def parse(self):        
        self.check_parenthesis()
        self.detect_blocks()

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
        pass



parser = Parser()
parser.set_commands("invalidCommands.txt")
parser.parse()