import matplotlib.pyplot as plt


class Vertice:
    def __init__(self, id, x=0, y=0): # X,Y onde ficara o vertice ex: entre (1,2) 
        self.id = id
        self.x = x
        self.y = y


class Aresta:
    def __init__(self, origem, destino, capacidade):
        self.origem = origem
        self.destino = destino
        self.capacidade = capacidade
        self.fluxo = 0  # começa com 0

# Classe principal do grafo
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

        # Desenha arestas
        for aresta in self.arestas:
            v1 = self.vertices[aresta.origem]
            v2 = self.vertices[aresta.destino]
            ax.plot([v1.x, v2.x], [v1.y, v2.y], 'k-') 

            # Capacidade da aresta
            mx, my = (v1.x + v2.x) / 2, (v1.y + v2.y) / 2
            ax.text(mx, my, f'{aresta.capacidade}', color='blue', fontsize=8)

        # Desenha vértices
        for v in self.vertices.values():
            ax.plot(v.x, v.y, 'ro')  
            ax.text(v.x + 0.2, v.y, str(v.id), fontsize=10)

        ax.set_aspect('equal')
        plt.title("Rede de Distribuição de Água - Grafo Exemplo")
        plt.grid(True)
        plt.show()


# =========================
# EXEMPLO DE USO ABAIXO:
# =========================

g = Grafo()

# Adicionando vértices com posições (x, y)
g.adicionar_vertice(0, 0, 0)    # Fonte
g.adicionar_vertice(1, 2, 2)    # Intermediário
g.adicionar_vertice(2, 4, 0)    # Destino

# Adicionando arestas com capacidade
g.adicionar_aresta(0, 1, 50)    # 0 → 1 com capacidade 50
g.adicionar_aresta(1, 2, 30)    # 1 → 2 com capacidade 30
g.adicionar_aresta(0, 2, 20)    # 0 → 2 com capacidade 20

# Desenha o grafo
g.desenhar()
