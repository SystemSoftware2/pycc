FETCH, STORE, ASTORE, PUSH, POP, ADD, SUB, MUL, DIV, LT, GT, EQ, NOTEQ, JZ, JNZ, JMP, HALT = range(17)

class VirtualMachine:
    def __init__(self):
        built = {}
        eval('5', built)
        self.builtins = built['__builtins__']
    
    def run(self, program):
        env = {'stdout': ' '}
        
        stack = []
        pc = 0
        while True:
            op = program[pc]
            if pc < len(program) - 1:
                arg = program[pc + 1]
            
            if op == FETCH:
                try:
                    if env[arg]:
                        stack.append(env[arg])
                    else:
                        stack.append(0)
                except:
                    stack.append(0)
                pc += 2
            elif op == STORE:
                if arg in env:
                    value = stack.pop()
                    if type(env[arg]) == type(value):
                        env[arg] = value
                    else:
                        raise ValueError('invalid value of variable')
                else:
                    raise NameError('variable not found')
                pc += 2
            elif op == ASTORE:
                value = stack.pop()
                if type(value) == type(1):
                    env[arg] = value
                elif type(value) == type("1"):
                    env[arg] = value
                else:
                    raise SyntaxError('invalid type of value')
                pc += 2
            elif op == 'int':
                value = stack.pop()
                if type(value) == type(1):
                    env[arg] = value
                else:
                    raise SyntaxError('invalid type of value')
                pc += 2
            elif op == 'char':
                value = stack.pop()
                if type(value) == type("1"):
                    env[arg] = value
                else:
                    raise SyntaxError('invalid type of value')
                pc += 2
            elif op == PUSH:
                stack.append(arg)
                pc += 2
            elif op == ADD:
                stack[-2] += stack[-1]
                stack.pop()
                pc += 1
            elif op == SUB:
                stack[-2] -= stack[-1]
                stack.pop()
                pc += 1
            elif op == MUL:
                stack[-2] *= stack[-1]
                stack.pop()
                pc += 1
            elif op == DIV:
                stack[-2] //= stack[-1]
                stack.pop()
                pc += 1
            elif op == LT:
                if stack[-2] < stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == GT:
                if stack[-2] > stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == EQ:
                if stack[-2] == stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == NOTEQ:
                if stack[-2] != stack[-1]:
                    stack[-2] = 1
                else:
                    stack[-2] = 0
                stack.pop()
                pc += 1
            elif op == POP:
                stack.append(arg)
                stack.pop()
                pc += 1
            elif op == JZ:
                    if stack.pop() == 0:
                          pc = arg
                    else:
                        pc += 2
            elif op == JNZ:
                    if stack.pop() != 0:
                          pc = arg
                    else:
                          pc += 2
            elif op == JMP:
                pc = arg
            elif op == HALT:
                break

        try:
            env['stdout'] = env['stdout'][1:]
        except:
            pass
        print(str(eval(str(env['stdout']), self.builtins | env)).replace('True', '1').replace('False', '0'))
