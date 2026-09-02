# Variáveis
print("1. Atribuição de Variáveis:")
planeta = "Terra"
print(planeta)

# Comparação
print("\n2. Comparação:")
ligado = True
print(ligado)
comprou = not True
print(comprou)
deixou = False
print(comprou == deixou)

#f string
print("\n3. f string:")
animal = "gata"
nome_animal = "Selina"
idade_animal = 2
print(f"Eu tenho um(a) {animal}. O nome dele(a) é {nome_animal} e ele(a) possui {idade_animal} de idade.")

# Tupla
print("\n4. Tupla:")
cores = ("verde", "azul", "amarelo", "vermelho")
print(cores[3])

# Função
print("\n5. Função:")
def blusa(cor, tamanho):
    tipo = f"Quero uma blusa {cor} e do tamanho {tamanho}."
    return tipo
qual = blusa("azul", "G")
print(qual)

# Classe
print("\n6. Classe e Objeto:")
class Pessoa:
    def __init__ (self, nome, idade):
        self.nome = nome
        self.idade = idade
    def ola(self):
        return f"Olá! Eu me chamo {self.nome}, e tenho {self.idade} anos."
    def __endereco(self):
        return "Lugar Nenhum >:)"
perfil_a = Pessoa("João", 20)
perfil_b = Pessoa("Levi", 11)
print(perfil_a.ola())
print(perfil_b.ola())
