import time
import tkinter as tk
from tkinter import messagebox
from grafo import Grafo

root = tk.Tk()
root.title("Fluxo de Abastecimento")
root.geometry("600x600")

label_titulo = tk.Label(root, text="Fluxo de Abastecimento - Escolha uma opção:", font=("Arial", 14))
label_titulo.pack(pady=10)

frame_info = tk.Frame(root)
label_fontes = tk.Label(frame_info, text=f"Fontes: ", font=("Arial", 12))
label_destinos = tk.Label(frame_info, text=f"Destinos: ", font=("Arial", 12))
label_fontes.pack(pady=5)
label_destinos.pack(pady=5)
frame_info.pack()

def exibir_grafo():
    grafo.exibir_grafo()

def exibir_fluxo():
    grafo.exibir_fluxo_maximo(fontes, destinos)

def calcular_fluxo():
    tempo_inicio = time.time()
    fluxoValor, _ = grafo.fluxo_maximo(grafo, fontes, destinos)
    tempo_final = time.time()
    duracao = tempo_final - tempo_inicio
    messagebox.showinfo(
        "Fluxo Máximo",
        f"Fluxo máximo entre todas as fontes e destinos: {fluxoValor} m³/dia\n"
        f"Tempo de execução: {duracao:.6f} segundos"
    )

def sugerir_cano():
    grafo.exibir_fluxo_e_gargalo(fontes, destinos)

def sair():
    root.destroy()

def gerar_novo_grafo():
    global grafo, fontes, destinos
    try:
        n = int(entry_vertices.get())
        m = int(entry_arestas.get())
        n_fontes = int(entry_fontes.get())
        n_destinos = int(entry_destinos.get())

        tempo_inicio = time.time()
        grafo, fontes, destinos = Grafo.gerar_grafo_direcionado(n, m, n_fontes, n_destinos)
        tempo_final = time.time()
        duracao = tempo_final - tempo_inicio

        label_fontes.config(text=f"Fontes: {', '.join(fontes)}")
        label_destinos.config(text=f"Destinos: {', '.join(destinos)}")

        messagebox.showinfo("Novo Grafo", f"Grafo com {n} vértices, {m} arestas, {n_fontes} fontes e {n_destinos} destinos gerado com sucesso!\n"
                                          f"Tempo de geração: {duracao:.6f} segundos")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar grafo: {e}")

frame_entrada = tk.Frame(root)

tk.Label(frame_entrada, text="Vértices:").grid(row=0, column=0, padx=5)
entry_vertices = tk.Entry(frame_entrada, width=5)
entry_vertices.grid(row=0, column=1, padx=5)

tk.Label(frame_entrada, text="Arestas:").grid(row=0, column=2, padx=5)
entry_arestas = tk.Entry(frame_entrada, width=5)
entry_arestas.grid(row=0, column=3, padx=5)

tk.Label(frame_entrada, text="Fontes:").grid(row=1, column=0, padx=5)
entry_fontes = tk.Entry(frame_entrada, width=5)
entry_fontes.grid(row=1, column=1, padx=5)

tk.Label(frame_entrada, text="Destinos:").grid(row=1, column=2, padx=5)
entry_destinos = tk.Entry(frame_entrada, width=5)
entry_destinos.grid(row=1, column=3, padx=5)

botao_gerar = tk.Button(frame_entrada, text="Gerar Grafo", command=gerar_novo_grafo)
botao_gerar.grid(row=0, column=4, rowspan=2, padx=10, sticky="ns")

frame_entrada.pack(pady=10)

botao_a = tk.Button(root, text="A - Exibir Grafo", width=40, command=exibir_grafo)
botao_b = tk.Button(root, text="B - Calcular Fluxo Máximo", width=40, command=calcular_fluxo)
botao_c = tk.Button(root, text="C - Exibir Fluxo no gráfico", width=40, command=exibir_fluxo)
botao_d = tk.Button(root, text="D - Sugerir Cano para Aumentar Capacidade", width=40, command=sugerir_cano)
botao_e = tk.Button(root, text="Sair", width=40, command=sair)

for botao in [botao_a, botao_b, botao_c, botao_d, botao_e]:
    botao.pack(pady=6)

root.mainloop()
