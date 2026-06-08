import tkinter as tk
from tkinter import ttk, messagebox
import json
from piloto import Piloto
from avl import AVL

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 2025 - Árvore AVL")
        self.root.geometry("700x500")

        self.arvore = AVL()
        self.carregar_dados()
        self.criar_componentes()

    def carregar_dados(self):
        with open("dados/pilotos_2025.json", encoding="utf-8") as f:
            dados = json.load(f)

        for p in dados:
            self.arvore.inserir_piloto(
                Piloto(p["nome"], p["equipe"], p["pontos"], p["podios"], p["poles"])
            )

    def criar_componentes(self):
        tk.Label(
            self.root,
            text="Classificação Fórmula 1 2025",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Buscar piloto:").pack(side=tk.LEFT)

        self.entrada = tk.Entry(frame, width=30)
        self.entrada.pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Buscar", command=self.buscar_piloto).pack(side=tk.LEFT)

        self.resultado = tk.Label(
            self.root,
            text="Digite o nome de um piloto.",
            font=("Arial", 12),
            justify="left"
        )
        self.resultado.pack(pady=20)

        tk.Button(
            self.root,
            text="Classificação Completa",
            width=30,
            command=self.mostrar_classificacao
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Estrutura e Tamanho da AVL",
            width=30,
            command=self.mostrar_estatisticas
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="Mostrar Árvore Hierárquica",
            width=30,
            command=self.mostrar_arvore
        ).pack(pady=5)

    def buscar_piloto(self):
        piloto = self.arvore.buscar(self.entrada.get())

        if piloto:
            self.resultado.config(
                text=f"Nome: {piloto.nome}\nEquipe: {piloto.equipe}\nPontos: {piloto.pontos}\nPódios: {piloto.podios}\nPole Positions: {piloto.poles}"
            )
        else:
            self.resultado.config(text="Piloto não encontrado.")

    def mostrar_classificacao(self):
        janela = tk.Toplevel(self.root)
        janela.title("Classificação")

        tabela = ttk.Treeview(
            janela,
            columns=("pos", "nome", "equipe", "pontos", "podios", "poles"),
            show="headings"
        )

        for col, txt in [
            ("pos", "Posição"),
            ("nome", "Piloto"),
            ("equipe", "Equipe"),
            ("pontos", "Pontos"),
            ("podios", "Pódios"),
            ("poles", "Pole Positions")
        ]:
            tabela.heading(col, text=txt)

        tabela.pack(fill="both", expand=True)

        for pos, piloto in enumerate(self.arvore.listar_ranking(), start=1):
            tabela.insert("", "end", values=(pos, piloto.nome, piloto.equipe, piloto.pontos, piloto.podios, piloto.poles))

    def mostrar_estatisticas(self):
        messagebox.showinfo(
            "AVL",
            f"Tamanho da árvore: {self.arvore.quantidade_nos(self.arvore.raiz)}\n"
            f"Altura da árvore: {self.arvore.altura(self.arvore.raiz)}"
        )

    def mostrar_arvore(self):
        janela = tk.Toplevel(self.root)
        janela.title("Árvore Hierárquica")

        texto = tk.Text(janela, font=("Courier New", 10))
        texto.pack(fill="both", expand=True)

        linhas = []

        def desenhar(no, prefixo="", ultimo=True):
            if no:
                linhas.append(prefixo + ("└── " if ultimo else "├── ") +
                              f"{no.piloto.nome} ({no.piloto.pontos})")

                filhos = [f for f in [no.esq, no.dir] if f]

                for i, filho in enumerate(filhos):
                    desenhar(
                        filho,
                        prefixo + ("    " if ultimo else "│   "),
                        i == len(filhos) - 1
                    )

        desenhar(self.arvore.raiz)

        texto.insert("1.0", "\n".join(linhas))
        texto.config(state="disabled")

root = tk.Tk()
App(root)
root.mainloop()
