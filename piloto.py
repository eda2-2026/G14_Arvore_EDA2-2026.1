class Piloto:
    def __init__(self, nome, equipe, pontos):
        self.nome = nome
        self.equipe = equipe
        self.pontos = pontos

    def __str__(self):
        return f"{self.nome} - {self.equipe} - {self.pontos} pts"
