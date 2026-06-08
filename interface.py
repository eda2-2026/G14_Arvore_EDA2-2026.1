import tkinter as tk
from tkinter import ttk, messagebox
import json

from piloto import Piloto
from avl import AVL


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Classificação F1 2025 - AVL")
        self.root.geometry("900x600")

        self.arvore = AVL()
        self.carregar_dados()

        self.criar_componentes()
        self.carregar_ranking()

    def carregar_dados(self):
        with open("dados/pilotos_2025.json", encoding="utf-8") as f:
            dados = json.load(f)

        for p in dados:
            piloto = Piloto(
                p["nome"],
                p["equipe"],
                p["pontos"]
            )

            self.arvore.inserir_piloto(piloto)

    def criar_componentes(self):

        titulo = tk.Label(
            self.root,
            text="Classificação Fórmula 1 2025",
            font=("Arial", 18, "bold")
        )
        titulo.pack(pady=10)

        frame_busca = tk.Frame(self.root)
        frame_busca.pack(pady=10)

        tk.Label(
            frame_busca,
            text="Buscar piloto:"
        ).pack(side=tk.LEFT)

        self.entrada_nome = tk.Entry(frame_busca, width=30)
        self.entrada_nome.pack(side=tk.LEFT, padx=5)

        tk.Button(
            frame_busca,
            text="Buscar",
            command=self.buscar_piloto
        ).pack(side=tk.LEFT)

        tk.Button(
            frame_busca,
            text="Estatísticas AVL",
            command=self.mostrar_estatisticas
        ).pack(side=tk.LEFT, padx=10)

        self.tabela = ttk.Treeview(
            self.root,
            columns=("pos", "nome", "equipe", "pontos"),
            show="headings"
        )

        self.tabela.heading("pos", text="Posição")
        self.tabela.heading("nome", text="Piloto")
        self.tabela.heading("equipe", text="Equipe")
        self.tabela.heading("pontos", text="Pontos")

        self.tabela.column("pos", width=80, anchor="center")
        self.tabela.column("nome", width=250)
        self.tabela.column("equipe", width=200)
        self.tabela.column("pontos", width=100, anchor="center")

        self.tabela.pack(fill="both", expand=True, padx=10, pady=10)

    def carregar_ranking(self):

        ranking = self.arvore.listar_ranking()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for posicao, piloto in enumerate(ranking, start=1):

            self.tabela.insert(
                "",
                "end",
                values=(
                    posicao,
                    piloto.nome,
                    piloto.equipe,
                    piloto.pontos
                )
            )

    def buscar_piloto(self):

        nome = self.entrada_nome.get()

        piloto = self.arvore.buscar(nome)

        if piloto:

            messagebox.showinfo(
                "Piloto Encontrado",
                f"Nome: {piloto.nome}\n"
                f"Equipe: {piloto.equipe}\n"
                f"Pontos: {piloto.pontos}"
            )

        else:

            messagebox.showwarning(
                "Busca",
                "Piloto não encontrado."
            )

    def mostrar_estatisticas(self):

        quantidade = self.arvore.quantidade_nos(
            self.arvore.raiz
        )

        altura = self.arvore.altura(
            self.arvore.raiz
        )

        messagebox.showinfo(
            "Estatísticas AVL",
            f"Quantidade de pilotos: {quantidade}\n"
            f"Altura da AVL: {altura}"
        )


root = tk.Tk()
app = App(root)
root.mainloop()