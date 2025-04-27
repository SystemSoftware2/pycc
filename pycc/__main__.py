'''
Последняя стадия разработки компилятора ANSI C:
выполнение кода.
'''
from lexer import *
from parser import *
from compiler import *
from vm import *
from cpp import *
import sys

def run_c(program):
    parser = Parser()

    compiler = Compiler()

    ast = parser.parse(c_lexer(preproc(program)))
    bytecode = compiler.compileast(ast)

    vm = VirtualMachine()
    vm.run(bytecode)
    
args = sys.argv

if len(args) == 1:
    print('Usage: pycc name.c')

elif len(args) == 2:
    with open(args[1], 'r', encoding='utf-8') as f:
        try:
            run_c(f.read())
        except Exception as err:
            print('Error:', err)
