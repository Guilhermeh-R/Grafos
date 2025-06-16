import time
import tkinter as tk
from tkinter import messagebox
from grafo import Grafo

grafo, origem, destino = Grafo.gerar_grafo_direcionado(2, 1)
root = tk.Tk()
root.title("Fluxo de Abastecimento")
root.geometry("500x500")

label_titulo = tk.Label(root, text="Fluxo de Abastecimento - Escolha uma opção:", font=("Arial", 14))
label_titulo.pack(pady=10)

frame_info = tk.Frame(root)
label_origem = tk.Label(frame_info, text=f"Origem: {origem}", font=("Arial", 12))
label_destino = tk.Label(frame_info, text=f"Destino: {destino}", font=("Arial", 12))
label_origem.pack(pady=5)
label_destino.pack(pady=5)
frame_info.pack()

def exibir_grafo():
    grafo.exibir_grafo()

def exibir_fluxo():
    grafo.exibir_fluxo_maximo(origem, destino)

def calcular_fluxo():
    tempo_inicio = time.time()
    fluxoValor, _ = grafo.fluxo_maximo(grafo, origem, destino)
    tempo_final = time.time()
    duracao = tempo_final - tempo_inicio
    messagebox.showinfo(
        "Fluxo Máximo",
        f"Fluxo máximo de '{origem}' para '{destino}': {fluxoValor} m³/dia\n"
        f"Tempo de execução: {duracao:.6f} segundos"
    )

def sugerir_cano():
    grafo.exibir_fluxo_e_gargalo(origem, destino)

def sair():
    root.destroy()

def gerar_novo_grafo():
    global grafo, origem, destino
    try:
        n = int(entry_vertices.get())
        m = int(entry_arestas.get())
        tempo_inicio = time.time()
        grafo, origem, destino = Grafo.gerar_grafo_direcionado(n, m)
        tempo_final = time.time()
        duracao = tempo_final - tempo_inicio
        label_origem.config(text=f"Origem: {origem}")
        label_destino.config(text=f"Destino: {destino}")
        messagebox.showinfo("Novo Grafo", f"Grafo com {n} vértices e {m} arestas gerado com sucesso!\n"
                                            f"Tempo de geração: {duracao:.6f} segundos")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar grafo: {e}")

frame_entrada = tk.Frame(root)
tk.Label(frame_entrada, text="Vértices:").grid(row=0, column=0, padx=5)
entry_vertices = tk.Entry(frame_entrada, width=5)
entry_vertices.insert(0, "")
entry_vertices.grid(row=0, column=1, padx=5)

tk.Label(frame_entrada, text="Arestas:").grid(row=0, column=2, padx=5)
entry_arestas = tk.Entry(frame_entrada, width=5)
entry_arestas.insert(0, "")
entry_arestas.grid(row=0, column=3, padx=5)

botao_gerar = tk.Button(frame_entrada, text="Gerar Grafo", command=gerar_novo_grafo)
botao_gerar.grid(row=0, column=4, padx=10)

frame_entrada.pack(pady=10)

botao_a = tk.Button(root, text="A - Exibir Grafo", width=40, command=exibir_grafo)
botao_b = tk.Button(root, text="B - Calcular Fluxo Máximo", width=40, command=calcular_fluxo)
botao_c = tk.Button(root, text="C - Exibir Fluxo no gráfico", width=40, command=exibir_fluxo)
botao_d = tk.Button(root, text="D - Sugerir Cano para Aumentar Capacidade", width=40, command=sugerir_cano)
botao_e = tk.Button(root, text="Sair", width=40, command=sair)

for botao in [botao_a, botao_b, botao_c, botao_d, botao_e]:
    botao.pack(pady=6)

root.mainloop()
