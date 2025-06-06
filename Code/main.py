from grafo import Grafo
from fluxoMaximo import edmonds_karp
# from RedeEsgoto import processar_csv
from readcsv import carregar_trechos_do_csv, Trecho

# Criar o grafo
g = Grafo()
# g = processar_csv("C:/Users/thiag/OneDrive/Documentos/GitHub/Grafos/Code/rede.csv")

trechos = carregar_trechos_do_csv("C:/Users/thiag/OneDrive/Documentos/GitHub/Grafos/Code/rede.csv")
for t in trechos:
    print(t)


# g.adicionar_vertice(0, 0, 0)    # Fonte
# g.adicionar_vertice(1, 2, 2)    # Intermediário
# g.adicionar_vertice(2, 4, 0)    # Destino


# Adiciona arestas com capacidade
# g.adicionar_aresta(0, 1, 50)
# g.adicionar_aresta(1, 2, 30)
# g.adicionar_aresta(0, 2, 20)


# Desenhar o grafo original
# g.desenhar()

# Executar o algoritmo de Edmonds-Karp
# fluxo_maximo, capacidades_residuais = edmonds_karp(g, 0, 2)

# Exibir resultado
# print(f"Fluxo máximo: {fluxo_maximo}")

# Desenhar o grafo residual com fluxos
# g.desenhar_com_residual(capacidades_residuais, origem=0, destino=2)
