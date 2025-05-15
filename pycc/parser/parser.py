"""
Парсер для компилятора ANSI C.
Класс Parser - сам парсер
"""

from .node import *
import re

class Parser:
    def __init__(self):
        self.pos = 0

    def term(self, value):
        if value.isdigit():
            return Node('NUM', value, None, None)
        elif re.match('[a-zA-Z][a-zA-Z0-9_]*', value):
            return Node('ID', value, None, None)
        elif re.match('".*?"', value):
            f = value.replace(value[0], '')
            return Node('STRING', f, None, None)
        f = value.replace(value[0], '')
        return Node('STRING', f.replace('\n', '\\n'), None, None)

    def expr(self, exp):
        d = exp.split(' ')
        try:
            if exp[0] == '"':
                return self.term(exp)
            left = self.term(d[0])
            op = d[1]
            right = self.term(d[2])
            if len(d) == 4 and d[1] + d[2] == '==':
                op = d[1] + d[2]
                right = self.term(d[3])  
            return Node(op, left, right, None)
        except:
            return self.term(exp)

    def paren_expr(self, tokens):
        if tokens[self.pos][0] == '(' and (')', 'RESERVED') in tokens:
            expr = ''
            self.pos += 1
            while tokens[self.pos] != (')', 'RESERVED'):
                if tokens[self.pos + 1] == (')', 'RESERVED'):
                    expr += tokens[self.pos][0]
                else:
                    expr += tokens[self.pos][0] + ' '
                self.pos += 1
            return self.expr(expr)
        else:
            raise SyntaxError('Invalid paren expression')

    def semicolon_expr(self, tokens):
        if (';', 'RESERVED') in tokens:
            expr = ''
            self.pos += 1
            while tokens[self.pos] != (';', 'RESERVED'):
                if tokens[self.pos + 1] == (';', 'RESERVED'):
                    expr += tokens[self.pos][0]
                else:
                    expr += tokens[self.pos][0] + ' '
                self.pos += 1
            return self.expr(expr)
        else:
            raise SyntaxError('Invalid expression with semicolon')

    def parse(self, toks, block=False):
        ast = []
        astpos = 0
        while self.pos < len(toks):
            token = toks[self.pos]
            if token[0] == 'int' or token[0] == 'char':
                self.pos += 1
                name = toks[self.pos][0]
                if self.pos + 1 < len(toks) and toks[self.pos + 1][0] == '=':
                    self.pos += 1
                    value = self.semicolon_expr(toks)
                    ast.append(Node(token[0], name, value, None))
                else:
                    raise SyntaxError('invalid declaration')
            elif self.pos + 1 < len(toks) and toks[self.pos + 1][0] == '=':
                name = toks[self.pos][0]
                self.pos += 1
                value = self.semicolon_expr(toks)
                ast.append(Node('assign', name, value, None))
            elif token[0] == 'do':
                self.pos += 1
                if toks[self.pos][0] == '{':
                    blockrr = []
                    self.pos += 1
                    while self.pos < len(toks):
                        if toks[self.pos][0] == '}':
                            self.pos += 1
                            break
                        parserzv = Parser()
                        res = parserzv.parse(toks[self.pos:], block=True)
                        blockrr.append(res[0])
                        self.pos += res[1] + 1
                    self.pos -= 1
                    self.pos += 1
                    if toks[self.pos][0] == 'while':
                        self.pos += 1
                        condition = self.paren_expr(toks)
                        self.pos += 1
                        if toks[self.pos][0] == ';':
                            if block == True:
                                return ([Node('do', condition, blockrr, None)], self.pos)
                            ast.append(Node('do', condition, blockrr, None))
                        else:
                            raise SyntaxError('invalid "do" statement')
                    else:
                        raise SyntaxError('invalid "do" statement')
                else:
                    raise SyntaxError('invalid syntax')
            elif token[0] == 'while':
                self.pos += 1
                condition = self.paren_expr(toks)
                self.pos += 1
                if toks[self.pos][0] == '{':
                    block = []
                    self.pos += 1
                    while self.pos < len(toks):
                        if toks[self.pos][0] == '}':
                            self.pos += 1
                            break
                        parsere = Parser()
                        res = parsere.parse(toks[self.pos:], block=True)
                        block.append(res[0])
                        self.pos += res[1] + 1
                    self.pos -= 1
                    if block:
                        return ([Node('while', condition, block, None)], self.pos)
                    ast.append(Node('while', condition, block, None))
                else:
                    raise SyntaxError('invalid syntax')
            elif token[0] == 'void':
                self.pos += 1
                name = toks[self.pos][0]
                self.pos += 1
                if toks[self.pos][0] != '(':
                    raise SyntaxError('invalid params')
                self.pos += 1
                args = []
                for i in toks[self.pos:]:
                    if i[0] == ')':
                        break
                    d = Parser()
                    argval = ''
                    while self.pos < len(toks):
                        if toks[self.pos][0] == ',' or toks[self.pos][0] == ')':
                            if toks[self.pos][0] == ',': self.pos += 1
                            break
                        argval += toks[self.pos][0]
                        self.pos += 1
                    if d.expr(argval):
                        args.append(d.expr(argval))
                self.pos += 1
                if toks[self.pos][0] == '{':
                    blocks = []
                    self.pos += 1
                    while self.pos < len(toks):
                        if toks[self.pos][0] == '}':
                            self.pos += 1
                            break
                        parser = Parser()
                        res = parser.parse(toks[self.pos:], block=True)
                        blocks.append(res[0])
                        self.pos += res[1] + 1
                    self.pos -= 1
                    ast.append(Node(token[0], name, args, blocks))
                else:
                    raise SyntaxError('invalid syntax')
            elif token[0] == 'if':
                self.pos += 1
                condition = self.paren_expr(toks)
                self.pos += 1
                if toks[self.pos][0] == '{':
                    blockrm = []
                    self.pos += 1
                    while self.pos < len(toks):
                        if toks[self.pos][0] == '}':
                            self.pos += 1
                            break
                        parserj = Parser()
                        res = parserj.parse(toks[self.pos:], block=True)
                        blockrm.append(res[0])
                        self.pos += res[1] + 1
                    self.pos -= 1
                    if block == True:
                        self.pos += 1
                        if self.pos < len(toks) and toks[self.pos][0] == 'else':
                            self.pos += 1
                            if toks[self.pos][0] == '{':
                                blockr = []
                                self.pos += 1
                                while self.pos < len(toks):
                                    if toks[self.pos][0] == '}':
                                        self.pos += 1
                                        break
                                    parserr = Parser()
                                    res = parserr.parse(toks[self.pos:], block=True)
                                    blockr.append(res[0])
                                    self.pos += res[1] + 1
                                self.pos -= 1
                                return ([Node('else', condition, blockrm, blockr)], self.pos)
                        else:
                            self.pos -= 1
                        return ([Node('if', condition, blockrm, None)], self.pos)
                    ast.append(Node('if', condition, blockrm, None))
                else:
                    raise SyntaxError('invalid syntax')
            elif token[0] == 'else':
                if ast[astpos - 1].name == 'if':
                    self.pos += 1
                    if toks[self.pos][0] == '{':
                        block = []
                        self.pos += 1
                        while self.pos < len(toks):
                            if toks[self.pos][0] == '}':
                                self.pos += 1
                                break
                            parserr = Parser()
                            res = parserr.parse(toks[self.pos:], block=True)
                            block.append(res[0])
                            self.pos += res[1] + 1
                        self.pos -= 1
                        ast[astpos - 1].name = 'else'
                        ast[astpos - 1].op3 = block
                    else:
                        raise SyntaxError('invalid syntax')
                else:
                    raise SyntaxError('invalid "else" statement')
            elif token[1] == 'ID' and self.pos + 1 < len(toks) and toks[self.pos + 1][0] == '(':
                args = []
                name = token[0]
                self.pos += 2
                for i in toks[self.pos:]:
                    if i[0] == ')':
                        break
                    d = Parser()
                    argval = ''
                    while self.pos < len(toks):
                        if toks[self.pos][0] == ',' or toks[self.pos][0] == ')':
                            if toks[self.pos][0] == ',': self.pos += 1
                            break
                        elif self.pos + 1 < len(toks) and toks[self.pos + 1][0] == ',' or toks[self.pos + 1][0] == ')':
                            argval += toks[self.pos][0]
                        else:
                            argval += toks[self.pos][0] + ' '
                        self.pos += 1
                    if d.expr(argval):
                        args.append(d.expr(argval))
                self.pos += 1
                if toks[self.pos][0] == ';':
                    ast.append(Node('call', name, args, None))
                else:
                    raise SyntaxError('invalid syntax')
            if block == True:
                return (ast[0], self.pos)
            self.pos += 1
            astpos += 1
        return ast
