import os
import sys
import yaml
import logging
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('arkitect')

class ArkitectIntegration:
    def __init__(self):
        self.config = None
        self.components = {}
        self.base_path = Path(__file__).parent
        self.load_config()

    def load_config(self):
        """Carrega a configuração do ARKITECT"""
        config_path = self.base_path / 'config.yaml'
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            logger.info("Configuração do ARKITECT carregada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            sys.exit(1)

    def init_components(self):
        """Inicializa todos os componentes do ARKITECT"""
        for component_name, settings in self.config['components'].items():
            if settings.get('enabled', False):
                try:
                    self.init_component(component_name, settings)
                    logger.info(f"Componente {component_name} inicializado")
                except Exception as e:
                    logger.error(f"Erro ao inicializar {component_name}: {e}")

    def init_component(self, name, settings):
        """Inicializa um componente específico"""
        if name == 'architecture_analysis':
            self.init_architecture_analysis(settings)
        elif name == 'code_quality':
            self.init_code_quality(settings)
        elif name == 'evolution_tracking':
            self.init_evolution_tracking(settings)
        elif name == 'integration_management':
            self.init_integration_management(settings)

    def init_architecture_analysis(self, settings):
        """Inicializa o componente de análise arquitetural"""
        from .components.architecture import ArchitectureAnalyzer
        self.components['architecture_analysis'] = ArchitectureAnalyzer(
            depth=settings['settings']['analysis_depth'],
            interval=settings['settings']['update_interval']
        )

    def init_code_quality(self, settings):
        """Inicializa o componente de qualidade de código"""
        from .components.quality import CodeQualityAnalyzer
        self.components['code_quality'] = CodeQualityAnalyzer(
            threshold=settings['settings']['quality_threshold'],
            frequency=settings['settings']['check_frequency']
        )

    def init_evolution_tracking(self, settings):
        """Inicializa o componente de tracking de evolução"""
        from .components.evolution import EvolutionTracker
        self.components['evolution_tracking'] = EvolutionTracker(
            retention=settings['settings']['history_retention'],
            interval=settings['settings']['analysis_interval']
        )

    def init_integration_management(self, settings):
        """Inicializa o componente de gerenciamento de integração"""
        from .components.integration import IntegrationManager
        self.components['integration_management'] = IntegrationManager(
            interval=settings['settings']['sync_interval'],
            retries=settings['settings']['retry_attempts']
        )

    def setup_aeon_chess_integration(self):
        """Configura a integração específica com o aeon_chess"""
        if 'aeon_chess' not in self.config:
            logger.warning("Configuração do aeon_chess não encontrada")
            return

        chess_config = self.config['aeon_chess']
        
        # Configurar análise dos componentes
        for component in chess_config['analysis']['components']:
            self.setup_component_analysis(component)

        # Configurar tracking de evolução
        for focus_area in chess_config['evolution_tracking']['focus_areas']:
            self.setup_evolution_tracking(focus_area)

        # Configurar quality gates
        self.setup_quality_gates(chess_config['quality_gates'])

        # Configurar pontos de integração
        self.setup_integration_points(chess_config['integration_points'])

        logger.info("Integração com aeon_chess configurada com sucesso")

    def setup_component_analysis(self, component):
        """Configura análise para um componente específico"""
        analyzer = self.components['architecture_analysis']
        analyzer.add_component_analysis(
            name=component['name'],
            patterns=component['patterns'],
            metrics=component['metrics']
        )

    def setup_evolution_tracking(self, focus_area):
        """Configura tracking de evolução para uma área específica"""
        tracker = self.components['evolution_tracking']
        tracker.add_focus_area(
            component=focus_area['component'],
            metrics=focus_area['metrics']
        )

    def setup_quality_gates(self, gates):
        """Configura quality gates para os componentes"""
        quality = self.components['code_quality']
        for component, thresholds in gates.items():
            quality.add_quality_gate(component, thresholds)

    def setup_integration_points(self, integration_points):
        """Configura pontos de integração com outros sistemas"""
        integration = self.components['integration_management']
        for point in integration_points:
            integration.add_integration_point(
                system=point['system'],
                features=point['features']
            )

    def start(self):
        """Inicia o ARKITECT"""
        try:
            logger.info("Iniciando ARKITECT...")
            self.init_components()
            self.setup_aeon_chess_integration()
            logger.info("ARKITECT iniciado com sucesso")
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar ARKITECT: {e}")
            return False

def main():
    arkitect = ArkitectIntegration()
    if arkitect.start():
        logger.info("ARKITECT está pronto para uso")
    else:
        logger.error("Falha ao iniciar ARKITECT")
        sys.exit(1)

if __name__ == '__main__':
    main()
