from abc import ABC, abstractmethod

class Conta(ABC):
    def __init__(self, id, id_cliente, saldo):
        self.id = id
        self.id_cliente = id_cliente
        self.saldo = saldo

    @abstractmethod
    def sacar(self):
        pass

    @abstractmethod
    def transferir(self):
        pass

    @abstractmethod
    def retornar_tipo(self):
        pass

    def depositar(self, valor):
        if valor <= 0:
            return 'Erro! O saldo deve ser maior que 0'
        self.saldo += valor
        return f'Sucesso! R$ {valor:.2f} depositado na conta de id {self.id}'

    def trans_dict(self):
        dicionario = { 
            'id': self.id,
            'tipo': self.retornar_tipo(),
            'saldo': self.saldo,
            'cliente': self.id_cliente
        }
        return dicionario

class ContaCorrente(Conta):
    def sacar(self, valor):
        self.saldo -= valor
        return f'Sucesso! R$ {valor:.2f} depositado na conta de id {self.id}'

    def transferir(self, valor, receptor):
        self.saldo -= valor
        receptor.depositar(valor)
        return f'Sucesso! Valor transferido.'

    def retornar_tipo(self):
        return 'Corrente'

class ContaPoupanca(Conta):
    def sacar(self, valor):
        # adiciona verificação para impedir valor negativo
        if self.saldo - valor < 0:
            return f'Erro! Impossível sacar valor acima do saldo da conta.'
        self.saldo -= valor
        return f'Sucesso! Valor de R$ {self.saldo} depositado na conta'

    def transferir(self, valor, receptor):
        # impede valor negativo aqui também
        if self.saldo - valor < 0:
            return f'Erro! Impossível transferir valor acima do saldo da conta.'
        self.saldo -= valor
        receptor.depositar(valor)

    def retornar_tipo(self):
        return 'Poupança'
