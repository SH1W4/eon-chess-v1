#!/usr/bin/env python3

import asyncio
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Dict, Any
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.columns import Columns
from rich import box
from pyfiglet import Figlet

# Configuração global
console = Console()

class Section(Enum):
    INTRO = auto()
    FEATURES = auto()
    CULTURAL = auto()
    METRICS = auto()
    ARCHITECTURE = auto()

@dataclass
class Feature:
    name: str
    description: str
    progress: int
    status: str
    color: str

@dataclass
class Metric:
    name: str
    value: str
    trend: str
    description: str

class AeonPresentation:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.features = self._init_features()
        self.metrics = self._init_metrics()
        
    def _init_features(self) -> Dict[str, Feature]:
        return {
            "chess": Feature(
                "Motor de Xadrez",
                "Engine de xadrez com IA adaptativa",
                90, "Ativo", "cyan"
            ),
            "cultural": Feature(
                "Sistema Cultural",
                "Sistema de processamento cultural",
                80, "Operacional", "magenta"
            ),
            "ai": Feature(
                "IA Adaptativa",
                "Sistema de aprendizado dinâmico",
                85, "Otimizando", "green"
            )
        }
        
    def _init_metrics(self) -> Dict[str, Metric]:
        return {
            "dev_speed": Metric(
                "Velocidade de Desenvolvimento",
                "11.5%/dia",
                "↑",
                "Taxa de entrega de features"
            ),
            "code_quality": Metric(
                "Qualidade de Código",
                "85%",
                "→",
                "Métricas de qualidade"
            ),
            "test_coverage": Metric(
                "Cobertura de Testes",
                "70%",
                "↑",
                "Testes automatizados"
            ),
            "tech_debt": Metric(
                "Dívida Técnica",
                "15%",
                "↓",
                "Índice de manutenibilidade"
            )
        }

    async def _create_title(self, text: str, font: str = 'slant') -> str:
        f = Figlet(font=font)
        return f.renderText(text)

    async def show_intro(self):
        """Apresentação inicial com animação"""
        await self._clear_screen()
        
        # Banner principal
        title = await self._create_title('AEON CHESS')
        subtitle = await self._create_title('NEXUS', 'small')
        
        # Painel de introdução
        intro_panel = Panel(
            f"[bold cyan]{title}[/bold cyan]\n"
            f"[bold green]{subtitle}[/bold green]\n"
            "[bold magenta]Sistema de Xadrez com IA Cultural Adaptativa[/bold magenta]",
            title="[bold yellow]Bem-vindo ao Projeto AEON[/bold yellow]",
            border_style="cyan",
            box=box.DOUBLE
        )
        
        self.console.print(intro_panel)
        await asyncio.sleep(2)

    async def show_features(self):
        """Demonstração dos recursos com progresso interativo"""
        with Live(console=self.console, refresh_per_second=4) as live:
            for feature in self.features.values():
                progress = Progress(
                    TextColumn("[bold blue]{task.description}"),
                    SpinnerColumn(),
                    *Progress.get_default_columns(),
                )
                task = progress.add_task(
                    description=feature.description,
                    total=100
                )
                
                live.update(Panel(
                    progress,
                    title=f"[{feature.color}]{feature.name}[/{feature.color}]",
                    border_style=feature.color
                ))
                
                while not progress.finished:
                    progress.update(task, advance=5)
                    await asyncio.sleep(0.1)

    async def show_cultural_system(self):
        """Visualização do sistema cultural"""
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            title="Sistema Cultural",
            title_style="bold magenta"
        )
        
        table.add_column("Componente", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Detalhes", style="magenta")
        
        components = [
            ("Motor Cultural", "ATIVO", "Processamento de padrões culturais"),
            ("Narrativa", "OPERACIONAL", "Geração de contexto histórico"),
            ("Eventos", "PROCESSANDO", "Análise de eventos significativos")
        ]
        
        for comp in components:
            table.add_row(*comp)
        
        self.console.print(Panel(table, box=box.DOUBLE))
        await asyncio.sleep(2)

    async def show_architecture(self):
        """Arquitetura do sistema em ASCII art aprimorada"""
        architecture = """
[bold cyan]AEON CHESS - Arquitetura Neural Simbiótica[/bold cyan]

+====================[ Interface Layer ]====================+
|                                                         |
|   +------------+    +------------+    +------------+    |
|   |   WEB UI   |====|   MOBILE   |====|  DESKTOP   |    |
|   +------------+    +------------+    +------------+    |
|                           ||                           |
+========================||==========================+
                         ||
         +===============||===============+
         |        SYMBIOTIC CORE         |
         |  +----------+    +----------+ |
         |  | ARQUIMAX |====|  NEXUS   | |
         |  +----------+    +----------+ |
         |         ||           ||      |
         +=========||===========||======+
                  ||           ||
    +============ || ========= || =============+
    |          Neural Network Layer           |
    |   +-----------+   +-----------+        |
    |   | Cultural  |===|    AI     |        |
    |   |  Engine   |   |  Engine   |        |
    |   +-----------+   +-----------+        |
    |         ||            ||              |
    +=========||============||==============+
             ||            ||
    +========||============||=============+
    |       Data & Learning Layer         |
    |  +----------+   +------------+      |
    |  | Cultural |===| Neural DB  |      |
    |  |    DB    |   |  & Cache   |      |
    |  +----------+   +------------+      |
    +===================================+
"""
        self.console.print(Panel(architecture, box=box.DOUBLE))
        await asyncio.sleep(3)

    async def show_metrics(self):
        """Dashboard de métricas"""
        metrics_panel = []
        
        for metric in self.metrics.values():
            table = Table(show_header=False, box=box.ROUNDED)
            table.add_column(style="bold blue")
            table.add_column(style="green")
            
            table.add_row(
                metric.name,
                f"{metric.value} {metric.trend}"
            )
            table.add_row(
                "Descrição",
                metric.description
            )
            
            metrics_panel.append(Panel(
                table,
                title=f"[bold blue]{metric.name}[/bold blue]",
                border_style="blue"
            ))
        
        self.console.print(Columns(metrics_panel))
        await asyncio.sleep(2)

    async def show_demo(self):
        """Execução da demonstração completa"""
        sections = {
            Section.INTRO: self.show_intro,
            Section.FEATURES: self.show_features,
            Section.CULTURAL: self.show_cultural_system,
            Section.METRICS: self.show_metrics,
            Section.ARCHITECTURE: self.show_architecture
        }
        
        for section in Section:
            await self._clear_screen()
            await sections[section]()
            if section != Section.ARCHITECTURE:
                if not await self._confirm_continue():
                    break

    async def _confirm_continue(self) -> bool:
        """Confirmação para continuar a apresentação"""
        return Prompt.ask("\n[bold yellow]Pressione ENTER para continuar[/bold yellow]") != 'q'

    async def _clear_screen(self):
        """Limpa a tela"""
        self.console.clear()

if __name__ == "__main__":
    presentation = AeonPresentation()
    asyncio.run(presentation.show_demo())
