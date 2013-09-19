#encoding: utf-8

# Jogo campo minado feito em terminal para a aula de Programação de Jogos Digitais
# Fatec Carapicuíba
# Autor: Filipe Gabriel Fagundes
# 14/08/2012 (Data de entrega. Foi uma semana de labuta)


from os import system
from random import randint

import sys
import tty
import termios


def cria_campo():
    for x in range(tamanho):
        campo_lin = []
        for y in range(tamanho):
            campo_lin.append('#')
        campo.append(campo_lin)


class cores:
    HEADER = '\033[105;30;1m'
    OKBLUE = '\033[104;30;1m'
    OKGREEN = '\033[102;91;1m'
    WARNING = '\033[43;30;1m'
    LTWARNING = '\033[103;30;1m'
    FAIL = '\033[41;10;1m'
    LTFAIL = '\033[101;10;1m'
    LTFAIL_T = '\033[101;92;1m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.LTWARNING = ''
        self.FAIL = ''
        self.LTFAIL_T = ''
        self.ENDC = ''


def desenha_campo(is_alive=True):
    system('clear')
    print '\n'
    for num_lin, lin in enumerate(campo):
        print '\t',
        for num_col, col in enumerate(lin):
            if is_alive:

                if (num_col, num_lin) == pos:
                    if type(col) is int:
                        if col == 0:
                            print cores.OKGREEN, ' ', cores.ENDC,
                        else:
                            print cores.OKGREEN, str(col), cores.ENDC,

                    elif col == '$' or col == '%':
                        print cores.OKGREEN, 'F', cores.ENDC,

                    else:
                        print cores.OKGREEN, ' ', cores.ENDC,
                elif type(col) is int:
                    if col == 0:
                        print cores.WARNING, ' ', cores.ENDC,

                    else:
                        print cores.LTWARNING, str(col), cores.ENDC,

                elif col == '$' or col == '%':
                    print cores.LTFAIL, 'F', cores.ENDC,
                else:
                    print cores.OKBLUE, ' ', cores.ENDC,
            else:
                if type(col) is int:
                    if col == 0:
                        print cores.WARNING, ' ', cores.ENDC,
                    else:
                        print cores.LTWARNING, str(col), cores.ENDC,

                elif col == '%':
                    print cores.LTFAIL, 'F', cores.ENDC,

                elif col == '*' or col == '@':
                    print cores.FAIL, str(col), cores.ENDC,

                elif col == '$':
                    print cores.LTFAIL_T, 'F', cores.ENDC,
                else:
                    print cores.OKBLUE, ' ', cores.ENDC,
        print '\n'
    print


def preenche_bombas():
    for num_linha, linha in enumerate(campo):
        for num_coluna, coluna in enumerate(linha):
            random = randint(0, 99)
            if random < dificuldade:
                campo[num_linha][num_coluna] = '*'


def valida_vizinho(linha, coluna, vizinho):
    if vizinho == 't':
        if linha - 1 >= 0:
            return True

    elif vizinho == 'b':
        if linha + 1 < tamanho:
            return True

    elif vizinho == 'r':
        if coluna + 1 < tamanho:
            return True

    elif vizinho == 'l':
        if coluna - 1 >= 0:
            return True

    return False


def procura_bomba(linha, coluna):

    bombas = 0

    if valida_vizinho(linha, coluna, 'r'):
        if campo[linha][coluna + 1] == "*" or campo[linha][coluna + 1] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 'l'):
        if campo[linha][coluna - 1] == "*" or campo[linha][coluna - 1] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 'b'):
        if  campo[linha + 1][coluna] == "*" or campo[linha + 1][coluna] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 't'):
        if campo[linha - 1][coluna] == "*" or campo[linha - 1][coluna] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 'b') and valida_vizinho(linha, coluna, 'r'):
        if  campo[linha + 1][coluna + 1] == "*" or campo[linha + 1][coluna + 1] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 'b') and valida_vizinho(linha, coluna, 'l'):
        if campo[linha + 1][coluna - 1] == "*" or campo[linha + 1][coluna - 1] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 't') and valida_vizinho(linha, coluna, 'r'):
        if campo[linha - 1][coluna + 1] == "*" or campo[linha - 1][coluna + 1] == "$":
            bombas += 1

    if valida_vizinho(linha, coluna, 't') and valida_vizinho(linha, coluna, 'l'):
        if  campo[linha - 1][coluna - 1] == "*" or campo[linha - 1][coluna - 1] == "$":
            bombas += 1

    if campo[linha][coluna] == "*" or campo[linha][coluna] == "$":
        campo[linha][coluna] = "@"
        return "morreu"

    return bombas


def seleciona(linha, coluna, is_mortal=True):
    casa_atual = campo[linha][coluna]
    if casa_atual == '#' or casa_atual == '*' or casa_atual == '%':
        selecao = procura_bomba(linha, coluna)

        if not selecao:
            valid_cel = not is_mortal or (is_mortal and casa_atual != '%')

            if valida_vizinho(linha, coluna, 'r') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha, coluna + 1, False)

            if valida_vizinho(linha, coluna, 'l') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha, coluna - 1, False)

            if valida_vizinho(linha, coluna, 'b') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha + 1, coluna, False)

            if valida_vizinho(linha, coluna, 't') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha - 1, coluna, False)

            if valida_vizinho(linha, coluna, 't') and valida_vizinho(linha, coluna, 'r') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha - 1, coluna + 1, False)

            if valida_vizinho(linha, coluna, 'b') and valida_vizinho(linha, coluna, 'r') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha + 1, coluna + 1, False)

            if valida_vizinho(linha, coluna, 'b') and valida_vizinho(linha, coluna, 'l') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha + 1, coluna - 1, False)

            if valida_vizinho(linha, coluna, 't') and valida_vizinho(linha, coluna, 'l') and valid_cel:
                campo[linha][coluna] = selecao
                seleciona(linha - 1, coluna - 1, False)

        elif selecao == "morreu" and is_mortal:
            return False

        if not is_mortal or (is_mortal and casa_atual != '%'):
            campo[linha][coluna] = selecao

    return True


def valida_vitoria():

    for lin in campo:
        for col in lin:
            if col in ('*', '#', '%'):
                return False

    return True


def move_cursor(tecla, pos):
    # import pdb;pdb.set_trace()

    x, y = pos

    if tecla == 'w':
        y -= 1

    elif tecla == 'a':
        x -= 1

    elif tecla == 's':
        y += 1

    elif tecla == 'd':
        x += 1

    if x < 0:
        x = 0

    if x >= tamanho:
        x = tamanho - 1

    if y < 0:
        y = 0

    if y >= tamanho:
        y = tamanho - 1

    return (x, y)


def set_flag(pos):
    coluna, linha = pos
    if campo[linha][coluna] == '*':
        campo[linha][coluna] = '$'

    elif campo[linha][coluna] == '$':
        campo[linha][coluna] = '*'

    elif campo[linha][coluna] == '%':
        campo[linha][coluna] = '#'

    elif campo[linha][coluna] == '#':
        campo[linha][coluna] = '%'


def legenda():
    print "\n\tW - cima\tS - baixo\tA - esquerda\tD - direita\n\n\tH - seleciona\tJ - bandeira"

if __name__ == '__main__':

    dificuldade = 13
    tamanho = 12
    campo = []
    pos = (0, 0)
    direcional = ['w', 'a', 's', 'd']

    loop = True
    cria_campo()
    preenche_bombas()

    while loop:

        coluna, linha = pos
        desenha_campo()
        legenda()

        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            tecla = sys.stdin.read(1)
            if tecla in direcional:
                pos = move_cursor(tecla, pos)

            elif tecla == 'h':
                if not seleciona(linha, coluna):
                    desenha_campo(False)
                    print '\t' + cores.LTFAIL, 'VOCÊ MORREU!', cores.ENDC + '\n'
                    loop = False

            elif tecla == 'j':
                set_flag(pos)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

        if valida_vitoria():
            desenha_campo(False)
            print '\t' + cores.OKGREEN, 'PARABÉNS! VOCÊ GANHOU!', cores.ENDC + '\n'
            loop = False
