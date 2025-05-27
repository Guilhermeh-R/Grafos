from Code.grafo import Grafo
from fluxoMaximo import edmonds_karp

# Criar o grafo
g = Grafo()

g.adicionar_vertice(0, 0, 0)    # Fonte
g.adicionar_vertice(1, 2, 2)    # Intermediário
g.adicionar_vertice(2, 4, 0)    # Destino


# Adiciona arestas com capacidade
g.adicionar_aresta(0, 1, 50)
g.adicionar_aresta(1, 2, 30)
g.adicionar_aresta(0, 2, 20)


# Desenhar o grafo original
g.desenhar()

# Executar o algoritmo de Edmonds-Karp
fluxo_maximo, capacidades_residuais = edmonds_karp(g, 0, 2)

# Exibir resultado
print(f"Fluxo máximo: {fluxo_maximo}")

# Desenhar o grafo residual com fluxos
g.desenhar_com_residual(capacidades_residuais, origem=0, destino=2)
