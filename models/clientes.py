class Cliente():
    def __init__(self, id, nome, cpf, email):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.lista_contas = []

    def associar_conta(self, id_conta):
        self.lista_contas.append(id_conta)
        return True

    def trans_dict(self):
        dicionario = {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'email': self.email,
            'lista_contas': self.lista_contas
        }
        return dicionario