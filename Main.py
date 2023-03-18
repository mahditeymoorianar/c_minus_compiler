from scanner import Scanner

file_name = 'input.txt'
scanner = Scanner(file_name)
Sym_table = set()
err = False
num_lines = 0
line = ''
f_err = open("lexical_errors.txt", "w")
f_tok = open("tokens.txt", "w")
f_table = open("symbol_table.txt", "w")

while not scanner.EOF:
    token = scanner.get_next_token()
    print(f'Main: {token[0]}')
    if token[0] in ['Unmatched comment', 'Invalid number', 'Unclosed comment', 'Invalid input']:
        f = f_err
        err = True
    else:
        f = f_tok
        Sym_table.add(token[1])
    line += f"({token[0]}, {token[1]})"
    if scanner.EOL:
        line += '\n'
        num_lines += 1
        line = str(num_lines) + '.' + line
        f.write(line)
    else:
        line += ' '

if not err:
    f_err.write('There is no lexical error.')

for i, tok in enumerate(Sym_table):
    f_table.write(f'{i}. {tok}\n')

f_err.close()
f_tok.close()
f_table.close()