FETCH, STORE, ASTORE, PUSH, POP, ADD, SUB, MUL, DIV, LT, GT, EQ, NOTEQ, JZ, JNZ, JMP, HALT = range(17)

class Node:
    def __init__(self, name, op1, op2, op3):
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return f'Node("{self.name}", {self.op1}, {self.op2}, {self.op3})'

class Compiler:
    def __init__(self):
        self.program = []
        self.pc = 0
        self.funcs = {}

    def gen(self, command):
        self.program.append(command)
        self.pc = self.pc + 1

    def compilenode(self, node):
        try:
            name = node.name
        except:
            name = node[0].name
            node = node[0]
        if name == 'NUM':
            self.gen(PUSH)
            self.gen(int(node.op1))
        elif name == 'ID':
            self.gen(FETCH)
            self.gen(node.op1)
        elif name == 'STRING':
            self.gen(PUSH)
            self.gen(node.op1)
        elif name == '+':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(ADD)
        elif name == '-':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(SUB)
        elif name == '/':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(DIV)
        elif name == '*':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(MUL)
        elif name == '<':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(LT)
        elif name == '>':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(GT)
        elif name == '!=':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(NOTEQ)
        elif name == '==':
            self.compilenode(node.op1)
            self.compilenode(node.op2)
            self.gen(EQ)
        elif name == 'assign':
            self.compilenode(node.op2)
            self.gen(STORE)
            self.gen(node.op1)
        elif name == 'int':
            self.compilenode(node.op2)
            self.gen('int')
            self.gen(node.op1)
        elif name == 'char':
            self.compilenode(node.op2)
            self.gen('char')
            self.gen(node.op1)
        elif name == 'do':
            addr = self.pc
            self.compilenode(node.op1)
            for i in node.op2:
                self.compilenode(i)
            self.gen(JNZ)
            self.gen(addr)
        elif name == 'if':
            self.compilenode(node.op1)
            self.gen(JZ)
            addr = self.pc
            self.gen(0)
            for i in node.op2:
                self.compilenode(i)
            self.program[addr] = self.pc
        elif name == 'void':
            func_name = node.op1
            args = node.op2
            body = node.op3
            self.funcs[func_name] = {
                'args': args,
                'body': body,
            }
        elif name == 'call':
            if node.op1 in self.funcs:
                cur = 0
                for i in node.op2:
                    self.compilenode(i)
                    self.gen(ASTORE)
                    self.gen(self.funcs[node.op1]['args'][cur].op1)
                    cur += 1
                for j in self.funcs[node.op1]['body']:
                    self.compilenode(j)
            else:
                raise NameError('function '+str(node.op1)+' not found')
        elif name == 'while':
            if node.op1.op2:
                try:
                    r = node.op1.op2
                    if node.op1.name == '<':
                        d = str(int(r.op1) - 1)
                    else:
                        d = str(int(r.op1))
                    r.op1 = d
                except:
                    r = node.op1.op1
                    if node.op1.name == '<':
                        d = str(int(r.op1) - 1)
                    else:
                        d = str(int(r.op1))
                    r.op1 = d
            addr1 = self.pc
            self.compilenode(node.op1)
            self.gen(JZ)
            addr2 = self.pc
            self.gen(1)
            for i in node.op2:
                self.compilenode(i)
            self.gen(JMP)
            self.gen(addr1)
            self.program[addr2] = self.pc
        elif name == 'else':
            self.compilenode(node.op1)
            self.gen(JZ)
            addr1 = self.pc
            self.gen(0)
            for i in node.op2:
                self.compilenode(i)
            self.gen(JMP)
            addr2 = self.pc
            self.gen(0)
            self.program[addr1] = self.pc
            for j in node.op3:
                self.compilenode(j)
            self.program[addr2] = self.pc

    def compileast(self, ast):
        for i in ast:
            self.compilenode(i)
        if 'main' in self.funcs:
            self.compilenode(Node('call', 'main', [], None))
        else:
            raise SyntaxError('invalid main func')
        self.gen(HALT)
        return self.program
