from .lexer import *
from .parser import *
from .compiler import *
from .vm import *
from .cpp import *
import sys

def run_c(program):
    parser = Parser()

    compiler = Compiler()

    ast = parser.parse(c_lexer(preproc(program)))
    bytecode = compiler.compileast(ast)

    vm = VirtualMachine()
    vm.run(bytecode)
