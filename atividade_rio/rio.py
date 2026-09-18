"""
Simulação de um ecossistema.

O rio contém:
- Ursos
- Peixes
- Água
- Tocas
- Algas

A cada rodada, os animais podem permanecer parados,
mover-se para a esquerda ou para a direita.

Quando dois animais do mesmo tipo colidem:
- mesma quantidade de vidas: reproduzem;
- quantidade diferente de vidas: o animal com menos vidas
- perde uma e o animal com mais vidas ganha uma.

Quando um Urso e um Peixe colidem:
- o Peixe morre;
- o Urso ocupa a posição do Peixe e ganha uma vida.

Peixes podem entrar em Tocas e comer Algas.
As Algas crescem uma unidade a cada rodada.
"""

# Números randomicos
from random import randint
# Classes abstratas
from abc import ABC, abstractmethod

# Rio
class Rio:
    def __init__(self, tamanho=15):
        self.__rio = [None] * tamanho
        self.__rodada_atual = 0
        self.__historico = []
        self.__povoar_rio()

    # Criação do rio
    def __povoar_rio(self): 
        self.__posicionar(2, Urso)
        self.__posicionar(5, Peixe)
        self.__posicionar(1, Toca)
        self.__posicionar(2, Alga)
        for i in range(len(self.__rio)):
            if self.__posicao_vazia(i):
                self.__rio[i] = Agua()

    # Definição de posições
    def __posicionar(self, quantidade, tipo):
        while quantidade > 0:
            posicao = randint(0, len(self.__rio) - 1)
            if self.__posicao_vazia(posicao):
                self.__rio[posicao] = tipo()
                quantidade -= 1

    # Posições vazias
    def __posicao_vazia(self, posicao):
        return (
            self.__rio[posicao] is None
            or isinstance(self.__rio[posicao], Agua)
        )

    # Funcionamento do programa
    def run(self, rodadas=5):
        for rodada in range(rodadas):
            self.__rodada_atual = rodada + 1
            print(f"\n========== RODADA {self.__rodada_atual} ==========")
            animais = []
            for posicao in range(len(self.__rio)):
                elemento = self.__rio[posicao]
                if isinstance(elemento, Animal):
                    animais.append((posicao, elemento))
            for origem, animal in animais:
                if self.__rio[origem] is not animal:
                    continue
                direcao = animal.mover()
                if direcao == 0:
                    self.__registrar(
                        f"{animal} permaneceu na posição {origem}."
                    )
                    continue
                destino = self.__calc_destino(origem, direcao)
                self.__colisao(origem, destino)
            self.__verificar_saidas_tocas()
            self.__crescer_algas()
            self.__mostrar_rio()

    # Destino
    def __calc_destino(self, origem, direcao):
        destino = origem + direcao
        if destino < 0:
            destino = len(self.__rio) - 1
        elif destino >= len(self.__rio):
            destino = 0
        return destino

    # Colisão
    def __colisao(self, origem, destino):
        obj_origem = self.__rio[origem]
        obj_destino = self.__rio[destino]
        if self.__posicao_vazia(destino):
            self.__rio[destino] = obj_origem
            self.__rio[origem] = Agua()
            self.__registrar(
                f"{obj_origem} moveu-se de {origem} para {destino}."
            )
        elif isinstance(obj_destino, Toca):
            if isinstance(obj_origem, Peixe):
                if not obj_destino.ocupada:
                    obj_destino.entrar(obj_origem)
                    self.__rio[origem] = Agua()
                    self.__registrar(
                        f"{obj_origem} entrou na toca na posição {destino}."
                    )
        elif isinstance(obj_destino, Alga):
            if isinstance(obj_origem, Peixe):
                tamanho = obj_destino.tamanho
                obj_origem.ganha_vidas(tamanho)
                self.__rio[destino] = obj_origem
                self.__rio[origem] = Agua()
                self.__registrar(
                    f"{obj_origem} comeu uma alga de tamanho {tamanho}."
                )
        elif isinstance(obj_destino, Animal):
            if obj_origem.reproduzir(obj_destino):
                if obj_origem.vidas == obj_destino.vidas:
                    self.__reproduzir(obj_origem)
                else:
                    self.__combate_iguais(
                        obj_origem,
                        obj_destino,
                        origem,
                        destino
                    )
            else:
                self.__combate_dif(
                    obj_origem,
                    obj_destino,
                    origem,
                    destino
                )

    # Reprodução dos animais
    def __reproduzir(self, animal):
        if not self.__tem_espaco():
            self.__registrar(
                f"{animal} tentou reproduzir, mas não havia espaço."
            )
            return
        posicao = randint(0, len(self.__rio) - 1)
        while not self.__posicao_vazia(posicao):
            posicao = randint(0, len(self.__rio) - 1)
        novo_animal = type(animal)()
        self.__rio[posicao] = novo_animal
        self.__registrar(
            f"{animal} reproduziu. Novo {novo_animal} nasceu "
            f"na posição {posicao}."
        )

    # Combate (entre animais iguais)
    def __combate_iguais(
        self,
        obj_origem,
        obj_destino,
        origem,
        destino
    ):
        if obj_origem.vidas < obj_destino.vidas:
            obj_origem.perde_vida()
            obj_destino.ganha_vida()
            self.__registrar(
                f"{obj_origem} perdeu uma vida e "
                f"{obj_destino} ganhou uma vida."
            )
            if not obj_origem.esta_vivo():
                self.__rio[origem] = Agua()
                self.__registrar(
                    f"{obj_origem} morreu na posição {origem}."
                )
        else:
            obj_destino.perde_vida()
            obj_origem.ganha_vida()
            self.__registrar(
                f"{obj_destino} perdeu uma vida e "
                f"{obj_origem} ganhou uma vida."
            )
            if not obj_destino.esta_vivo():
                self.__rio[destino] = Agua()
                self.__registrar(
                    f"{obj_destino} morreu na posição {destino}."
                )

    # Cmobate (entre animais diferentes)
    def __combate_dif(
        self,
        obj_origem,
        obj_destino,
        origem,
        destino
    ):
        if (
            isinstance(obj_origem, Peixe)
            and isinstance(obj_destino, Urso)
        ):
            self.__rio[origem] = Agua()
            self.__registrar(
                f"{obj_origem} foi comido pelo Urso."
            )
        elif (
            isinstance(obj_origem, Urso)
            and isinstance(obj_destino, Peixe)
        ):
            self.__rio[origem] = Agua()
            self.__rio[destino] = obj_origem
            obj_origem.ganha_vida()
            self.__registrar(
                f"{obj_origem} comeu {obj_destino} "
                f"e ganhou uma vida."
            )

    # Verificação de lugar com água
    def __tem_espaco(self):
        return any(
            isinstance(elemento, Agua)
            for elemento in self.__rio
        )

    # Verificação de saídas das tocas
    def __verificar_saidas_tocas(self):
        for posicao, elemento in enumerate(self.__rio):
            if not isinstance(elemento, Toca):
                continue
            if not elemento.ocupada:
                continue
            esquerda = (posicao - 1) % len(self.__rio)
            direita = (posicao + 1) % len(self.__rio)
            if isinstance(self.__rio[esquerda], Agua):
                peixe = elemento.sair()
                self.__rio[esquerda] = peixe
                self.__registrar(
                    f"{peixe} saiu da toca pela posição {esquerda}."
                )
            elif isinstance(self.__rio[direita], Agua):
                peixe = elemento.sair()
                self.__rio[direita] = peixe
                self.__registrar(
                    f"{peixe} saiu da toca pela posição {direita}."
                )

    # Algas crescendo
    def __crescer_algas(self):
        for elemento in self.__rio:
            if isinstance(elemento, Alga):
                elemento.cresce()

    # Registro de acontecimentos
    def __registrar(self, mensagem):
        self.__historico.append(
            f"[Rodada {self.__rodada_atual}] {mensagem}"
        )

    # Visualização do registro
    def mostrar_historico(self):
        print("\n========== HISTÓRICO ==========")
        for acao in self.__historico:
            print(acao)

    # Visualização do rio
    def __mostrar_rio(self):
        print(self.__rio)

# Animal (Abstrata)
class Animal(ABC):
    def __init__(self, vidas=3):
        self.vidas = vidas

    def mover(self):
        return randint(-1, 1)

    def ganha_vida(self):
        self.vidas += 1

    def ganha_vidas(self, quantidade):
        self.vidas += quantidade

    def perde_vida(self):
        self.vidas -= 1

    def esta_vivo(self):
        return self.vidas > 0

    @abstractmethod
    def reproduzir(self, other):
        ...

# Urso
class Urso(Animal):
    def reproduzir(self, other):
        return isinstance(other, Urso)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"U({self.vidas})"

# Peixe
class Peixe(Animal):
    def reproduzir(self, other):
        return isinstance(other, Peixe)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"P({self.vidas})"

# NPC (Absttrato)
class NPC(ABC):
    @abstractmethod
    def __str__(self):
        ...

# Água
class Agua(NPC):
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "A"

# Toca
class Toca(NPC):
    def __init__(self):
        self.ocupada = False
        self.peixe = None

    def entrar(self, peixe):
        self.ocupada = True
        self.peixe = peixe

    def sair(self):
        peixe = self.peixe
        self.ocupada = False
        self.peixe = None
        return peixe

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.ocupada:
            return "T(P)"

        return "T"

# Alga
class Alga(NPC):
    def __init__(self, tamanho=1):
        self.tamanho = tamanho

    def cresce(self):
        self.tamanho += 1

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"A{self.tamanho}"

# Execução
if __name__ == "__main__":
    r = Rio()
    r.run(5)
    r.mostrar_historico()