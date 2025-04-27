'''
Небольшая реализация препроцессора для компилятора ANSI C.
Директивы:
#include <файл> - вставляет содержимое файла заместо #include <файл>
'''
import os

flag = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/libc/'

def preproc(program):
    for i in program.split('\n'):
        try:
            if i[0:8] == '#include':
                if i.find('<') != -1 and i.find('>') != -1:
                    name = i[i.index('<') + 1:i.index('>')]
                    with open(flag+name, 'r', encoding='utf-8') as f:
                        program = program.replace(i, f.read())
                else:
                    raise SyntaxError('invalid #include directive')
        except IndexError:
            pass
        except FileNotFoundError as err:
            raise err
    return program
