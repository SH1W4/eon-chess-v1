import os
import yaml
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Carregador de configurações do sistema de integração."""
    
    @staticmethod
    def load(config_path: str) -> Dict[str, Any]:
        """Carrega configuração a partir de um arquivo."""
        try:
            # Verifica extensão
            ext = os.path.splitext(config_path)[1].lower()
            
            # Carrega baseado no tipo
            if ext == ".yaml" or ext == ".yml":
                return ConfigLoader._load_yaml(config_path)
            elif ext == ".json":
                return ConfigLoader._load_json(config_path)
            else:
                raise ValueError(f"Formato de configuração não suportado: {ext}")
            
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {str(e)}")
            raise
    
    @staticmethod
    def _load_yaml(path: str) -> Dict[str, Any]:
        """Carrega configuração YAML."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            
            # Valida configuração
            ConfigLoader._validate_config(config)
            
            return config
            
        except Exception as e:
            logger.error(f"Erro ao carregar YAML: {str(e)}")
            raise
    
    @staticmethod
    def _load_json(path: str) -> Dict[str, Any]:
        """Carrega configuração JSON."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
            
            # Valida configuração
            ConfigLoader._validate_config(config)
            
            return config
            
        except Exception as e:
            logger.error(f"Erro ao carregar JSON: {str(e)}")
            raise
    
    @staticmethod
    def _validate_config(config: Dict[str, Any]):
        """Valida a configuração carregada."""
        try:
            # Verifica seção principal
            if "sistema_integracao" not in config:
                raise ValueError("Configuração deve ter seção 'sistema_integracao'")
            
            sistema = config["sistema_integracao"]
            
            # Verifica versão
            if "versao" not in sistema:
                raise ValueError("Versão do sistema não especificada")
            
            # Verifica componentes obrigatórios
            required_sections = [
                "nucleo_integracao",
                "conectores",
                "adaptadores",
                "protocolos",
                "cache",
                "monitoramento"
            ]
            
            for section in required_sections:
                if section not in sistema:
                    raise ValueError(f"Seção obrigatória ausente: {section}")
            
            # Valida configurações específicas
            ConfigLoader._validate_core_config(sistema["nucleo_integracao"])
            ConfigLoader._validate_connectors_config(sistema["conectores"])
            ConfigLoader._validate_adapters_config(sistema["adaptadores"])
            ConfigLoader._validate_protocols_config(sistema["protocolos"])
            ConfigLoader._validate_cache_config(sistema["cache"])
            ConfigLoader._validate_monitoring_config(sistema["monitoramento"])
            
        except Exception as e:
            logger.error(f"Erro na validação de configuração: {str(e)}")
            raise
    
    @staticmethod
    def _validate_core_config(config: Dict[str, Any]):
        """Valida configuração do núcleo."""
        try:
            # Verifica componentes do motor
            if "motor_integracao" not in config:
                raise ValueError("Configuração do motor ausente")
            
            motor = config["motor_integracao"]
            required_motor = ["conexoes", "roteamento", "sincronizacao"]
            
            for section in required_motor:
                if section not in motor:
                    raise ValueError(f"Seção do motor ausente: {section}")
            
            # Verifica sistema de adaptação
            if "sistema_adaptacao" not in config:
                raise ValueError("Configuração do sistema de adaptação ausente")
            
            adaptacao = config["sistema_adaptacao"]
            required_adapt = ["protocolos", "transformacao", "compatibilidade"]
            
            for section in required_adapt:
                if section not in adaptacao:
                    raise ValueError(f"Seção de adaptação ausente: {section}")
            
        except Exception as e:
            logger.error(f"Erro na validação do núcleo: {str(e)}")
            raise
    
    @staticmethod
    def _validate_connectors_config(config: Dict[str, Any]):
        """Valida configuração dos conectores."""
        try:
            required_connectors = ["cultural", "quantico", "narrativo"]
            
            for connector in required_connectors:
                if connector not in config:
                    raise ValueError(f"Conector obrigatório ausente: {connector}")
                
                conn_config = config[connector]
                required_fields = ["tipo", "cache", "validacao"]
                
                for field in required_fields:
                    if field not in conn_config:
                        raise ValueError(
                            f"Campo obrigatório ausente no conector {connector}: {field}"
                        )
            
        except Exception as e:
            logger.error(f"Erro na validação dos conectores: {str(e)}")
            raise
    
    @staticmethod
    def _validate_adapters_config(config: Dict[str, Any]):
        """Valida configuração dos adaptadores."""
        try:
            required_adapters = ["arquimax", "nexus", "symbiotic"]
            
            for adapter in required_adapters:
                if adapter not in config:
                    raise ValueError(f"Adaptador obrigatório ausente: {adapter}")
                
                adapt_config = config[adapter]
                required_fields = ["interface", "protocolo", "cache"]
                
                for field in required_fields:
                    if field not in adapt_config:
                        raise ValueError(
                            f"Campo obrigatório ausente no adaptador {adapter}: {field}"
                        )
            
        except Exception as e:
            logger.error(f"Erro na validação dos adaptadores: {str(e)}")
            raise
    
    @staticmethod
    def _validate_protocols_config(config: Dict[str, Any]):
        """Valida configuração dos protocolos."""
        try:
            required_protocols = ["comunicacao", "sincronizacao", "evolucao"]
            
            for protocol in required_protocols:
                if protocol not in config:
                    raise ValueError(f"Protocolo obrigatório ausente: {protocol}")
            
            # Valida protocolo de comunicação
            comm = config["comunicacao"]
            required_comm = ["formato", "compressao", "encriptacao", "validacao"]
            
            for field in required_comm:
                if field not in comm:
                    raise ValueError(
                        f"Campo obrigatório ausente no protocolo de comunicação: {field}"
                    )
            
            # Valida protocolo de sincronização
            sync = config["sincronizacao"]
            required_sync = ["estrategia", "conflitos", "versao", "cache"]
            
            for field in required_sync:
                if field not in sync:
                    raise ValueError(
                        f"Campo obrigatório ausente no protocolo de sincronização: {field}"
                    )
            
            # Valida protocolo de evolução
            evol = config["evolucao"]
            required_evol = ["modo", "compatibilidade", "versionamento", "migracao"]
            
            for field in required_evol:
                if field not in evol:
                    raise ValueError(
                        f"Campo obrigatório ausente no protocolo de evolução: {field}"
                    )
            
        except Exception as e:
            logger.error(f"Erro na validação dos protocolos: {str(e)}")
            raise
    
    @staticmethod
    def _validate_cache_config(config: Dict[str, Any]):
        """Valida configuração de cache."""
        try:
            required_caches = ["distribuido", "local", "adaptativo"]
            
            for cache in required_caches:
                if cache not in config:
                    raise ValueError(f"Cache obrigatório ausente: {cache}")
            
            # Valida cache distribuído
            dist = config["distribuido"]
            required_dist = ["tipo", "modo", "tamanho", "ttl"]
            
            for field in required_dist:
                if field not in dist:
                    raise ValueError(
                        f"Campo obrigatório ausente no cache distribuído: {field}"
                    )
            
            # Valida cache local
            local = config["local"]
            required_local = ["tipo", "tamanho", "ttl"]
            
            for field in required_local:
                if field not in local:
                    raise ValueError(
                        f"Campo obrigatório ausente no cache local: {field}"
                    )
            
            # Valida cache adaptativo
            adapt = config["adaptativo"]
            required_adapt = ["modo", "aprendizado", "otimizacao"]
            
            for field in required_adapt:
                if field not in adapt:
                    raise ValueError(
                        f"Campo obrigatório ausente no cache adaptativo: {field}"
                    )
            
        except Exception as e:
            logger.error(f"Erro na validação do cache: {str(e)}")
            raise
    
    @staticmethod
    def _validate_monitoring_config(config: Dict[str, Any]):
        """Valida configuração de monitoramento."""
        try:
            required_sections = ["metricas", "visualizacao"]
            
            for section in required_sections:
                if section not in config:
                    raise ValueError(f"Seção de monitoramento ausente: {section}")
            
            # Valida métricas
            metrics = config["metricas"]
            required_metrics = ["coleta", "storage", "retencao"]
            
            for field in required_metrics:
                if field not in metrics:
                    raise ValueError(
                        f"Campo obrigatório ausente nas métricas: {field}"
                    )
            
            # Valida visualização
            visual = config["visualizacao"]
            required_visual = ["plataforma", "dashboards", "alertas"]
            
            for field in required_visual:
                if field not in visual:
                    raise ValueError(
                        f"Campo obrigatório ausente na visualização: {field}"
                    )
            
        except Exception as e:
            logger.error(f"Erro na validação do monitoramento: {str(e)}")
            raise
    
    @staticmethod
    def save(config: Dict[str, Any], path: str):
        """Salva configuração em arquivo."""
        try:
            # Valida configuração
            ConfigLoader._validate_config(config)
            
            # Determina formato
            ext = os.path.splitext(path)[1].lower()
            
            # Salva baseado no formato
            if ext == ".yaml" or ext == ".yml":
                ConfigLoader._save_yaml(config, path)
            elif ext == ".json":
                ConfigLoader._save_json(config, path)
            else:
                raise ValueError(f"Formato não suportado para salvar: {ext}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar configuração: {str(e)}")
            raise
    
    @staticmethod
    def _save_yaml(config: Dict[str, Any], path: str):
        """Salva configuração em YAML."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(
                    config,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )
            
        except Exception as e:
            logger.error(f"Erro ao salvar YAML: {str(e)}")
            raise
    
    @staticmethod
    def _save_json(config: Dict[str, Any], path: str):
        """Salva configuração em JSON."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(
                    config,
                    f,
                    indent=2,
                    ensure_ascii=False,
                    sort_keys=False
                )
            
        except Exception as e:
            logger.error(f"Erro ao salvar JSON: {str(e)}")
            raise
