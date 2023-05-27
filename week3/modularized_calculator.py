#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def man_mul(line, index, tokens):
    index += 1

    # Get the adjacent number
    mul1 = tokens.pop()

    # Calculate the right after number

    # If the right after letter is '(', get the sub token from '(' to ')',
    # evaluate the sub token, multiply the adjacent number with the evaluated number,
    # and register it to the tokens.
    if (line[index] == '('):
        (mul2, sub_index) = tokenize(line[index:])
        tokens.append({'type': 'NUMBER', 'number': mul1['number'] * evaluate(mul2[0:2])})
        sub_index -= 1

    # Otherwise (if the right after element is number), get the number.
    # multiply the adjacent number with the right after number,
    # and register it to the tokens.
    else:
        (mul2, sub_index) = (read_number(line, index), 1)
        tokens.append({'type': 'NUMBER', 'number': mul1['number'] * mul2[0]['number']})

    # Return updated tokens and updated index.
    return tokens, index + sub_index

def man_div(line, index, tokens):
    index += 1

    # Get the adjacent number
    div1 = tokens.pop()

    # Calculate the right after number

    # If the right after letter is '(', get the sub token from '(' to ')',
    # evaluate the sub token, divide the adjacent number with the evaluated number,
    # and register it to the tokens.
    if (line[index] == '('):
        (div2, sub_index) = tokenize(line[index:])
        tokens.append({'type': 'NUMBER', 'number': div1['number'] / evaluate(div2[0:2])})

    # Otherwise (if the right after element is number), get the number.
    # divide the adjacent number with the right after number,
    # and register it to the tokens.
    else:
        (div2, sub_index) = (read_number(line, index), 1)
        tokens.append({'type': 'NUMBER', 'number': div1['number'] / div2[0]['number']})

    # Return updated tokens and updated index.
    return tokens, index + sub_index

def man_bracket(line, index, tokens):
    index += 1

    # Get the sub tokens from '(' to ')'
    (sub_tokens, sub_index) = tokenize(line[index:])

    # Evaluate the sub tokens
    value_in_brackets = evaluate(sub_tokens)

    # Append the evaluated value in the original tokens as NUMBER
    tokens.append({'type': 'NUMBER', 'number': value_in_brackets})

    # Return updated tokens and updated index
    return tokens, index + sub_index

def tokenize(line):
    tokens = []
    index = 0
    tokens.append({'type': 'PLUS'}) # Insert a dummy '+' token

    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
            tokens.append(token)

        elif line[index] == '+':
            (token, index) = read_plus(line, index)
            tokens.append(token)

        elif line[index] == '-':
            (token, index) = read_minus(line, index)
            tokens.append(token)

        elif line[index] == '*':
            (tokens, index) = man_mul(line, index, tokens)

        elif line[index] == '/':
            (tokens, index) = man_div(line, index, tokens)

        elif line[index] == '(':
            (tokens, index) = man_bracket(line, index, tokens)

        elif line[index] == ')':
            index += 1
            return tokens, index

        else:
            print('Invalid character found: ' + line[index])
            exit(1)
    return tokens, index


def evaluate(tokens):
    answer = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    (tokens,  _) = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1*2")
    test("1+2*3")
    test("1+2+3+4*5*6")
    test("1+2+3*4/5")
    test("3.0+4*2-1/5")
    test("1/2/3")
    test("(1+2)+3")
    test("3/(1+2)")
    test("(3.0+4*(2-1))/5")
    test("(3+3)*(2+3)")
    test("(3+3)/(3*4)")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    (tokens, _) = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)