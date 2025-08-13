"""
Sistema de Moedas Virtuais do CHESS
Gerencia Ouro (gratuito), Gemas (premium), Pontos de Maestria e Tokens
"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json
import asyncio

class CurrencyType(Enum):
    GOLD = "gold"              # Moeda gratuita
    GEMS = "gems"              # Moeda premium
    MASTERY = "mastery"        # Pontos de maestria cultural
    TOKENS = "tokens"          # Tokens de torneio
    SEASONAL = "seasonal"      # Moeda sazonal (eventos)

@dataclass
class Transaction:
    """Representa uma transação de moeda"""
    id: str
    player_id: str
    currency_type: CurrencyType
    amount: int
    balance_before: int
    balance_after: int
    source: str
    description: str
    timestamp: datetime
    metadata: Optional[Dict] = None

class CurrencyManager:
    """Gerenciador central de moedas virtuais"""
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.exchange_rates = {
            # Conversões permitidas (origem -> destino: taxa)
            (CurrencyType.GOLD, CurrencyType.GEMS): 100,  # 100 gold = 1 gem (eventos)
            (CurrencyType.GEMS, CurrencyType.TOKENS): 10,  # 10 gems = 1 token
        }
        self.daily_caps = {
            CurrencyType.GOLD: 5000,    # Máximo de ouro por dia
            CurrencyType.MASTERY: 100,  # Máximo de maestria por dia
        }
        
    async def get_balance(self, player_id: str, currency: CurrencyType) -> int:
        """Retorna o saldo atual de uma moeda"""
        query = """
            SELECT balance FROM player_currencies 
            WHERE player_id = ? AND currency_type = ?
        """
        result = await self.db.fetchone(query, (player_id, currency.value))
        return result['balance'] if result else 0
    
    async def get_all_balances(self, player_id: str) -> Dict[CurrencyType, int]:
        """Retorna todos os saldos do jogador"""
        balances = {}
        for currency in CurrencyType:
            balances[currency] = await self.get_balance(player_id, currency)
        return balances
    
    async def add_currency(
        self,
        player_id: str,
        currency: CurrencyType,
        amount: int,
        source: str,
        description: str,
        check_daily_cap: bool = True
    ) -> Tuple[bool, str, Optional[Transaction]]:
        """
        Adiciona moeda à conta do jogador
        Retorna (sucesso, mensagem, transação)
        """
        if amount <= 0:
            return False, "Quantidade deve ser positiva", None
        
        # Verifica limite diário
        if check_daily_cap and currency in self.daily_caps:
            earned_today = await self._get_daily_earned(player_id, currency)
            if earned_today + amount > self.daily_caps[currency]:
                available = self.daily_caps[currency] - earned_today
                if available <= 0:
                    return False, f"Limite diário de {currency.value} atingido", None
                amount = available  # Ajusta para o máximo permitido
        
        # Realiza a transação
        async with self.db.transaction():
            current_balance = await self.get_balance(player_id, currency)
            new_balance = current_balance + amount
            
            # Atualiza saldo
            await self._update_balance(player_id, currency, new_balance)
            
            # Registra transação
            transaction = await self._record_transaction(
                player_id=player_id,
                currency_type=currency,
                amount=amount,
                balance_before=current_balance,
                balance_after=new_balance,
                source=source,
                description=description
            )
            
            # Eventos e conquistas
            await self._check_currency_milestones(player_id, currency, new_balance)
            
            return True, f"+{amount} {currency.value}", transaction
    
    async def spend_currency(
        self,
        player_id: str,
        currency: CurrencyType,
        amount: int,
        purpose: str,
        description: str,
        allow_negative: bool = False
    ) -> Tuple[bool, str, Optional[Transaction]]:
        """
        Remove moeda da conta do jogador
        Retorna (sucesso, mensagem, transação)
        """
        if amount <= 0:
            return False, "Quantidade deve ser positiva", None
        
        current_balance = await self.get_balance(player_id, currency)
        
        if current_balance < amount and not allow_negative:
            return False, f"Saldo insuficiente de {currency.value}", None
        
        async with self.db.transaction():
            new_balance = current_balance - amount
            
            # Atualiza saldo
            await self._update_balance(player_id, currency, new_balance)
            
            # Registra transação
            transaction = await self._record_transaction(
                player_id=player_id,
                currency_type=currency,
                amount=-amount,
                balance_before=current_balance,
                balance_after=new_balance,
                source=purpose,
                description=description
            )
            
            return True, f"-{amount} {currency.value}", transaction
    
    async def transfer_currency(
        self,
        from_player: str,
        to_player: str,
        currency: CurrencyType,
        amount: int,
        description: str = "Transferência"
    ) -> Tuple[bool, str]:
        """Transfere moeda entre jogadores (se permitido)"""
        # Apenas algumas moedas podem ser transferidas
        if currency not in [CurrencyType.GOLD, CurrencyType.TOKENS]:
            return False, f"{currency.value} não pode ser transferido"
        
        # Taxa de transferência (anti-exploração)
        fee = int(amount * 0.1)  # 10% de taxa
        total_cost = amount + fee
        
        # Verifica saldo
        sender_balance = await self.get_balance(from_player, currency)
        if sender_balance < total_cost:
            return False, "Saldo insuficiente para transferência + taxa"
        
        async with self.db.transaction():
            # Remove do remetente
            await self.spend_currency(
                from_player, currency, total_cost,
                "transfer_out", f"{description} para {to_player}"
            )
            
            # Adiciona ao destinatário
            await self.add_currency(
                to_player, currency, amount,
                "transfer_in", f"{description} de {from_player}"
            )
            
            # Taxa vai para o sistema
            if fee > 0:
                await self._record_system_fee(from_player, currency, fee)
            
            return True, f"Transferência concluída (taxa: {fee} {currency.value})"
    
    async def exchange_currency(
        self,
        player_id: str,
        from_currency: CurrencyType,
        to_currency: CurrencyType,
        amount: int
    ) -> Tuple[bool, str]:
        """Troca moedas usando taxas de câmbio definidas"""
        exchange_key = (from_currency, to_currency)
        
        if exchange_key not in self.exchange_rates:
            return False, "Conversão não permitida"
        
        rate = self.exchange_rates[exchange_key]
        cost = amount * rate
        
        # Verifica saldo
        balance = await self.get_balance(player_id, from_currency)
        if balance < cost:
            return False, f"Necessário {cost} {from_currency.value}"
        
        async with self.db.transaction():
            # Remove moeda origem
            await self.spend_currency(
                player_id, from_currency, cost,
                "exchange", f"Conversão para {to_currency.value}"
            )
            
            # Adiciona moeda destino
            await self.add_currency(
                player_id, to_currency, amount,
                "exchange", f"Conversão de {from_currency.value}",
                check_daily_cap=False  # Conversões ignoram cap diário
            )
            
            return True, f"Convertido {cost} {from_currency.value} → {amount} {to_currency.value}"
    
    async def grant_daily_rewards(self, player_id: str, streak: int) -> Dict[CurrencyType, int]:
        """Concede recompensas diárias baseadas em sequência de login"""
        rewards = {}
        
        # Ouro base + bônus por sequência
        gold_amount = 50 + (streak * 10)
        gold_amount = min(gold_amount, 500)  # Máximo 500
        rewards[CurrencyType.GOLD] = gold_amount
        
        # Gemas em dias especiais
        if streak % 7 == 0:  # A cada 7 dias
            rewards[CurrencyType.GEMS] = 50
        elif streak % 3 == 0:  # A cada 3 dias
            rewards[CurrencyType.GEMS] = 10
        
        # Tokens semanais
        if streak % 7 == 0:
            rewards[CurrencyType.TOKENS] = 3
        
        # Concede todas as recompensas
        for currency, amount in rewards.items():
            await self.add_currency(
                player_id, currency, amount,
                "daily_reward", f"Recompensa diária (streak: {streak})"
            )
        
        return rewards
    
    async def _update_balance(self, player_id: str, currency: CurrencyType, new_balance: int):
        """Atualiza o saldo no banco de dados"""
        query = """
            INSERT INTO player_currencies (player_id, currency_type, balance, last_updated)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(player_id, currency_type) 
            DO UPDATE SET balance = ?, last_updated = ?
        """
        now = datetime.now()
        await self.db.execute(
            query,
            (player_id, currency.value, new_balance, now, new_balance, now)
        )
    
    async def _record_transaction(self, **kwargs) -> Transaction:
        """Registra uma transação no histórico"""
        transaction = Transaction(**kwargs, timestamp=datetime.now())
        
        query = """
            INSERT INTO currency_transactions 
            (id, player_id, currency_type, amount, balance_before, 
             balance_after, source, description, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        await self.db.execute(
            query,
            (transaction.id, transaction.player_id, transaction.currency_type.value,
             transaction.amount, transaction.balance_before, transaction.balance_after,
             transaction.source, transaction.description, transaction.timestamp,
             json.dumps(transaction.metadata) if transaction.metadata else None)
        )
        
        return transaction
    
    async def _get_daily_earned(self, player_id: str, currency: CurrencyType) -> int:
        """Calcula quanto foi ganho hoje de uma moeda"""
        query = """
            SELECT SUM(amount) as total FROM currency_transactions
            WHERE player_id = ? 
            AND currency_type = ?
            AND amount > 0
            AND DATE(timestamp) = DATE('now')
        """
        result = await self.db.fetchone(query, (player_id, currency.value))
        return result['total'] or 0 if result else 0
    
    async def _check_currency_milestones(self, player_id: str, currency: CurrencyType, balance: int):
        """Verifica marcos de moeda para conquistas"""
        milestones = {
            CurrencyType.GOLD: [1000, 5000, 10000, 50000, 100000],
            CurrencyType.GEMS: [100, 500, 1000, 5000, 10000],
            CurrencyType.MASTERY: [50, 100, 250, 500, 1000]
        }
        
        if currency in milestones:
            for milestone in milestones[currency]:
                if balance >= milestone:
                    await self._trigger_achievement(
                        player_id,
                        f"{currency.value}_collector_{milestone}",
                        f"Acumule {milestone} {currency.value}"
                    )
    
    async def _trigger_achievement(self, player_id: str, achievement_id: str, description: str):
        """Dispara uma conquista (placeholder para sistema real)"""
        # Aqui integraria com o sistema de conquistas
        print(f"Achievement unlocked for {player_id}: {achievement_id} - {description}")
    
    async def _record_system_fee(self, player_id: str, currency: CurrencyType, amount: int):
        """Registra taxas do sistema para análise"""
        # Registra em tabela separada para tracking de economia
        query = """
            INSERT INTO system_fees (player_id, currency_type, amount, timestamp)
            VALUES (?, ?, ?, ?)
        """
        await self.db.execute(query, (player_id, currency.value, amount, datetime.now()))


class CurrencyDisplay:
    """Formatação e exibição de moedas"""
    
    SYMBOLS = {
        CurrencyType.GOLD: "🪙",
        CurrencyType.GEMS: "💎",
        CurrencyType.MASTERY: "⭐",
        CurrencyType.TOKENS: "🎟️",
        CurrencyType.SEASONAL: "🎃"  # Muda por temporada
    }
    
    COLORS = {
        CurrencyType.GOLD: "#FFD700",
        CurrencyType.GEMS: "#B9F2FF",
        CurrencyType.MASTERY: "#FF6B6B",
        CurrencyType.TOKENS: "#4ECDC4",
        CurrencyType.SEASONAL: "#FF6B9D"
    }
    
    @classmethod
    def format_amount(cls, amount: int, currency: CurrencyType) -> str:
        """Formata quantidade de moeda para exibição"""
        symbol = cls.SYMBOLS.get(currency, "")
        
        # Formatação de números grandes
        if amount >= 1_000_000:
            return f"{symbol} {amount/1_000_000:.1f}M"
        elif amount >= 1_000:
            return f"{symbol} {amount/1_000:.1f}K"
        else:
            return f"{symbol} {amount:,}"
    
    @classmethod
    def format_price(cls, prices: Dict[CurrencyType, int]) -> str:
        """Formata preço com múltiplas moedas"""
        parts = []
        for currency, amount in prices.items():
            parts.append(cls.format_amount(amount, currency))
        return " ou ".join(parts)
