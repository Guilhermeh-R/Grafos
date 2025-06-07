##############################################################################
# grafo.py (somente as partes que mudaram)                                   #
##############################################################################
import math
import matplotlib.pyplot as plt

class Vertice:
    def __init__(self, id, x=0.0, y=0.0):
        self.id = id
        self.x_real = x            # coordenada original (só para registro)
        self.y_real = y
        # coordenadas de desenho poderão ser atribuídas depois
        self.x_draw = None
        self.y_draw = None

class Aresta:                     #  ← Faltava esta classe
    def __init__(self, origem, destino, capacidade):
        self.origem     = origem
        self.destino    = destino
        self.capacidade = capacidade
        self.fluxo      = 0       # opcional, se precisar de fluxo


class Grafo:
    def __init__(self):
        self.vertices = {}         # id -> Vertice
        self.arestas  = []         # lista de Aresta

    def adicionar_vertice(self, id, x=0.0, y=0.0):
        self.vertices[id] = Vertice(id, x, y)

    def adicionar_aresta(self, origem, destino, capacidade):
        self.arestas.append(Aresta(origem, destino, capacidade))

    # --------------------------------------------------------------------- #
    # Novo desenho ABSTRATO: ignora as coordenadas originais.               #
    # Coloca os vértices igualmente espaçados num círculo.                  #
    # --------------------------------------------------------------------- #
    def desenhar(self):
        if not self.vertices:
            print("Grafo vazio.")
            return

        # layout em círculo
        n   = len(self.vertices)
        ids = list(self.vertices.keys())
        raio = 10                               # raio arbitrário

        for i, vid in enumerate(ids):
            ang               = 2 * math.pi * i / n
            self.vertices[vid].x_draw = raio * math.cos(ang)
            self.vertices[vid].y_draw = raio * math.sin(ang)

        # ----- plota -----
        fig, ax = plt.subplots(figsize=(7, 7))

        # arestas
        for ar in self.arestas:
            if ar.origem not in self.vertices or ar.destino not in self.vertices:
                print(f"Vértice ausente: {ar.origem} ou {ar.destino}")
                continue
            v1, v2 = self.vertices[ar.origem], self.vertices[ar.destino]
            ax.plot([v1.x_draw, v2.x_draw], [v1.y_draw, v2.y_draw], 'k-', lw=0.7)

        # vértices
        for v in self.vertices.values():
            ax.plot(v.x_draw, v.y_draw, 'ro', ms=4)
            ax.text(v.x_draw + 0.3, v.y_draw + 0.3, str(v.id), fontsize=8)

        ax.set_aspect('equal', 'box')
        ax.set_axis_off()
        plt.title("Grafo abstrato (coordenadas reais só para deduplicação)")
        plt.show()
