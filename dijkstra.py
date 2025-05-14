import tkinter as tk
from tkinter import messagebox, simpledialog

class Grafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_aresta(self, origem, destino, peso):
        if origem not in self.grafo:
            self.grafo[origem] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origem].append((destino, peso))

    def dijkstra(self, inicio):
        distancias = {v: float('inf') for v in self.grafo}
        distancias[inicio] = 0
        caminhos = {v: [] for v in self.grafo}
        caminhos[inicio] = [inicio]
        visitados = set()

        while len(visitados) < len(self.grafo):
            # Seleciona o vértice com menor distância ainda não visitado
            min_vertice = None
            min_distancia = float('inf')
            for v in self.grafo:
                if v not in visitados and distancias[v] < min_distancia:
                    min_vertice = v
                    min_distancia = distancias[v]

            if min_vertice is None:
                break

            visitados.add(min_vertice)

            for vizinho, peso in self.grafo[min_vertice]:
                nova_dist = distancias[min_vertice] + peso
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    caminhos[vizinho] = caminhos[min_vertice] + [vizinho]

        return distancias, caminhos

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Dijkstra")
        self.grafo = Grafo()

        self.frame = tk.Frame(root, padx=10, pady=10)
        self.frame.pack()

        self.lbl = tk.Label(self.frame, text="Adicionar aresta:")
        self.lbl.grid(row=0, column=0, columnspan=2)

        self.btn_adicionar = tk.Button(self.frame, text="Adicionar Aresta", command=self.adicionar_aresta)
        self.btn_adicionar.grid(row=1, column=0, padx=5, pady=5)

        self.btn_calcular = tk.Button(self.frame, text="Executar Dijkstra", command=self.executar_dijkstra)
        self.btn_calcular.grid(row=1, column=1, padx=5, pady=5)

        self.txt_saida = tk.Text(self.frame, width=50, height=15)
        self.txt_saida.grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_aresta(self):
        origem = simpledialog.askstring("Origem", "Digite o vértice de origem:")
        destino = simpledialog.askstring("Destino", "Digite o vértice de destino:")
        try:
            peso = float(simpledialog.askstring("Peso", "Digite o peso da aresta:"))
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Peso inválido.")
            return

        if origem and destino:
            self.grafo.adicionar_aresta(origem, destino, peso)
            self.txt_saida.insert(tk.END, f"Aresta adicionada: {origem} -> {destino} (peso {peso})\n")
        else:
            messagebox.showerror("Erro", "Origem e destino devem ser preenchidos.")

    def executar_dijkstra(self):
        inicio = simpledialog.askstring("Vértice Inicial", "Digite o vértice inicial:")
        if inicio not in self.grafo.grafo:
            messagebox.showerror("Erro", "Vértice inicial inválido ou inexistente.")
            return

        distancias, caminhos = self.grafo.dijkstra(inicio)
        self.txt_saida.insert(tk.END, f"\n--- Resultado a partir de '{inicio}' ---\n")
        for v in distancias:
            caminho_str = " -> ".join(caminhos[v])
            custo = distancias[v]
            self.txt_saida.insert(tk.END, f"Para {v}: Custo = {custo}, Caminho = {caminho_str}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
