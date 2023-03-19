from scanner import Scanner

file_name = 'input.txt'
scanner = Scanner(file_name)
sym_table = []
err = False
num_lines = 0
line_tok = ''
line_err = ''
f_err = open("lexical_errors.txt", "w")
f_tok = open("tokens.txt", "w")
f_table = open("symbol_table.txt", "w")

while not scanner.EOF:
    token = scanner.get_next_token()
    print('*******************')
    print(f'Main: {token[0]}')
    print(f'Main: {token[1]}')
    print('*******************')
    if token[0] in ['Unmatched comment', 'Invalid number', 'Unclosed comment', 'Invalid input']:
        err = True
        if token[0] == 'Unclosed comment' and len(token[1]) > 7:
            lexeme = f'{token[1][:7]}...'
        else:
            lexeme = token[1]
        line_err += f"({lexeme}, {token[0]}) "
    elif not (token[0] == 'WHITESPACE' or token[0] == 'COMMENT'):
        if token[0] == 'ID' and token[1] not in sym_table:
            sym_table.append(token[1])
        line_tok += f"({token[0]}, {token[1]}) "
    if scanner.EOL or scanner.EOF:
        num_lines += 1
        if line_tok:
            f_tok.write(str(num_lines) + '.\t' + line_tok + '\n')
        if line_err:
            f_err.write(str(num_lines) + '.\t' + line_err + '\n')
        line_tok = ''
        line_err = ''

if not err:
    f_err.write('There is no lexical error.')

for i, tok in enumerate(scanner.keywords):
    f_table.write(f'{i+1}.\t{tok}\n')
length = len(scanner.keywords)
for i, tok in enumerate(sym_table):
    f_table.write(f'{i+length+1}.\t{tok}\n')

f_err.close()
f_tok.close()
f_table.close()
