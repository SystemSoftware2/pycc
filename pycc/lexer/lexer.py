'''
Лексер для компилятора ANSI C. Функции:
lex(chars, tokens_regex) - возвращает токены с помощью регулярных выраженией
c_lexer(chars) - возвращает результат функции lex
Пример:
>>> program = 'int main() { int x = 5 }'
>>> print(c_lexer(program))
[('int', 'RESERVED'), ('main', 'ID'), ('(', 'RESERVED'), (')', 'RESERVED'), ...]
>>>
'''

import re

#функция лексинга
def lex(characters, tokens_regex):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag == STRING:
                    text1 = text[1:-1]
                    text = text1.encode().decode('unicode_escape')
                    text = '"' + text + '"'
                    token = (text, tag)
                    tokens.append(token)
                elif tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            raise SyntaxError('Illegal character: %s' % characters[pos])
        else:
            pos = match.end(0)
    return tokens

#теги
RESERVED = 'RESERVED'
ID = 'ID'
INT = 'INT'
STRING = 'STRING'

#регулярные выражения
token_exprs = [
    (r'[ \n\t]+', None),
    (r'//[^\n]*', None),
    (r'\(', RESERVED),
    (r'=', RESERVED),
    (r'while', RESERVED),
    (r'if', RESERVED),
    (r'do', RESERVED),
    (r'void', RESERVED),
    (r'else', RESERVED),
    (r'\{', RESERVED),
    (r'int', RESERVED),
    (r'\}', RESERVED),
    (r'\)', RESERVED),
    (r';', RESERVED),
    (r'\+', RESERVED),
    (r'-', RESERVED),
    (r'\*', RESERVED),
    (r'/', RESERVED),
    (r'<=', RESERVED),
    (r'<', RESERVED),
    (r'>=', RESERVED),
    (r'>', RESERVED),
    (r'!=', RESERVED),
    (r'==', RESERVED),
    (r',', RESERVED),
    (r'"(\\.|[^"\\])*"', STRING),
    (r'[0-9]+', INT),
    (r'[a-zA-Z][a-zA-Z0-9_]*', ID)
]

#лексер
def c_lexer(chars):
    return lex(chars, token_exprs)
