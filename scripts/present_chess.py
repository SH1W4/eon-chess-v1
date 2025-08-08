#!/usr/bin/env python3

import asyncio
import sys
import time
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn
from rich.table import Table
from rich.text import Text
from pyfiglet import Figlet

console = Console()

class ChessPresentation:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        
    async def show_intro(self):
        await self.clear_screen()
        
        # Criar banner principal
        f = Figlet(font='slant')
        banner = f.renderText('AEON CHESS')
        
        # Criar subtítulo
        f_small = Figlet(font='small')
        subtitle = f_small.renderText('Cultural & Evolution')
        subtitle2 = f_small.renderText('Symbiotic System')
        
        intro_text = f"""[bold cyan]
{banner}
[/bold cyan][bold green]
{subtitle}
{subtitle2}[/bold green]

[bold magenta]Um Sistema de Xadrez com IA Cultural Adaptativa[/bold magenta]
[bold cyan]================================================[/bold cyan]"""
        self.console.print(intro_text)
        await asyncio.sleep(2)

    async def show_core_features(self):
        """Demonstra os recursos principais"""
        with Progress() as progress:
            task1 = progress.add_task("[cyan]Motor de Xadrez...", total=100)
            task2 = progress.add_task("[magenta]Sistema Cultural...", total=100)
            task3 = progress.add_task("[green]IA Adaptativa...", total=100)

            while not progress.finished:
                progress.update(task1, advance=0.9)
                progress.update(task2, advance=0.7)
                progress.update(task3, advance=0.8)
                await asyncio.sleep(0.02)

    async def show_cultural_system(self):
        """Demonstra o sistema cultural"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Componente Cultural")
        table.add_column("Status")
        table.add_column("Progresso")

        table.add_row(
            "Motor Cultural",
            "* Ativo",
            "[green]85%"
        )
        table.add_row(
            "Sistema Narrativo",
            "* Operacional",
            "[yellow]70%"
        )
        table.add_row(
            "Eventos Culturais",
            "* Processando",
            "[yellow]70%"
        )

        self.console.print(Panel(table, title="Sistema Cultural", border_style="magenta"))
        await asyncio.sleep(3)

    async def show_ai_capabilities(self):
        """Demonstra as capacidades da IA"""
        with console.status("[bold green]Analisando capacidades da IA...") as status:
            await asyncio.sleep(1)
            console.print("* Aprendizado Adaptativo", style="green")
            await asyncio.sleep(0.5)
            console.print("* Integração Cultural", style="green")
            await asyncio.sleep(0.5)
            console.print("* Auto-Otimização", style="green")
            await asyncio.sleep(0.5)
            console.print("* Evolução Simbiótica", style="green")

    async def show_metrics(self):
        """Mostra métricas do sistema"""
        metrics = {
            "Velocidade de Desenvolvimento": "11.5%/dia",
            "Qualidade de Código": "85%",
            "Cobertura de Testes": "70%",
            "Dívida Técnica": "15%"
        }

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Métrica")
        table.add_column("Valor")

        for metric, value in metrics.items():
            table.add_row(metric, value)

        self.console.print(Panel(table, title="Métricas do Sistema", border_style="blue"))
        await asyncio.sleep(3)

    async def show_architecture(self):
        """Demonstra a arquitetura do sistema"""
        architecture = """
[bold cyan]AEON CHESS - Arquitetura Simbiótica Completa[/bold cyan]
[bold cyan]================================================[/bold cyan]

+------------------- Interface Layer --------------------+
|   +-----------+    +-----------+    +-------------+   |
|   |   Web UI  |    |  Mobile   |    |   Desktop   |   |
|   +-----------+    +-----------+    +-------------+   |
+------------------------+------------------------+
                         |
           +------------- SYMBIOTIC CORE --------------+
           |    +----------+    +----------+    +----------+    |
           |    | ARQUIMAX |----| NEXUS   |----| CHESS   |    |
           |    +----------+    +----------+    +----------+    |
           +------------------------+------------------------+
                         |
    +------------------+-------------------------+
    |                Enhanced Systems                    |
    |  +-----------+   +-----------+   +------------+   |
    |  | Cultural  |   |    AI     |   |  Quantum   |   |
    |  | +---------+   | +---------+   | +--------+ |   |
    |  | |Narrative|   | |Adaptive |   | |Optimize| |   |
    |  | +---------+   | +---------+   | +--------+ |   |
    |  | +---------+   | +---------+   | +--------+ |   |
    |  | |Events   |   | |Learning |   | |Simulate| |   |
    |  | +---------+   | +---------+   | +--------+ |   |
    |  +-----------+   +-----------+   +------------+   |
    +------------------------------------------------+

    +------------------ Data Layer -------------------+
    |  +-----------+   +----------+   +----------+   |
    |  | Cultural  |   |   AI     |   |  System  |   |
    |  | Database  |   |  Models  |   | Storage  |   |
    |  +-----------+   +----------+   +----------+   |
    +------------------------------------------------+
        """
        self.console.print(architecture)
        await asyncio.sleep(3)

    async def show_demo(self):
        """Executa a demonstração completa"""
        await self.show_intro()
        await self.show_core_features()
        await self.show_cultural_system()
        await self.show_ai_capabilities()
        await self.show_metrics()
        await self.show_architecture()

    async def clear_screen(self):
        self.console.clear()

if __name__ == "__main__":
    presentation = ChessPresentation()
    asyncio.run(presentation.show_demo())
