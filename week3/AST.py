# token = [
#     {"type": "PLUS"},
#     {"type": "MINUS"},
#     {"type": "TIMES"},
#     {"type": "DIV"},
#     {"type": "NUMBER", "number": __},
#     {"type": "LANGLE"},
#     {"type": "RANGLE"}
# ]

def lexical_analysis(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index] == '+':
      tokens.append({"type": "PLUS"})
      index += 1

    elif line[index] == '-':
      tokens.append({"type": "MINUS"})
      index += 1

    elif line[index] == '*':
      tokens.append({"type": "TIMES"})
      index += 1

    elif line[index] == '/':
      tokens.append({"type": "DIV"})
      index += 1

    elif line[index] == '(':
      tokens.append({"type": "LANGLE"})
      index += 1

    elif line[index] == ')':
      tokens.append({"type": "RANGLE"})
      index += 1

    elif line[index].isdigit():
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
      tokens.append({'type': 'NUMBER', 'number': number})

    else:
      print("Invelid input: ", line[index])
      return None
  return Parse.parser1(tokens)

class Parse:
  def parser1(tokens):
    flag = 0
    for i in range(len(tokens)-1, -1, -1):
      if tokens[i]['type'] == 'RANGLE':
        flag += 1
      elif tokens[i]['type'] == 'LANGLE':
        flag -= 1
      elif tokens[i]['type'] == 'PLUS' and flag == 0:
        return Calculate.Add(Parse.parser1(tokens[:i]), Parse.parser2(tokens[i+1:]))
      elif tokens[i]['type'] == 'MINUS' and flag == 0:
        return Calculate.Sub(Parse.parser1(tokens[:i]), Parse.parser2(tokens[i+1:]))
    return Parse.parser2(tokens)

  def parser2(tokens):
    flag = 0
    for i in range(len(tokens)-1, -1, -1):
      if tokens[i]['type'] == 'RANGLE':
        flag += 1
      elif tokens[i]['type'] == 'LANGLE':
        flag -= 1
      if tokens[i]['type'] == 'TIMES' and flag == 0:
        return Calculate.Mul(Parse.parser2(tokens[:i]), Parse.parser3(tokens[i+1:]))
      elif tokens[i]['type'] == 'DIV' and flag == 0:
        return Calculate.Div(Parse.parser2(tokens[:i]), Parse.parser3(tokens[i+1:]))
    return Parse.parser3(tokens)

  def parser3(tokens):
    if tokens[0]['type'] == 'NUMBER':
      return tokens[0]['number']
    else:
      return Parse.parser1(tokens[1:len(tokens)-1])

class Calculate:
  def Add(e1, e2):
    return e1 + e2
  def Sub(e1, e2):
    return e1 - e2
  def Mul(e1, e2):
    return e1 * e2
  def Div(e1, e2):
    return e1 / e2

test_cases = [
  "1",
  "((1))",
  "1+2",
  "1.0+2.1-3",
  "1*2",
  "1+2*3",
  "1+2+3+4*5*6",
  "1+2+3*4/5",
  "3.0+4*2-1/5",
  "1/2/3",
  "(1+2)+3",
  "3/(1+2)",
  "(3.0+4*(2-1))/5",
  "(3+3)*(2+3)",
  "(3+3)/(3*4)"
]

for i in range(len(test_cases)):
  print(lexical_analysis(test_cases[i]))
