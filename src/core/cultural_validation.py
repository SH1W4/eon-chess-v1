from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import logging
import json
import asyncio

from .cultural_patterns import CulturalPattern, CulturalContext

logger = logging.getLogger(__name__)

@dataclass
class ValidationRule:
    """Regra de validação para padrões culturais."""
    name: str
    description: str
    validation_fn: callable
    severity: str  # 'low', 'medium', 'high', 'critical'
    timeout: int  # segundos

@dataclass
class ValidationResult:
    """Resultado de uma validação."""
    rule_name: str
    success: bool
    message: str
    timestamp: datetime
    details: Dict[str, Any]

class CulturalStateValidator:
    """Validador de estado para padrões culturais."""
    
    def __init__(self):
        self.validation_rules: Dict[str, ValidationRule] = {}
        self.validation_history: List[ValidationResult] = []
        
        # Configurações do validador
        self.config = {
            "max_history_size": 1000,
            "validation_interval": 300,  # 5 minutos
            "concurrent_validations": 5,
            "retry_attempts": 3
        }
        
        # Inicializa regras básicas
        self._initialize_basic_rules()
        
    def _initialize_basic_rules(self):
        """Inicializa regras básicas de validação."""
        self.validation_rules = {
            "pattern_integrity": ValidationRule(
                name="pattern_integrity",
                description="Valida integridade estrutural do padrão",
                validation_fn=self._validate_pattern_integrity,
                severity="critical",
                timeout=10
            ),
            "context_coherence": ValidationRule(
                name="context_coherence",
                description="Verifica coerência do contexto cultural",
                validation_fn=self._validate_context_coherence,
                severity="high",
                timeout=15
            ),
            "temporal_consistency": ValidationRule(
                name="temporal_consistency",
                description="Valida consistência temporal dos padrões",
                validation_fn=self._validate_temporal_consistency,
                severity="medium",
                timeout=10
            ),
            "indicator_validity": ValidationRule(
                name="indicator_validity",
                description="Verifica validade dos indicadores",
                validation_fn=self._validate_indicators,
                severity="high",
                timeout=5
            ),
            "pattern_conflict": ValidationRule(
                name="pattern_conflict",
                description="Detecta conflitos entre padrões",
                validation_fn=self._validate_pattern_conflicts,
                severity="medium",
                timeout=20
            )
        }
        
    async def validate_pattern(self, pattern: CulturalPattern) -> List[ValidationResult]:
        """Valida um padrão cultural específico."""
        results = []
        
        try:
            # Executa todas as regras de validação
            for rule in self.validation_rules.values():
                try:
                    async with asyncio.timeout(rule.timeout):
                        result = await rule.validation_fn(pattern)
                        results.append(result)
                        
                        # Registra resultado no histórico
                        self.validation_history.append(result)
                        
                except asyncio.TimeoutError:
                    result = ValidationResult(
                        rule_name=rule.name,
                        success=False,
                        message=f"Timeout durante validação da regra {rule.name}",
                        timestamp=datetime.now(),
                        details={"error": "timeout", "pattern": pattern.name}
                    )
                    results.append(result)
                    self.validation_history.append(result)
                    
            # Mantém tamanho máximo do histórico
            if len(self.validation_history) > self.config["max_history_size"]:
                self.validation_history = self.validation_history[-self.config["max_history_size"]:]
                
            return results
            
        except Exception as e:
            logger.error(f"Erro durante validação do padrão {pattern.name}: {e}")
            return []
            
    async def validate_context(self, context: CulturalContext) -> List[ValidationResult]:
        """Valida um contexto cultural completo."""
        results = []
        
        try:
            # Valida cada padrão dominante
            for pattern in context.dominant_patterns:
                pattern_results = await self.validate_pattern(pattern)
                results.extend(pattern_results)
                
            # Valida coerência entre padrões
            coherence_result = await self._validate_patterns_coherence(context)
            results.append(coherence_result)
            
            return results
            
        except Exception as e:
            logger.error(f"Erro durante validação do contexto: {e}")
            return []
            
    async def _validate_pattern_integrity(self, pattern: CulturalPattern) -> ValidationResult:
        """Valida integridade estrutural do padrão."""
        try:
            issues = []
            
            # Verifica campos obrigatórios
            if not pattern.name or not isinstance(pattern.name, str):
                issues.append("Nome inválido")
            if not pattern.description or not isinstance(pattern.description, str):
                issues.append("Descrição inválida")
            if not isinstance(pattern.indicators, list):
                issues.append("Indicadores inválidos")
            if not isinstance(pattern.context, dict):
                issues.append("Contexto inválido")
                
            # Verifica ranges válidos
            if not 0 <= pattern.strength <= 1:
                issues.append("Força fora do range válido")
            if not 0 <= pattern.confidence <= 1:
                issues.append("Confiança fora do range válido")
                
            success = len(issues) == 0
            message = "Padrão íntegro" if success else f"Problemas de integridade: {', '.join(issues)}"
            
            return ValidationResult(
                rule_name="pattern_integrity",
                success=success,
                message=message,
                timestamp=datetime.now(),
                details={"issues": issues}
            )
            
        except Exception as e:
            return ValidationResult(
                rule_name="pattern_integrity",
                success=False,
                message=f"Erro ao validar integridade: {e}",
                timestamp=datetime.now(),
                details={"error": str(e)}
            )
            
    async def _validate_context_coherence(self, pattern: CulturalPattern) -> ValidationResult:
        """Verifica coerência do contexto cultural."""
        try:
            issues = []
            
            # Verifica tipos válidos de contexto
            valid_types = {"social", "evolutionary", "behavioral", "cognitive"}
            if pattern.context.get("type") not in valid_types:
                issues.append(f"Tipo de contexto inválido: {pattern.context.get('type')}")
                
            # Verifica escopos válidos
            valid_scopes = {"individual", "group", "system", "network"}
            if pattern.context.get("scope") not in valid_scopes:
                issues.append(f"Escopo de contexto inválido: {pattern.context.get('scope')}")
                
            # Verifica consistência entre indicadores e contexto
            for indicator in pattern.indicators:
                if not self._is_indicator_valid_for_context(indicator, pattern.context):
                    issues.append(f"Indicador {indicator} incompatível com contexto")
                    
            success = len(issues) == 0
            message = "Contexto coerente" if success else f"Problemas de coerência: {', '.join(issues)}"
            
            return ValidationResult(
                rule_name="context_coherence",
                success=success,
                message=message,
                timestamp=datetime.now(),
                details={"issues": issues}
            )
            
        except Exception as e:
            return ValidationResult(
                rule_name="context_coherence",
                success=False,
                message=f"Erro ao validar coerência: {e}",
                timestamp=datetime.now(),
                details={"error": str(e)}
            )
            
    async def _validate_temporal_consistency(self, pattern: CulturalPattern) -> ValidationResult:
        """Valida consistência temporal dos padrões."""
        try:
            issues = []
            
            # Verifica se o padrão não está obsoleto
            age = (datetime.now() - pattern.last_update).total_seconds()
            if age > 3600:  # 1 hora
                issues.append(f"Padrão obsoleto: última atualização há {age/3600:.1f} horas")
                
            # Verifica taxa de mudança da força
            if hasattr(pattern, 'previous_strength'):
                strength_change = abs(pattern.strength - pattern.previous_strength)
                if strength_change > 0.5:  # Mudança máxima permitida
                    issues.append(f"Mudança abrupta na força do padrão: {strength_change:.2f}")
                    
            success = len(issues) == 0
            message = "Consistência temporal OK" if success else f"Problemas temporais: {', '.join(issues)}"
            
            return ValidationResult(
                rule_name="temporal_consistency",
                success=success,
                message=message,
                timestamp=datetime.now(),
                details={"issues": issues, "age": age}
            )
            
        except Exception as e:
            return ValidationResult(
                rule_name="temporal_consistency",
                success=False,
                message=f"Erro ao validar consistência temporal: {e}",
                timestamp=datetime.now(),
                details={"error": str(e)}
            )
            
    async def _validate_indicators(self, pattern: CulturalPattern) -> ValidationResult:
        """Verifica validade dos indicadores."""
        try:
            issues = []
            
            # Verifica quantidade mínima de indicadores
            if len(pattern.indicators) < 2:
                issues.append("Número insuficiente de indicadores")
                
            # Verifica formato dos indicadores
            for indicator in pattern.indicators:
                if not isinstance(indicator, str) or len(indicator) < 3:
                    issues.append(f"Indicador inválido: {indicator}")
                    
            # Verifica duplicatas
            if len(pattern.indicators) != len(set(pattern.indicators)):
                issues.append("Indicadores duplicados detectados")
                
            success = len(issues) == 0
            message = "Indicadores válidos" if success else f"Problemas nos indicadores: {', '.join(issues)}"
            
            return ValidationResult(
                rule_name="indicator_validity",
                success=success,
                message=message,
                timestamp=datetime.now(),
                details={"issues": issues}
            )
            
        except Exception as e:
            return ValidationResult(
                rule_name="indicator_validity",
                success=False,
                message=f"Erro ao validar indicadores: {e}",
                timestamp=datetime.now(),
                details={"error": str(e)}
            )
            
    async def _validate_pattern_conflicts(self, pattern: CulturalPattern) -> ValidationResult:
        """Detecta conflitos entre padrões."""
        try:
            issues = []
            
            # Verifica conflitos de indicadores com outros padrões
            for other in self.get_active_patterns():
                if other.name != pattern.name:
                    conflicts = self._find_indicator_conflicts(pattern, other)
                    if conflicts:
                        issues.append(f"Conflito com padrão {other.name}: {conflicts}")
                        
            # Verifica conflitos de contexto
            context_conflicts = self._find_context_conflicts(pattern)
            if context_conflicts:
                issues.extend(context_conflicts)
                
            success = len(issues) == 0
            message = "Sem conflitos detectados" if success else f"Conflitos encontrados: {', '.join(issues)}"
            
            return ValidationResult(
                rule_name="pattern_conflict",
                success=success,
                message=message,
                timestamp=datetime.now(),
                details={"issues": issues}
            )
            
        except Exception as e:
            return ValidationResult(
                rule_name="pattern_conflict",
                success=False,
                message=f"Erro ao validar conflitos: {e}",
                timestamp=datetime.now(),
                details={"error": str(e)}
            )
            
    async def _validate_patterns_coherence(self, context: CulturalContext) -> ValidationResult:
        """Valida coerência entre múltiplos padrões."""
        try:
            issues = []
            
            # Verifica distribuição de força
            total_strength = sum(p.strength for p in context.dominant_patterns)
            if total_strength > 2.0:  # Limite máximo de força combinada
                issues.append(f"Força total dos padrões muito alta: {total_strength:.2f}")
                
            # Verifica sobreposição de indicadores
            indicator_count = {}
            for pattern in context.dominant_patterns:
                for indicator in pattern.indicators:
                    indicator_count[indicator] = indicator_count.get(indicator, 0) + 1
                    if indicator_count[indicator] > 2:  # Máximo de compartilhamento
                        issues.append(f"Indicador {indicator} muito compartilhado")
                        
            success = len(issues) == 0
            message = "Padrões coerentes" if success else f"Problemas de coerência: {', '.join(issues)}"
            
            return ValidationResult(
                rule_name="patterns_coherence",
                success=success,
                message=message,
                timestamp=datetime.now(),
                details={"issues": issues, "total_strength": total_strength}
            )
            
        except Exception as e:
            return ValidationResult(
                rule_name="patterns_coherence",
                success=False,
                message=f"Erro ao validar coerência entre padrões: {e}",
                timestamp=datetime.now(),
                details={"error": str(e)}
            )
            
    def _is_indicator_valid_for_context(self, indicator: str, context: Dict[str, Any]) -> bool:
        """Verifica se um indicador é válido para um contexto específico."""
        # Mapeamento de indicadores válidos por tipo de contexto
        valid_indicators = {
            "social": {"resource_sharing", "mutual_aid", "collective_decision", "competition"},
            "evolutionary": {"learning_rate", "mutation_frequency", "adaptation_success"},
            "behavioral": {"response_time", "action_pattern", "decision_making"},
            "cognitive": {"processing_speed", "memory_usage", "learning_curve"}
        }
        
        context_type = context.get("type", "")
        if context_type in valid_indicators:
            # Verifica se o indicador ou um prefixo dele está nos indicadores válidos
            return any(indicator.startswith(valid) for valid in valid_indicators[context_type])
        return False
        
    def _find_indicator_conflicts(self, pattern1: CulturalPattern, pattern2: CulturalPattern) -> List[str]:
        """Encontra conflitos entre indicadores de dois padrões."""
        conflicts = []
        
        # Verifica sobreposição de indicadores
        common_indicators = set(pattern1.indicators) & set(pattern2.indicators)
        if common_indicators:
            conflicts.append(f"Indicadores compartilhados: {common_indicators}")
            
        # Verifica combinações incompatíveis
        incompatible_pairs = {
            ("resource_sharing", "resource_competition"),
            ("individual_achievement", "collective_decision"),
            ("mutation_frequency", "stability_index")
        }
        
        for ind1 in pattern1.indicators:
            for ind2 in pattern2.indicators:
                if (ind1, ind2) in incompatible_pairs or (ind2, ind1) in incompatible_pairs:
                    conflicts.append(f"Indicadores incompatíveis: {ind1} e {ind2}")
                    
        return conflicts
        
    def _find_context_conflicts(self, pattern: CulturalPattern) -> List[str]:
        """Encontra conflitos no contexto do padrão."""
        conflicts = []
        
        # Verifica combinações inválidas de tipo e escopo
        invalid_combinations = {
            ("social", "system"),
            ("evolutionary", "individual"),
            ("cognitive", "network")
        }
        
        context_pair = (pattern.context.get("type", ""), pattern.context.get("scope", ""))
        if context_pair in invalid_combinations:
            conflicts.append(f"Combinação inválida de tipo e escopo: {context_pair}")
            
        return conflicts
        
    def get_active_patterns(self) -> List[CulturalPattern]:
        """Retorna lista de padrões ativos no sistema."""
        # Implementação depende da integração com o sistema principal
        return []  # Placeholder
        
    def get_validation_history(self) -> List[ValidationResult]:
        """Retorna histórico de validações."""
        return self.validation_history
        
    def get_validation_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de validação."""
        if not self.validation_history:
            return {
                "total_validations": 0,
                "success_rate": 0.0,
                "failures_by_rule": {}
            }
            
        total = len(self.validation_history)
        successful = sum(1 for v in self.validation_history if v.success)
        
        # Calcula falhas por regra
        failures_by_rule = {}
        for result in self.validation_history:
            if not result.success:
                failures_by_rule[result.rule_name] = failures_by_rule.get(result.rule_name, 0) + 1
                
        return {
            "total_validations": total,
            "success_rate": successful / total,
            "failures_by_rule": failures_by_rule
        }
