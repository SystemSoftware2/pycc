'''
Узёл AST для парсера.
Класс Node - класс для узла.
'''

class Node:
    def __init__(self, name, op1, op2, op3):
        """
        Узёл AST для парсера
        :параметр name: имя узла
        :параметр op1: цифра, идентификатор или условие
        :параметр op2: выражение или блок кода
        :параметр op3: блок кода для необязательных конструкций или do-while
        """
        self.name = name
        self.op1 = op1
        self.op2 = op2
        self.op3 = op3

    def __repr__(self):
        return f'Node("{self.name}", {self.op1}, {self.op2}, {self.op3})'
