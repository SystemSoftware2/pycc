from .lexer import *
from .parser import *
from .compiler import *
from .vm import *
import sys

def run_c(program):
    parser = Parser()

    compiler = Compiler()

    ast = parser.parse(c_lexer(program))
    bytecode = compiler.compileast(ast)

    vm = VirtualMachine()
    vm.run(bytecode)
