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
    
    def desenhar_com_residual(self, capacidades, origem=None, destino=None):
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots()

        for aresta in self.arestas:
            v1 = self.vertices[aresta.origem]
            v2 = self.vertices[aresta.destino]

            ax.plot([v1.x, v2.x], [v1.y, v2.y], 'k-')

            # Exibir capacidades residuais
            cap_dir = capacidades.get((aresta.origem, aresta.destino), 0)
            cap_rev = capacidades.get((aresta.destino, aresta.origem), 0)

            mx = (v1.x + v2.x) / 2
            my = (v1.y + v2.y) / 2
            ax.text(mx, my + 0.3, f'{cap_dir}/{aresta.capacidade}', color='blue', fontsize=8)
            ax.text(mx, my - 0.3, f'{cap_rev}', color='red', fontsize=8)

        for v in self.vertices.values():
            ax.plot(v.x, v.y, 'ro')
            label = f"{v.id}"
            if origem is not None and v.id == origem:
                label += " (origem)"
            if destino is not None and v.id == destino:
                label += " (destino)"
            ax.text(v.x + 0.2, v.y, label, fontsize=10, fontweight='bold')

        ax.set_aspect('equal')
        plt.title("Grafo Residual com Fluxos")
        plt.grid(True)
        plt.show()



