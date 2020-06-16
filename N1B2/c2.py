import re

def separarSemString(token):
    # Expressões regulares para validações
    floatPattern = r"^(\+|-)?[0-9]+\.[0-9]+(e(\+|-)?[0-9]+)?$"
    integerPattern = r"^(\+|-)?[0-9]+$"

    lexemas = []
    pascal_keys = ""
    pascal_symbols = ""

    # Fazendo leitura das palavras reservadas da linguagem
    # Convertendo para lower case
    # Tranformando um uma lista apartir de quebras por ' 's
    with open("pascal-keys.txt", "r") as pkeys:
        pascal_keys = pkeys.read().lower().split()

    # Fazendo leitura dos símbolos da linguagem
    # Tranformando um uma lista apartir de quebras por ' 's
    with open("pascal-symbols.txt", "r") as psymbols:
        pascal_symbols = psymbols.read().split()

    # Mantendo apenas 1 espaço antes e depois do '('
    token = re.sub(r"\s*\(\s*", " ( ", token)

    # Mantendo apenas 1 espaço antes e depois do ')'
    token = re.sub(r"\s*\)\s*", " ) ", token)

    # Mantendo apenas 1 espaço antes e depois do ','
    token = re.sub(r"\s*,\s*", " , ", token)

    # Mantendo apenas 1 espaço antes e depois do ';'
    token = re.sub(r"\s*;\s*", " ; ", token)

    for outroToken in token.split():
        if outroToken in pascal_keys:
            print([outroToken, 'keyword'])
            lexemas.append([outroToken, 'keyword'])
        elif re.match(integerPattern, outroToken):
            print([outroToken, 'integer'])
            lexemas.append([outroToken, 'integer'])
        elif re.match(floatPattern, outroToken):
            print([outroToken, 'float'])
            lexemas.append([outroToken, 'float'])
        elif outroToken in pascal_symbols:
            print([outroToken, 'symbol'])
            lexemas.append([outroToken, 'symbol'])
        else:
            print([outroToken, 'variable'])
            lexemas.append([outroToken, 'variable'])

    return lexemas

startStringPattern = r".*\'.*"
endStringPattern = r".*\'.*"

auxStringRead = ""
lexemas = []
pascal_code = ""
isString = False

# Fazendo leitura do código a ser trabalhado
# Convertendo para lower case
# Removendo comentários iniciando com '//'
with open("p1.pas", "r") as pcode:
    # pascal_code = re.sub(r"//.*", "", pcode.read().lower())
    pascal_code = re.sub(r"\s+", " ", pcode.read().lower()).split()

# Tranformando qualquer tipo de espaços, quebras de linha e tabulações em 1 espaço apenas
# pascal_code = re.sub(r"\s+", " ", pascal_code)

# Removendo comentários iniciando com '{' e terminando com '}'
# pascal_code = re.sub(r"\{[^\}.*\{]*\}", "", pascal_code)

# Removendo comentários iniciando com '(*' e terminando com '*)'
# pascal_code = re.sub(r"\(\*[^\*\).*\(\*]*\*\)", "", pascal_code)

for token in pascal_code:
    if isString:
        if re.match(endStringPattern, token):
            aux = re.sub(r"\'", "' ", token).split()
            isString = False
            auxStringRead += aux[0]
            print([auxStringRead.replace("'", ""), 'String'])
            lexemas.append([auxStringRead.replace("'", ""), 'String'])
            lexemasAux = separarSemString(token.replace(aux[0], ""))

            for lex in lexemasAux:
                lexemas.append(lex)
        else:
            auxStringRead += " " + token + " "
    else:
        if re.match(startStringPattern, token):
            aux = re.sub(r"\'", " '", token).split()
            isString = True
            auxStringRead = aux[-1]

            lexemasAux = separarSemString(token.replace(auxStringRead, ""))

            for lex in lexemasAux:
                lexemas.append(lex)
        else:
            lexemasAux = separarSemString(token)

            for lex in lexemasAux:
                lexemas.append(lex)

with open("tokens.txt", "w") as lexemas_file:
    lexemas_file.write(str(lexemas))

# Links utilizados para referência
# http://www.inf.ufpr.br/cursos/ci055/pascal.pdf
