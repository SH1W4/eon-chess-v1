from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ValidationRule:
    """Regra de validação para elementos narrativos."""
    name: str
    description: str
    severity: str  # 'high', 'medium', 'low'
    validation_fn: callable
    error_message: str

@dataclass
class ValidationResult:
    """Resultado de uma validação."""
    passed: bool
    rule_name: str
    message: Optional[str] = None
    timestamp: datetime = datetime.now()
    details: Optional[Dict[str, Any]] = None

class NarrativeValidator:
    """Validador para elementos narrativos."""
    
    def __init__(self):
        self.rules: Dict[str, ValidationRule] = {}
        self._initialize_rules()
        
    def _initialize_rules(self):
        """Inicializa regras de validação padrão."""
        self.rules["structure"] = ValidationRule(
            name="structure",
            description="Valida estrutura básica do elemento narrativo",
            severity="high",
            validation_fn=self._validate_structure,
            error_message="Estrutura narrativa inválida"
        )
        
        self.rules["coherence"] = ValidationRule(
            name="coherence",
            description="Verifica coerência narrativa",
            severity="high",
            validation_fn=self._validate_coherence,
            error_message="Incoerência narrativa detectada"
        )
        
        self.rules["complexity"] = ValidationRule(
            name="complexity",
            description="Avalia complexidade do elemento",
            severity="medium",
            validation_fn=self._validate_complexity,
            error_message="Complexidade fora dos limites aceitáveis"
        )
        
        self.rules["temporal"] = ValidationRule(
            name="temporal",
            description="Verifica consistência temporal",
            severity="medium",
            validation_fn=self._validate_temporal,
            error_message="Inconsistência temporal detectada"
        )
        
    async def validate(self, element: Dict[str, Any]) -> List[ValidationResult]:
        """Valida um elemento narrativo."""
        results = []
        
        for rule in self.rules.values():
            try:
                passed, details = await rule.validation_fn(element)
                result = ValidationResult(
                    passed=passed,
                    rule_name=rule.name,
                    message=rule.error_message if not passed else None,
                    details=details
                )
                results.append(result)
            except Exception as e:
                results.append(ValidationResult(
                    passed=False,
                    rule_name=rule.name,
                    message=f"Erro na validação: {str(e)}"
                ))
                
        return results
        
    async def _validate_structure(self, element: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Valida estrutura básica do elemento."""
        required_fields = {"id", "type", "content", "metadata"}
        details = {
            "missing_fields": [],
            "invalid_types": []
        }
        
        # Verifica campos obrigatórios
        for field in required_fields:
            if field not in element:
                details["missing_fields"].append(field)
                
        # Verifica tipos
        if "type" in element and not isinstance(element["type"], str):
            details["invalid_types"].append("type")
        if "content" in element and not isinstance(element["content"], (dict, list)):
            details["invalid_types"].append("content")
        if "metadata" in element and not isinstance(element["metadata"], dict):
            details["invalid_types"].append("metadata")
            
        passed = not (details["missing_fields"] or details["invalid_types"])
        return passed, details
        
    async def _validate_coherence(self, element: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Verifica coerência narrativa."""
        details = {
            "coherence_score": 0.0,
            "issues": []
        }
        
        if "content" not in element:
            return False, details
            
        # Verifica relações internas
        if isinstance(element["content"], dict):
            relations = element["content"].get("relations", [])
            if relations:
                relation_coherence = sum(1 for r in relations if self._is_relation_valid(r))
                details["coherence_score"] = relation_coherence / len(relations)
            
        # Verifica metadados
        if "metadata" in element:
            metadata = element["metadata"]
            if "context" in metadata and "theme" in metadata:
                if not self._is_context_theme_coherent(metadata["context"], metadata["theme"]):
                    details["issues"].append("context_theme_mismatch")
                    
        passed = details["coherence_score"] >= 0.7 and not details["issues"]
        return passed, details
        
    async def _validate_complexity(self, element: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Avalia complexidade do elemento."""
        details = {
            "complexity_score": 0.0,
            "factors": {}
        }
        
        if "content" not in element:
            return False, details
            
        # Analisa profundidade da estrutura
        depth = self._calculate_structure_depth(element["content"])
        details["factors"]["structural_depth"] = min(1.0, depth / 5)
        
        # Analisa relações
        if isinstance(element["content"], dict):
            relations = len(element["content"].get("relations", []))
            details["factors"]["relation_complexity"] = min(1.0, relations / 10)
            
        # Calcula score final
        details["complexity_score"] = sum(details["factors"].values()) / len(details["factors"])
        
        # Complexidade deve estar entre 0.3 e 0.9
        passed = 0.3 <= details["complexity_score"] <= 0.9
        return passed, details
        
    async def _validate_temporal(self, element: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Verifica consistência temporal."""
        details = {
            "temporal_score": 0.0,
            "issues": []
        }
        
        if "metadata" not in element or "timestamp" not in element["metadata"]:
            return False, details
            
        try:
            # Verifica ordem temporal
            current_time = datetime.now()
            element_time = datetime.fromisoformat(element["metadata"]["timestamp"])
            
            if element_time > current_time:
                details["issues"].append("future_timestamp")
            
            # Verifica sequência de eventos
            if "sequence" in element["metadata"]:
                sequence = element["metadata"]["sequence"]
                if not self._is_sequence_valid(sequence):
                    details["issues"].append("invalid_sequence")
                    
            details["temporal_score"] = 1.0 if not details["issues"] else 0.0
            
        except Exception as e:
            details["issues"].append(f"timestamp_error: {str(e)}")
            details["temporal_score"] = 0.0
            
        passed = details["temporal_score"] > 0.8
        return passed, details
        
    def _is_relation_valid(self, relation: Dict[str, Any]) -> bool:
        """Verifica se uma relação é válida."""
        required = {"type", "target", "strength"}
        return all(field in relation for field in required)
        
    def _is_context_theme_coherent(self, context: str, theme: str) -> bool:
        """Verifica coerência entre contexto e tema."""
        # Implementação simplificada
        return bool(context and theme)
        
    def _calculate_structure_depth(self, content: Any, current_depth: int = 0) -> int:
        """Calcula profundidade da estrutura."""
        if not isinstance(content, (dict, list)) or current_depth > 10:
            return current_depth
            
        if isinstance(content, dict):
            depths = [self._calculate_structure_depth(v, current_depth + 1) 
                     for v in content.values()]
        else:  # list
            depths = [self._calculate_structure_depth(v, current_depth + 1) 
                     for v in content]
            
        return max(depths) if depths else current_depth
        
    def _is_sequence_valid(self, sequence: List[Dict[str, Any]]) -> bool:
        """Verifica se uma sequência temporal é válida."""
        if not sequence:
            return True
            
        try:
            prev_time = None
            for event in sequence:
                if "timestamp" not in event:
                    return False
                    
                current_time = datetime.fromisoformat(event["timestamp"])
                if prev_time and current_time < prev_time:
                    return False
                    
                prev_time = current_time
                
            return True
        except:
            return False
