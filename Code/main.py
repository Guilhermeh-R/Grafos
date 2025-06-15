import tkinter as tk
from tkinter import messagebox
from grafo import Grafo
import random

# Inicialmente gera um grafo
grafo, origem, destino = Grafo.gerar_grafo_direcionado(5, 10)

# Interface Visual
root = tk.Tk()
root.title("Fluxo de Abastecimento")
root.geometry("500x500")

# Título
label_titulo = tk.Label(root, text="Fluxo de Abastecimento - Escolha uma opção:", font=("Arial", 14))
label_titulo.pack(pady=10)

# Frame de informações de origem e destino
frame_info = tk.Frame(root)
label_origem = tk.Label(frame_info, text=f"Origem: {origem}", font=("Arial", 12))
label_destino = tk.Label(frame_info, text=f"Destino: {destino}", font=("Arial", 12))
label_origem.pack(pady=5)
label_destino.pack(pady=5)
frame_info.pack()

# Funções
def exibir_grafo():
    grafo.exibir_grafo()

def calcular_fluxo():
    fluxoValor, _ = grafo.calcular_fluxo_maximo(origem, destino)
    grafo.exibir_fluxo_maximo(origem, destino)
    messagebox.showinfo("Fluxo Máximo", f"Fluxo máximo de '{origem}' para '{destino}': {fluxoValor} m³/dia")

def sugerir_cano():
    grafo.exibir_fluxo_e_gargalo(origem, destino)

def sair():
    root.destroy()

def gerar_novo_grafo():
    global grafo, origem, destino
    try:
        n = int(entry_vertices.get())
        m = int(entry_arestas.get())
        grafo, origem, destino = Grafo.gerar_grafo_direcionado(n, m)
        label_origem.config(text=f"Origem: {origem}")
        label_destino.config(text=f"Destino: {destino}")
        messagebox.showinfo("Novo Grafo", f"Grafo com {n} vértices e {m} arestas gerado com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar grafo: {e}")

# Frame para inserir n e m
frame_entrada = tk.Frame(root)
tk.Label(frame_entrada, text="Vértices:").grid(row=0, column=0, padx=5)
entry_vertices = tk.Entry(frame_entrada, width=5)
entry_vertices.insert(0, "5")
entry_vertices.grid(row=0, column=1, padx=5)

tk.Label(frame_entrada, text="Arestas:").grid(row=0, column=2, padx=5)
entry_arestas = tk.Entry(frame_entrada, width=5)
entry_arestas.insert(0, "10")
entry_arestas.grid(row=0, column=3, padx=5)

botao_gerar = tk.Button(frame_entrada, text="Gerar Novo Grafo", command=gerar_novo_grafo)
botao_gerar.grid(row=0, column=4, padx=10)

frame_entrada.pack(pady=10)

# Botões de ações
botao_a = tk.Button(root, text="A - Exibir Grafo", width=40, command=exibir_grafo)
botao_b = tk.Button(root, text="B - Calcular Fluxo Máximo", width=40, command=calcular_fluxo)
botao_d = tk.Button(root, text="D - Sugerir Cano para Aumentar Capacidade", width=40, command=sugerir_cano)
botao_e = tk.Button(root, text="Sair", width=40, command=sair)

for botao in [botao_a, botao_b, botao_d, botao_e]:
    botao.pack(pady=6)

# Inicia interface
root.mainloop()
