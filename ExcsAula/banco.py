from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

class ContaBancaria(ABC):
    def __init__(self, titular: str, numero: str, saldo: float = 0.0):
        self._titular = titular
        self._numero = numero
        self._saldo = saldo
        self._historico = []

    @abstractmethod
    def sacar(self, valor: float) -> bool:
        pass

    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            self._historico.append(f"Depósito de R$ {valor:.2f}")
        else:
            print("O valor de depósito precisa ser positivo.")

    def consultar_saldo(self):
        print(f"Saldo atual: R$ {self._saldo:.2f}")

    def registrar_transacao(self, descricao: str):
        self._historico.append(descricao)

    def exibir_historico(self):
        print("Histórico de transações:")
        for transacao in self._historico:
            print(transacao)


class ContaCorrente(ContaBancaria):
    def __init__(self, titular: str, numero: str, saldo: float = 0.0, limite_cheque_especial: float = 500.0):
        super().__init__(titular, numero, saldo)
        self._limite_cheque_especial = limite_cheque_especial

    def sacar(self, valor: float) -> bool:
        if valor <= (self._saldo + self._limite_cheque_especial):
            self._saldo -= valor
            self.registrar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        else:
            print("Saldo insuficiente, incluindo o limite de cheque especial.")
            return False


class ContaPoupanca(ContaBancaria):
    def __init__(self, titular: str, numero: str, saldo: float = 0.0, taxa_rendimento: float = 0.005, limite_saques_diarios: int = 3):
        super().__init__(titular, numero, saldo)
        self._taxa_rendimento = taxa_rendimento
        self._saques_diarios = 0
        self._limite_saques_diarios = limite_saques_diarios

    def sacar(self, valor: float) -> bool:
        if self._saques_diarios >= self._limite_saques_diarios:
            print("Limite de saques diários atingido.")
            return False
        if valor <= self._saldo:
            self._saldo -= valor
            self._saques_diarios += 1
            self.registrar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        else:
            print("Saldo insuficiente.")
            return False

    def aplicar_rendimento(self):
        rendimento = self._saldo * self._taxa_rendimento
        self._saldo += rendimento
        self.registrar_transacao(f"Aplicação de rendimento de R$ {rendimento:.2f}")


@dataclass
class Endereco:
    rua: str
    cidade: str
    estado: str
    cep: str


class Cliente:
    def __init__(self, nome: str, cpf: str):
        self._nome = nome
        self._cpf = cpf
        self._enderecos = []
        self._contas = []

    def adicionar_endereco(self, endereco: Endereco):
        self._enderecos.append(endereco)

    def adicionar_conta(self, conta: ContaBancaria):
        self._contas.append(conta)

    def remover_conta(self, numero_conta: str):
        self._contas = [conta for conta in self._contas if conta._numero != numero_conta]

    def listar_contas(self):
        for conta in self._contas:
            print(f"Conta {conta._numero} - Saldo: R$ {conta._saldo:.2f}")

    def transferir(self, numero_origem: str, numero_destino: str, valor: float):
        conta_origem = next((conta for conta in self._contas if conta._numero == numero_origem), None)
        conta_destino = next((conta for conta in self._contas if conta._numero == numero_destino), None)
        if conta_origem and conta_destino and conta_origem.sacar(valor):
            conta_destino.depositar(valor)
            conta_origem.registrar_transacao(f"Transferência para conta {numero_destino} de R$ {valor:.2f}")
            conta_destino.registrar_transacao(f"Recebimento de transferência da conta {numero_origem} de R$ {valor:.2f}")
        else:
            print("Transferência não realizada. Verifique os dados ou saldo da conta origem.")