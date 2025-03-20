from dataclasses import dataclass
from datetime import datetime, time
from enum import Enum
from typing import List, Optional

# Tipos de serviço disponíveis
class TipoServico(Enum):
    UBERX = "UberX"      
    UBERXL = "UberXL"    
    UBER_BLACK = "Uber Black"  

# Status que uma viagem pode ter
class StatusViagem(Enum):
    AGUARDANDO = "Aguardando"        
    EM_ANDAMENTO = "Em andamento"    
    FINALIZADA = "Finalizada"        
    CANCELADA = "Cancelada"          

@dataclass
class Cidade:
    nome: str                
    chave: int              
    taxa_base: float        
    taxa_km: dict[TipoServico, float]  # Taxa por km diferente para cada tipo de serviço
    taxa_minuto: float      
    zonas_boost: List['ZonaBoost'] = None  

    def __post_init__(self):
        if self.zonas_boost is None:
            self.zonas_boost = []

@dataclass
class ZonaBoost:
    nome: str              
    multiplicador: float   
    hora_inicio: time      
    hora_fim: time        
    
    def esta_ativo(self, hora_atual: time) -> bool:
        return self.hora_inicio <= hora_atual <= self.hora_fim

class Servico:
    def __init__(self, tipo: TipoServico, multiplicador_taxa: float):
        self.tipo = tipo  
        self.multiplicador_taxa = multiplicador_taxa  # Multiplicador geral do serviço

class PrecosDinamicos:
    def __init__(self):
        self.multiplicador_atual: float = 1.0
        
    # Atualiza preço baseado em demanda/oferta
    def atualizar_multiplicador(self, demanda: float, oferta: float) -> None:
        if oferta == 0:
            self.multiplicador_atual = 3.0  
        else:
            ratio = demanda / oferta
            self.multiplicador_atual = min(max(ratio, 1.0), 3.0)

class Motorista:
    def __init__(self, nome: str, servico: Servico):
        self.nome = nome
        self.servico = servico
        self.saldo = 0.0
        self.viagens_completadas = 0
        self.viagens_consecutivas = 0
        
    def receber_pagamento(self, valor: float) -> None:
        self.saldo += valor
        
    def completar_viagem(self) -> None:
        self.viagens_completadas += 1
        self.viagens_consecutivas += 1
        
    def resetar_viagens_consecutivas(self) -> None:
        self.viagens_consecutivas = 0

class Cliente:
    def __init__(self, nome: str, saldo: float, chave: int, localizacao: Cidade):
        self.nome = nome
        self.saldo = saldo
        self.chave = chave
        self.localizacao = localizacao
        self.historico_viagens: List[Viagem] = []
        
    # Tenta dar gorjeta se tiver saldo suficiente
    def dar_gorjeta(self, gorjeta: float, motorista: Motorista) -> bool:
        if gorjeta > 0 and self.saldo >= gorjeta:
            motorista.receber_pagamento(gorjeta)
            self.saldo -= gorjeta
            return True
        return False
    
    def mudar_localizacao(self, nova_localizacao: Cidade) -> None:
        self.localizacao = nova_localizacao
        
    # Tenta pagar viagem se tiver saldo suficiente
    def pagar_viagem(self, valor: float) -> bool:
        if self.saldo >= valor:
            self.saldo -= valor
            return True
        return False

class Viagem:
    def __init__(self, cliente: Cliente, motorista: Motorista, cidade: Cidade, 
                 precos_dinamicos: PrecosDinamicos):
        self.cliente = cliente
        self.motorista = motorista
        self.cidade = cidade
        self.precos_dinamicos = precos_dinamicos
        self.distancia = 0.0
        self.tempo = 0.0
        self.status = StatusViagem.AGUARDANDO
        self.hora_inicio: Optional[datetime] = None
        self.hora_fim: Optional[datetime] = None
        
    def iniciar_viagem(self) -> None:
        self.status = StatusViagem.EM_ANDAMENTO
        self.hora_inicio = datetime.now()
        
    # Finaliza viagem e processa pagamento
    def finalizar_viagem(self, distancia: float, tempo: float) -> float:
        self.status = StatusViagem.FINALIZADA
        self.hora_fim = datetime.now()
        self.distancia = distancia
        self.tempo = tempo
        
        valor = self.calcular_valor_total()
        
        if self.cliente.pagar_viagem(valor):
            taxa_uber = self.calcular_taxa_servico(valor)
            valor_motorista = valor - taxa_uber
            
            self.motorista.receber_pagamento(valor_motorista)
            self.motorista.completar_viagem()
            
            self.cliente.historico_viagens.append(self)
            
            return valor
        return 0.0
    
    # Processa cancelamento e taxa se aplicável
    def cancelar_viagem(self, tempo_espera: float) -> float:
        self.status = StatusViagem.CANCELADA
        if tempo_espera > 5:  # 5 minutos de tolerância
            taxa_cancelamento = self.cidade.taxa_base * 0.5
            if self.cliente.pagar_viagem(taxa_cancelamento):
                self.motorista.receber_pagamento(taxa_cancelamento * 0.8)
                return taxa_cancelamento
        return 0.0
    
    def calcular_valor_total(self) -> float:
        valor = self.cidade.taxa_base
        
        valor += self.distancia * self.cidade.taxa_km[self.motorista.servico.tipo]
        valor += self.tempo * self.cidade.taxa_minuto
        
        valor *= self.motorista.servico.multiplicador_taxa
        
        valor *= self.precos_dinamicos.multiplicador_atual
        
        if self.hora_inicio:
            for zona in self.cidade.zonas_boost:
                if zona.esta_ativo(self.hora_inicio.time()):
                    valor *= zona.multiplicador
                    break
                    
        return valor
    
    def calcular_taxa_servico(self, valor_total: float, taxa: float = 0.25) -> float:
        return valor_total * taxa

# Sistema de bônus para motoristas
class SistemaBonus:
    @staticmethod
    def calcular_bonus_quest(motorista: Motorista, meta_viagens: int, valor_bonus: float) -> float:
        if motorista.viagens_completadas >= meta_viagens:
            return valor_bonus
        return 0.0
    
    @staticmethod
    def calcular_bonus_consecutivo(motorista: Motorista, min_consecutivas: int, 
                                 valor_por_viagem: float) -> float:
        if motorista.viagens_consecutivas >= min_consecutivas:
            return motorista.viagens_consecutivas * valor_por_viagem
        return 0.0

