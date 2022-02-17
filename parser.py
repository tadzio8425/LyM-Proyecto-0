import os
import sys


class Parser:

    def __init__(self):
        os.chdir(sys.path[0])
        self.commands = ""
        self.blocks=[]

    def set_commands(self, file_name):
        with open(file_name) as command_file:
            self.commands = command_file.read()
 
    def parse(self):        
        self.delete_tabs()
        self.check_parenthesis()
        self.detect_blocks()

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
            

        print(self.blocks)


        



parser = Parser()
parser.set_commands("invalidCommands.txt")
parser.parse()