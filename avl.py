class No:
    def __init__(self, piloto):
        self.piloto = piloto
        self.chave = (piloto.pontos, piloto.nome)
        self.esq = None
        self.dir = None
        self.altura = 1


class AVL:
    def __init__(self):
        self.raiz = None

    def altura(self, no):
        return no.altura if no else 0

    def balanceamento(self, no):
        return self.altura(no.esq) - self.altura(no.dir) if no else 0

    def rotacao_direita(self, y):
        x = y.esq
        t2 = x.dir
        x.dir = y
        y.esq = t2
        y.altura = 1 + max(self.altura(y.esq), self.altura(y.dir))
        x.altura = 1 + max(self.altura(x.esq), self.altura(x.dir))
        return x

    def rotacao_esquerda(self, x):
        y = x.dir
        t2 = y.esq
        y.esq = x
        x.dir = t2
        x.altura = 1 + max(self.altura(x.esq), self.altura(x.dir))
        y.altura = 1 + max(self.altura(y.esq), self.altura(y.dir))
        return y

    def inserir(self, raiz, piloto):
        if not raiz:
            return No(piloto)

        chave = (piloto.pontos, piloto.nome)

        if chave < raiz.chave:
            raiz.esq = self.inserir(raiz.esq, piloto)
        else:
            raiz.dir = self.inserir(raiz.dir, piloto)

        raiz.altura = 1 + max(self.altura(raiz.esq), self.altura(raiz.dir))
        balance = self.balanceamento(raiz)

        if balance > 1 and chave < raiz.esq.chave:
            return self.rotacao_direita(raiz)

        if balance < -1 and chave > raiz.dir.chave:
            return self.rotacao_esquerda(raiz)

        if balance > 1 and chave > raiz.esq.chave:
            raiz.esq = self.rotacao_esquerda(raiz.esq)
            return self.rotacao_direita(raiz)

        if balance < -1 and chave < raiz.dir.chave:
            raiz.dir = self.rotacao_direita(raiz.dir)
            return self.rotacao_esquerda(raiz)

        return raiz

    def inserir_piloto(self, piloto):
        self.raiz = self.inserir(self.raiz, piloto)

    def ranking_decrescente(self, no, resultado):
        if no:
            self.ranking_decrescente(no.dir, resultado)
            resultado.append(no.piloto)
            self.ranking_decrescente(no.esq, resultado)

    def listar_ranking(self):
        resultado = []
        self.ranking_decrescente(self.raiz, resultado)
        return resultado

    def buscar_nome(self, no, nome):
        if not no:
            return None

        if no.piloto.nome.lower() == nome.lower():
            return no.piloto

        encontrado = self.buscar_nome(no.esq, nome)
        if encontrado:
            return encontrado

        return self.buscar_nome(no.dir, nome)

    def buscar(self, nome):
        return self.buscar_nome(self.raiz, nome)

    def quantidade_nos(self, no):
        if not no:
            return 0
        return 1 + self.quantidade_nos(no.esq) + self.quantidade_nos(no.dir)
