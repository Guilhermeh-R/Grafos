import networkx as nxAdd commentMore actions

import matplotlib.pyplot as plt
class Vertice:
    def __init__(self, nome, x=None, y=None):
        self.nome = nome
        self.x = x
        self.y = y
        self.arestas = []
    def adicionar_aresta(self, aresta):
        self.arestas.append(aresta)
    def __repr__(self):
        return f"Vertice({self.nome}, x={self.x}, y={self.y})"

class Aresta:
    def __init__(self, origem, destino, capacidade, distancia, direcao):
        self.origem = origem  # objeto Vertice
        self.destino = destino  # objeto Vertice
        self.capacidade = capacidade
        self.distancia = distancia
        self.direcao = direcao  # "unidirectional" ou "bidirectional"

    def __repr__(self):
        return (f"Aresta({self.origem.nome} -> {self.destino.nome}, "
                f"capacidade={self.capacidade}, distancia={self.distancia}, direcao={self.direcao})")

class Grafo:
    def __init__(self):
        self.vertices = {}
    def adicionar_vertice(self, nome, x=None, y=None):
        if nome not in self.vertices:
            self.vertices[nome] = Vertice(nome, x, y)
        else:
            # Se já existe, atualiza posição se ainda não foi definida
            vertice = self.vertices[nome]
            if vertice.x is None and x is not None:
                vertice.x = x
            if vertice.y is None and y is not None:
                vertice.y = y
        return self.vertices[nome]

    def adicionar_aresta(self, nome_origem, x_origem, y_origem,
                         nome_destino, x_destino, y_destino,
                         capacidade, distancia, direcao):
        origem = self.adicionar_vertice(nome_origem, x_origem, y_origem)
        destino = self.adicionar_vertice(nome_destino, x_destino, y_destino)

        aresta = Aresta(origem, destino, capacidade, distancia, direcao)
        origem.adicionar_aresta(aresta)

        if direcao == "bidirectional":
            aresta_reversa = Aresta(destino, origem, capacidade, distancia, direcao)
            destino.adicionar_aresta(aresta_reversa)