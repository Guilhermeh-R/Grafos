import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import random

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
    def __init__(self, origem, destino, capacidade, distancia):
        self.origem = origem  
        self.distancia = distancia 
        self.destino = destino  
        self.capacidade = capacidade

    def __repr__(self):
        return (f"Aresta({self.origem.nome} -> {self.destino.nome}, "
                f"capacidade={self.capacidade}, distancia={self.distancia})")


class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_vertice(self, nome, x=None, y=None):
        if nome not in self.vertices:
            self.vertices[nome] = Vertice(nome, x, y)
        else:
            vertice = self.vertices[nome]
            if vertice.x is None and x is not None:
                vertice.x = x
            if vertice.y is None and y is not None:
                vertice.y = y
        return self.vertices[nome]

    def adicionar_aresta(self, nome_origem, x_origem, y_origem,
                         nome_destino, x_destino, y_destino,
                         capacidade, distancia):
        origem = self.adicionar_vertice(nome_origem, x_origem, y_origem)
        destino = self.adicionar_vertice(nome_destino, x_destino, y_destino)
        aresta = Aresta(origem, destino, capacidade, distancia)
        origem.adicionar_aresta(aresta)

        

    def gerar_grafo_direcionado(n_vertices, n_arestas, n_sources, n_sinks,
                                capacidade_min=5, capacidade_max=100):
        if n_vertices < (n_sources + n_sinks):
            raise ValueError(f"Precisa de pelo menos {n_sources + n_sinks} vértices para comportar {n_sources} fontes e {n_sinks} sumidouros.")

        max_arestas_sem_bidirecionais = n_sources * (n_vertices - n_sources) + \
                                        (n_vertices - n_sources - n_sinks) * n_sinks + \
                                        ((n_vertices - n_sources - n_sinks) * (n_vertices - 1))
        if n_arestas < (n_vertices - 1):
            raise ValueError("Número de arestas precisa ser no mínimo n-1 para garantir conectividade.")
        if n_arestas > max_arestas_sem_bidirecionais:
            raise ValueError(f"Número de arestas muito alto para este número de vértices/sources/sinks sem duplicatas e loops.")

        grafo = Grafo()

        vertices = []
        usados = set()
        while len(vertices) < n_vertices:
            x, y = random.randint(0, 100), random.randint(0, 100)
            if (x, y) not in usados:
                nome = str(len(vertices))
                grafo.adicionar_vertice(nome, x, y)
                vertices.append(nome)
                usados.add((x, y))

        random.shuffle(vertices)
        fontes = vertices[:n_sources]
        sumidouros = vertices[-n_sinks:]
        intermediarios = vertices[n_sources:n_vertices - n_sinks]

        arestas_usadas = set()

        todos_vizinhos = fontes + intermediarios + sumidouros
        for v in intermediarios:
            possiveis_origens = fontes + [u for u in intermediarios if u != v]
            possiveis_destinos = sumidouros + [u for u in intermediarios if u != v]

            if not possiveis_origens or not possiveis_destinos:
                continue

            origem = random.choice(possiveis_origens)
            destino = random.choice(possiveis_destinos)

            if origem == destino or (origem, destino) in arestas_usadas or (destino, origem) in arestas_usadas:
                continue

            cap = random.choice(range(capacidade_min, capacidade_max + 1, 5))
            dist = random.uniform(1.0, 10.0)
            grafo.adicionar_aresta(origem, grafo.vertices[origem].x, grafo.vertices[origem].y,
                                   destino, grafo.vertices[destino].x, grafo.vertices[destino].y,
                                   cap, dist)
            arestas_usadas.add((origem, destino))

        while len(arestas_usadas) < n_arestas:
            u, v = random.sample(vertices, 2)

            if u == v:
                continue

            if (u, v) in arestas_usadas or (v, u) in arestas_usadas:
                continue

            if v in fontes:
                continue  
            if u in sumidouros:
                continue  

            cap = random.choice(range(capacidade_min, capacidade_max + 1, 5))
            dist = random.uniform(1.0, 10.0)
            grafo.adicionar_aresta(u, grafo.vertices[u].x, grafo.vertices[u].y,
                                v, grafo.vertices[v].x, grafo.vertices[v].y,
                                cap, dist)
            arestas_usadas.add((u, v))


        return grafo, fontes, sumidouros


    def remover_vertice(self, nome_vertice):
        if nome_vertice not in self.vertices:
            raise ValueError(f"Vértice '{nome_vertice}' não encontrado no grafo.")

        for vertice in self.vertices.values():
            vertice.arestas = [a for a in vertice.arestas if a.destino.nome != nome_vertice]

        del self.vertices[nome_vertice]


    def exibir_grafo(self, escala=5, origem=None, destino=None):
        cores = self.gerar_node_colors(origem, destino)
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.DiGraph()

        for vertice in self.vertices.values():
            G.add_node(vertice.nome)

        capacidades = {}
        for vertice in self.vertices.values():
            for aresta in vertice.arestas:
                u = aresta.origem.nome
                v = aresta.destino.nome
                capacidades[(u, v)] = aresta.capacidade
                G.add_edge(u, v)

        edge_labels = {}
        adicionados = set()

        for (u, v), cap_uv in capacidades.items():
            if (v, u) in capacidades and (v, u) not in adicionados:
                cap_vu = capacidades[(v, u)]
                label = f"→ {cap_uv} | {cap_vu} ←"
                edge_labels[(u, v)] = label
                edge_labels[(v, u)] = ""  # Oculta duplicado
                adicionados.add((u, v))
                adicionados.add((v, u))
            elif (u, v) not in adicionados:
                label = f"{cap_uv}"  # Sem setas se for só em um sentido
                edge_labels[(u, v)] = label
                adicionados.add((u, v))

        pos = {
            nome: (v.x * escala, v.y * escala)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color=cores, font_size=10, arrows=True)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=7)

        plt.title("Rede de Distribuição de Água")
        plt.axis('off')
        plt.tight_layout()
        plt.show()
        
    def gerar_node_colors(self, origem=None, destino=None):
        cores = []
        for nome in self.vertices:
            if nome == origem or nome==destino:
                cores.append('green')
            else:
                cores.append('skyblue')
        return cores

    def to_networkx(self): #só pra converter pra um grafo da lib que desenha
      G = nx.DiGraph()
      for vertice in self.vertices.values():
          G.add_node(vertice.nome)
      for vertice in self.vertices.values():
          for aresta in vertice.arestas:
              G.add_edge(
                  aresta.origem.nome,
                  aresta.destino.nome,
                  capacity=aresta.capacidade
              )
      return G
    
    @staticmethod
    def fluxo_maximo(self, s, t):
        residual = defaultdict(dict)
        flow = defaultdict(dict)

        for u in self.vertices.values():
            for v in self.vertices.values():
                residual[u.nome][v.nome] = 0
                flow[u.nome][v.nome] = 0

        for vertice in self.vertices.values():
            for aresta in vertice.arestas:
                u = aresta.origem.nome
                v = aresta.destino.nome
                capacidade = aresta.capacidade
                residual[u][v] = capacidade
                residual[v][u] = 0

                

        def bfs(source, sink, parent):
            visited = set()
            queue = deque([source])
            visited.add(source)

            while queue:
                u = queue.popleft()
                for v in residual[u]:
                    if v not in visited and residual[u][v] > 0:
                        visited.add(v)
                        parent[v] = u
                        if v == sink:
                            return True
                        queue.append(v)
            return False

        max_flow = 0
        parent = {}

        while bfs(s, t, parent):
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, residual[u][v])
                v = u

            v = t
            while v != s:
                u = parent[v]
                residual[u][v] -= path_flow
                residual[v][u] += path_flow
                flow[u][v] += path_flow
                flow[v][u] -= path_flow
                v = u

            max_flow += path_flow
            parent = {}

        flow_dict = {}
        for u in self.vertices:
            flow_dict[u] = {}
            for aresta in self.vertices[u].arestas:
                v = aresta.destino.nome
                flow_dict[u][v] = flow[u][v]

        return max_flow, flow_dict

    def fluxo_maximo_multi(self, fontes, destinos):
        """
        Calcula o fluxo máximo entre múltiplas fontes e múltiplos destinos.
        """
        from copy import deepcopy

        # Clona o grafo atual para não modificar o original
        G = deepcopy(self)

        # Cria dois novos vértices: super origem e super destino
        s_prime = str(max(map(int, G.vertices.keys())) + 1)
        t_prime = str(int(s_prime) + 1)
        G.adicionar_vertice(s_prime, x=0, y=0)
        G.adicionar_vertice(t_prime, x=100, y=100)

        INFINITY = 10**9  # Capacidade muito alta para simular infinito

        # Liga super origem às fontes
        for fonte in fontes:
            G.adicionar_aresta(s_prime, 0, 0, fonte, G.vertices[fonte].x, G.vertices[fonte].y, INFINITY, 0)

        # Liga destinos ao super destino
        for destino in destinos:
            G.adicionar_aresta(destino, G.vertices[destino].x, G.vertices[destino].y, t_prime, 100, 100, INFINITY, 0)

        # Calcula fluxo máximo de s' para t'
        fluxo, fluxo_dict = G.fluxo_maximo(G, s_prime, t_prime)

        return fluxo, fluxo_dict


    def calcular_fluxo_maximo(self, origem, destino):
        fluxo_valor, fluxo_dict = self.fluxo_maximo(self, origem, destino)
        return fluxo_valor, fluxo_dict

    # ------------------------------------------------------------------ #
    # Exibe fluxo; agora aceita str ou lista                             #
    # ------------------------------------------------------------------ #
    def exibir_fluxo_maximo(self, origem, destino):
        # converte para listas se vier string
        origens  = origem  if isinstance(origem,  (list, tuple, set)) else [origem]
        destinos = destino if isinstance(destino, (list, tuple, set)) else [destino]

        # calcula fluxo multi ou simples
        if len(origens) == 1 and len(destinos) == 1:
            fluxo_valor, fluxo_dict = self.fluxo_maximo(origens[0], destinos[0])
        else:
            fluxo_valor, fluxo_dict = self.fluxo_maximo_multi(origens, destinos)

        print(f"Fluxo máximo: {fluxo_valor} m³/dia")

        G = self.to_networkx()                       # grafo para desenho
        pos = {n: (v.x, v.y) for n, v in self.vertices.items() if v.x is not None}

        cores = ["green" if n in origens else
                "orange" if n in destinos else
                "skyblue" for n in self.vertices]

        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=cores)
        nx.draw_networkx_labels(G, pos, font_size=10)

        edge_colors, edge_labels = [], {}
        for u, v, data in G.edges(data=True):
            if u not in self.vertices or v not in self.vertices:
                continue                            # ignora arestas de s', t'
            cap  = int(data["capacity"])
            fluxo = int(fluxo_dict.get(u, {}).get(v, 0))
            edge_colors.append("red" if fluxo else "gray")
            edge_labels[(u, v)] = f"{fluxo}/{cap}"

        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='-|>', arrowsize=15)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color="red")
        plt.title("Fluxo máximo (origens verdes, destinos laranja)")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    # ------------------------------------------------------------------ #
    # Exibe fluxo + gargalo; agora aceita str ou lista                   #
    # ------------------------------------------------------------------ #
    def exibir_fluxo_e_gargalo(self, origem, destino):
        origens  = origem  if isinstance(origem,  (list, tuple, set)) else [origem]
        destinos = destino if isinstance(destino, (list, tuple, set)) else [destino]

        if len(origens) == 1 and len(destinos) == 1:
            fluxo_valor, fluxo_dict = self.fluxo_maximo(origens[0], destinos[0])
        else:
            fluxo_valor, fluxo_dict = self.fluxo_maximo_multi(origens, destinos)

        print(f"💧 Fluxo máximo total: {fluxo_valor} m³/dia")

        G = self.to_networkx()
        pos = {n: (v.x, v.y) for n, v in self.vertices.items() if v.x is not None}

        cores = ["green" if n in origens else
                "orange" if n in destinos else
                "skyblue" for n in self.vertices]

        # identifica gargalos
        gargalos = [(u, v, int(G[u][v]["capacity"]))
                    for u, v in G.edges()
                    if int(fluxo_dict.get(u, {}).get(v, 0)) == int(G[u][v]["capacity"])]
        gargalo_critico = min(gargalos, key=lambda x: x[2]) if gargalos else None

        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color=cores)
        nx.draw_networkx_labels(G, pos, font_size=10)

        edge_labels, cores_ar = {}, []
        for u, v, data in G.edges(data=True):
            if u not in self.vertices or v not in self.vertices:
                continue
            cap  = int(data["capacity"])
            fluxo = int(fluxo_dict.get(u, {}).get(v, 0))
            edge_labels[(u, v)] = f"{fluxo}/{cap}"
            cor = "blue" if gargalo_critico and (u, v) == gargalo_critico[:2] else \
                "red" if fluxo else "gray"
            cores_ar.append(cor)

        nx.draw_networkx_edges(G, pos, edge_color=cores_ar, arrowstyle='-|>', arrowsize=15, width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color="red")

        if gargalo_critico:
            plt.title("Gargalo em azul – considere aumentar a capacidade.")
        else:
            plt.title("Nenhum gargalo detectado.")

        plt.axis("off")
        plt.tight_layout()
        plt.show()

    
    @staticmethod
    def desenhar_rede_residual(self, grafo_original, fluxo_dict):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.DiGraph()
        arestas_originais = set()

        # Marca todas as arestas do grafo original
        for vertice in grafo_original.vertices.values():
            for aresta in vertice.arestas:
                arestas_originais.add((aresta.origem.nome, aresta.destino.nome))

        for vertice in grafo_original.vertices.values():
            for aresta in vertice.arestas:
                u = aresta.origem.nome
                v = aresta.destino.nome
                capacidade = aresta.capacidade
                fluxo = fluxo_dict.get(u, {}).get(v, 0)

                capacidade_residual = capacidade - fluxo

                # Aresta direta residual
                if capacidade_residual > 0:
                    G.add_edge(u, v, capacidade=capacidade, residual=capacidade_residual, cor='green')

                # Aresta reversa (somente se não existir no original)
                if fluxo > 0:
                    if (v, u) not in arestas_originais:
                        G.add_edge(v, u, capacidade=fluxo, residual=fluxo, cor='orange')

        # Posicionamento dos nós
        pos = {
            nome: (v.x, v.y)
            for nome, v in self.vertices.items()
            if v.x is not None and v.y is not None
        }

        edge_colors = [data['cor'] for _, _, data in G.edges(data=True)]
        edge_labels = {
            (u, v): f"{data['residual']}/{data['capacidade']}"
            for u, v, data in G.edges(data=True)
        }

        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightyellow')
        nx.draw_networkx_labels(G, pos, font_size=10)
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='-|>', arrowsize=15, width=2)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

        plt.title("Rede Residual (Capacidade restante / Capacidade total)")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    
    def __repr__(self):
        return '\n'.join(f"{v.nome}: {v.arestas}" for v in self.vertices.values())
