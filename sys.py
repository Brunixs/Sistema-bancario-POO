from abc import ABC, classmethod, property
from datetime import datetime

# Lista de clientes que vão ou estão cadastrados.
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def add_conta(self, conta):
        self.contas.append(conta)

# Pessoa Fisica.
class Pessoa_fisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Conta do cliente.
class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia

    @property 
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
        
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("OPERAÇÃO FALHOU!!!\nVocê Não tem Saldo Suficiente.")
        
        elif valor > 0:
            self.saldo -= valor
            print("Saque Realizado com Sucesso!!!")
            return True

        else:
            return "Operação Falhou! Valor informado é Invalido."
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito Realizado com Sucesso!!.")

        else:
            print("Operação Falhou! O valor informado é inválido.")
            return False
        
        return True

# Conta corrente.
class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == "Saque"]
        )
    
        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação Falhou! o valor de saque excede o limite.")
        elif excedeu_saque:
            print("Operação Falhou! Limite de saque excedido.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}"""

# Historico de Saque/Deposito.
class Historico:

    def __init__(self):
        self.transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes

    def add_transacoes(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__nome__,
                'valor': transacao.valor,
                'data': datetime.now().strftime("%d-%m-%Y %H:%H:%s"),

            }
        )

# Interface de Transação.
class Transacao(ABC):
    @property
    def valor(self):
        pass

    @classmethod
    def registrar(self, conta):
        pass

# mapeamneto do saque.
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacoes(self)

# mapeamneto do deposito.
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.add_transacoes(self)

          