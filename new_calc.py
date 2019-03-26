import re
import operator

# import time


line = input('Hey! Please input the expression below\n')

# start = time. time()

op_bracket = '('
cl_bracket = ')'

operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}


def find_brackets(line):
    if op_bracket in line:

        def opcnt(line):
            return line.count(op_bracket)

        def clcnt(line):
            return line.count(cl_bracket)

        opind = []

        clind = []

        pairs = []
        i, j = 0, 0

        for k in range(len(line)):
            if line[k] == op_bracket:
                opind.append(k)
            elif line[k] == cl_bracket:
                clind.append(k)
        length = len(opind)
        for i in range(length):
            while j < length:
                if opcnt(line[opind[i]:clind[j] + 1]) == clcnt(line[opind[i]:clind[j] + 1]):
                    pairs.append((opind[i], clind[j]))
                    del clind[j]
                    j = 0
                    break
                j += 1
        pairs.sort(key=lambda pair: pair[1])
        return pairs
    else:
        return []


def calculate(action, num0, num1):
    # checking for (-a-b) situation
    if len(action) > 1:
        action = '' + action[0]
        num1 = -num1
    return operators[action](num0, num1)


def execute(query):
    # return solitary numbers
    if len(re.split('[-+*/]', query)) == 1 or \
            len(re.split('[-+*/]', query)) == 2 \
            and re.split('[-+*/]', query)[0] == '':
        return float(query)
    numbers = re.split('[-+*/]', query)
    actions = re.split('[^-+*/]', query)
    # clearing numbers and actions of ''
    while '' in numbers:
        numbers.remove('')
    for i in range(len(numbers)):
        numbers[i] = float(numbers[i])
    while '' in actions:
        actions.remove('')
    # checking for (-a-b) situation(2)
    if len(numbers) == len(actions):
        numbers[0] = -numbers[0]
        del actions[0]
    # a shortcut for (a?b)-like queries
    if len(numbers) < 3:
        return calculate(actions[0], numbers[0], numbers[1])
    else:
        nums = {}
        acts = {}
        for i in range(len(numbers)):
            nums[i] = nums.get(numbers[i], 0) * 0 + float(numbers[i])

        for i in range(len(actions)):
            acts[i] = acts.get(actions[i], '') + actions[i]
        ind = 0
        # calculating '*' and '/'
        while '*' in acts.values() or '/' in acts.values():
            if acts[ind] == '*' or acts[ind] == '/':
                nums[ind + 1] = calculate(acts[ind], nums[ind], nums[ind + 1])
                del nums[ind]
                del acts[ind]
            ind += 1
        ind = 0
        # calculating '+' and '-'
        nums = list(nums.values())
        acts = list(acts.values())
        while len(acts) > 0:
            nums[ind + 1] = calculate(acts[ind], nums[ind], nums[ind + 1])
            del nums[ind]
            del acts[ind]
            ind = 0
        return nums[ind]


# processing Brackets


def del_brackets(string):
    if op_bracket not in string:
        pass
    else:
        base = (string.strip(op_bracket)).strip(cl_bracket)
        test = re.split('[-+*/]', base)
        if test[0] == '' and len(test) < 3:
            return -float(test[1])
        else:
            return execute(base)


# outputting func


def result(line):
    b = find_brackets(line)
    while len(b) > 0:
        current_pair = b[0]  # current pair of brackets
        pre = line[0:current_pair[0]]
        aft = line[current_pair[1] + 1:len(line)]
        bra = line[current_pair[0]:current_pair[1] + 1]
        bra = str(del_brackets(bra))
        line = pre + bra + aft
        del b[0]
        bra = ''
        if op_bracket in line:
            b = find_brackets(line)
    return execute(line)


print('Result:', result(line))
# end = time.time()
# print('time:',end - start)
