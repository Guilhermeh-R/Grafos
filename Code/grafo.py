import matplotlib.pyplot as plt

class Vertice:
    def __init__(self, id, x=0, y=0):
        self.id = id
        self.x = x
        self.y = y

class Aresta:
    def __init__(self, origem, destino, capacidade):
        self.origem = origem
        self.destino = destino
        self.capacidade = capacidade
        self.fluxo = 0

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.arestas = []

    def adicionar_vertice(self, id, x=0, y=0):
        self.vertices[id] = Vertice(id, x, y)

    def adicionar_aresta(self, origem, destino, capacidade):
        self.arestas.append(Aresta(origem, destino, capacidade))

    def desenhar(self):
        fig, ax = plt.subplots()

        for aresta in self.arestas:
            if aresta.origem not in self.vertices or aresta.destino not in self.vertices:
                print(f"Vértice ausente: {aresta.origem} ou {aresta.destino}")
                continue

            v1 = self.vertices[aresta.origem]
            v2 = self.vertices[aresta.destino]
            ax.plot([v1.x, v2.x], [v1.y, v2.y], 'k-')
            mx, my = (v1.x + v2.x) / 2, (v1.y + v2.y) / 2
            ax.text(mx, my, f'{aresta.capacidade}', color='blue', fontsize=8)

        for v in self.vertices.values():
            ax.plot(v.x, v.y, 'ro')
            ax.text(v.x + 0.2, v.y, str(v.id), fontsize=10)

        ax.set_aspect('equal')
        plt.title("Rede de Distribuição de Água - Grafo Exemplo")
        plt.grid(True)
        plt.show()
