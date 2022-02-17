import os
import sys

class Parser:

    def __init__(self):
        os.chdir(sys.path[0])
        self.commands = ""

    def set_commands(self, file_name):
        with open(file_name) as command_file:
            self.commands = command_file.read()

    def parse(self):        
        self.clean_separators()
    
    def clean_separators(self):
        pass

parser = Parser()
parser.set_commands("invalidCommands.txt")
parser.parse()