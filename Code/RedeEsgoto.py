import csv
from grafo import Grafo  # Supondo que sua classe esteja em grafo.py

# Inicializa o grafo
g = Grafo()

# Lê o CSV e preenche o grafo
with open('dados.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        origem = row['origem']
        destino = row['destino']
        capacidade = int(row['capacidade'])

        x1, y1 = float(row['x1']), float(row['y1'])
        x2, y2 = float(row['x2']), float(row['y2'])

        # Adiciona vértices se ainda não existirem
        if origem not in g.vertices:
            g.adicionar_vertice(origem, x1, y1)
        if destino not in g.vertices:
            g.adicionar_vertice(destino, x2, y2)

        # Adiciona aresta
        g.adicionar_aresta(origem, destino, capacidade)

# Chama a visualização
g.desenhar()

# Exemplo opcional: grafo com capacidades residuais fictícias
# capacidades_residuais = {
#     ('A', 'B'): 6, ('B', 'A'): 4,
#     ('B', 'C'): 10, ('C', 'B'): 5,
#     ('A', 'C'): 0, ('C', 'A'): 5
# }
# g.desenhar_com_residual(capacidades_residuais, origem='A', destino='C')
