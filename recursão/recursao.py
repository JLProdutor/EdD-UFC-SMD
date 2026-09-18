import re
import unicodedata


# Exercício 1: Implemente a soma de todos números 0 + 1 + ... + n de modo recursivo.
def fatorial(n):
    # Caso base: se n for 0 ou 1, o resultado é 1
    if n <= 1:
        return 1
    # Caso recursivo: n multiplicado pelo fatorial do antecessor
    return n + fatorial(n - 1)
print("Exercício 1: " + str(fatorial(5)))

# Exercício 2: Implemente uma versão recursiva de uma função que retorna o maior elemento de uma lista.
def maior(l):
    # Se a lista for vazia, retorna None
    if not l:
        return None
    # Se a lista tem apenas um elemento, ele é o maior
    if len(l) == 1:
        return l[0]
    # Recursão: pega o resto da lista
    maior_do_resto = maior(l[1:])
    # Compara o primeiro elemento com o maior do restante
    if l[0] > maior_do_resto:
        return l[0]
    else:
        return maior_do_resto
print("Exercício 2: " + maior(["eae", "saudações", "olá", "hello"]))

# Exercício 3: Implemente, via recursão, uma função que recebe como parâmetro uma string invertido.
def reverso(p):
    # Caso seja uma única letra
    if len(p)<=1:
        return p
    # Recursão: pega o resto da palavra
    else:
        return reverso(p[1:])+p[0]
print("Exercício 3: " + reverso("opa"))

# Exercício 4: Implemente uma função que identifica palíndromos
palavra = 'Socorram-me! Subi no ônibus em Marrocos'
sem_acento = unicodedata.normalize('NFKD', palavra).encode('ASCII', 'ignore').decode('ASCII')
p_palindromo = re.sub(r'[^a-z]', '', sem_acento.lower())
def palindromo(t):
    # Se a string tiver 0 ou 1 caractere, é um palíndromo
    if len(t)<=1:
        return True
    # Se as extremidades forem diferentes, não é um palíndromo
    if t[0] != t[-1]:
        return False
    # Recursão: remove a primeira e a última letra
    return palindromo(t[1:-1])
print(palindromo(p_palindromo))
