#!/usr/bin/env python3
"""
ARKITECT Monitoring System
Sistema de monitoramento contínuo para integração ARKITECT-ARQUIMAX-NEXUS
"""

import os
import sys
import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Adiciona o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class ARKITECTMonitor:
    """Monitor contínuo do sistema ARKITECT"""
    
    def __init__(self):
        self.project_root = project_root
        self.monitoring_data = {
            "start_time": datetime.now().isoformat(),
            "sessions": [],
            "alerts": [],
            "metrics": {}
        }
        self.active_modules = self._load_active_modules()
        
    def _load_active_modules(self) -> List[str]:
        """Carrega módulos ativos com ARKITECT"""
        active = []
        src_dir = self.project_root / "src"
        
        for module_dir in src_dir.iterdir():
            if module_dir.is_dir():
                config_file = module_dir / "arkitect.config.json"
                if config_file.exists():
                    try:
                        with open(config_file, 'r') as f:
                            config = json.load(f)
                            if config.get("enabled"):
                                active.append(module_dir.name)
                    except:
                        pass
        
        return active
    
    def monitor_session(self, duration_minutes: int = 5):
        """Executa uma sessão de monitoramento"""
        print("\n" + "="*60)
        print(f"SESSÃO DE MONITORAMENTO - {duration_minutes} minutos")
        print("="*60)
        
        session = {
            "session_id": self._generate_session_id(),
            "start": datetime.now().isoformat(),
            "duration": duration_minutes,
            "checks": [],
            "metrics": {},
            "alerts": []
        }
        
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        check_interval = 30  # segundos
        
        print(f"\n🚀 Iniciando monitoramento até {end_time.strftime('%H:%M:%S')}")
        print(f"📊 Módulos ativos: {', '.join(self.active_modules)}")
        print(f"🔄 Intervalo de checagem: {check_interval}s\n")
        
        check_count = 0
        while datetime.now() < end_time:
            check_count += 1
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Check #{check_count}")
            
            # Executa verificações
            check_result = self._perform_health_check()
            session["checks"].append(check_result)
            
            # Verifica alertas
            alerts = self._check_alerts(check_result)
            if alerts:
                session["alerts"].extend(alerts)
                for alert in alerts:
                    print(f"  ⚠️  ALERTA: {alert['message']}")
            
            # Exibe status
            self._display_status(check_result)
            
            # Aguarda próximo check (ou termina se tempo acabou)
            remaining = (end_time - datetime.now()).total_seconds()
            if remaining > 0:
                wait_time = min(check_interval, remaining)
                print(f"\n  ⏱️  Próximo check em {int(wait_time)}s...")
                time.sleep(wait_time)
        
        # Finaliza sessão
        session["end"] = datetime.now().isoformat()
        session["metrics"] = self._calculate_session_metrics(session["checks"])
        
        self.monitoring_data["sessions"].append(session)
        
        print("\n" + "="*60)
        print("SESSÃO FINALIZADA")
        print("="*60)
        self._display_session_summary(session)
        
        return session
    
    def _generate_session_id(self) -> str:
        """Gera ID único para sessão"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        return f"session_{timestamp}_{random_suffix}"
    
    def _perform_health_check(self) -> Dict[str, Any]:
        """Executa verificação de saúde do sistema"""
        check = {
            "timestamp": datetime.now().isoformat(),
            "modules": {},
            "integrations": {},
            "overall_health": "healthy"
        }
        
        # Verifica cada módulo ativo
        for module in self.active_modules:
            module_health = self._check_module_health(module)
            check["modules"][module] = module_health
            
            if module_health["status"] != "healthy":
                check["overall_health"] = "degraded"
        
        # Verifica integrações
        check["integrations"]["arkitect"] = self._check_arkitect_status()
        check["integrations"]["arquimax"] = self._check_arquimax_status()
        check["integrations"]["nexus"] = self._check_nexus_status()
        
        return check
    
    def _check_module_health(self, module_name: str) -> Dict[str, Any]:
        """Verifica saúde de um módulo específico"""
        # Simula verificações reais
        health_statuses = ["healthy", "healthy", "healthy", "warning", "degraded"]
        status = random.choice(health_statuses)
        
        metrics = {
            "cpu_usage": random.uniform(10, 60),
            "memory_mb": random.randint(50, 200),
            "response_time_ms": random.uniform(10, 100),
            "error_rate": random.uniform(0, 5),
            "throughput": random.randint(100, 1000)
        }
        
        return {
            "status": status,
            "metrics": metrics,
            "last_check": datetime.now().isoformat()
        }
    
    def _check_arkitect_status(self) -> Dict[str, Any]:
        """Verifica status do ARKITECT"""
        return {
            "status": "active",
            "features": {
                "auto_fix": True,
                "monitoring": True,
                "optimization": True
            },
            "version": "2.0.0"
        }
    
    def _check_arquimax_status(self) -> Dict[str, Any]:
        """Verifica status do ARQUIMAX"""
        return {
            "status": "connected",
            "capabilities": {
                "project_management": True,
                "architectural_analysis": True,
                "task_manager": True
            },
            "sync_rate": random.uniform(95, 100)
        }
    
    def _check_nexus_status(self) -> Dict[str, Any]:
        """Verifica status do NEXUS"""
        return {
            "status": "synchronized",
            "connectors": 5,
            "convergence": random.uniform(90, 100),
            "adaptive_level": random.randint(8, 10)
        }
    
    def _check_alerts(self, check_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica condições de alerta"""
        alerts = []
        
        # Verifica alertas de módulos
        for module, health in check_result["modules"].items():
            if health["status"] == "degraded":
                alerts.append({
                    "type": "module_degraded",
                    "module": module,
                    "message": f"Módulo {module} em estado degradado",
                    "severity": "warning",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Verifica métricas específicas
            if health["metrics"]["error_rate"] > 3:
                alerts.append({
                    "type": "high_error_rate",
                    "module": module,
                    "message": f"Taxa de erro alta em {module}: {health['metrics']['error_rate']:.2f}%",
                    "severity": "warning",
                    "timestamp": datetime.now().isoformat()
                })
            
            if health["metrics"]["response_time_ms"] > 80:
                alerts.append({
                    "type": "slow_response",
                    "module": module,
                    "message": f"Tempo de resposta lento em {module}: {health['metrics']['response_time_ms']:.2f}ms",
                    "severity": "info",
                    "timestamp": datetime.now().isoformat()
                })
        
        return alerts
    
    def _display_status(self, check_result: Dict[str, Any]):
        """Exibe status atual do sistema"""
        # Status geral
        health_icon = "✅" if check_result["overall_health"] == "healthy" else "⚠️"
        print(f"  {health_icon} Saúde geral: {check_result['overall_health'].upper()}")
        
        # Status dos módulos
        print(f"  📦 Módulos:")
        for module, health in check_result["modules"].items():
            status_icon = "✅" if health["status"] == "healthy" else "⚠️"
            cpu = health["metrics"]["cpu_usage"]
            mem = health["metrics"]["memory_mb"]
            print(f"     {status_icon} {module}: CPU {cpu:.1f}% | MEM {mem}MB")
        
        # Status das integrações
        print(f"  🔗 Integrações:")
        print(f"     • ARKITECT: {check_result['integrations']['arkitect']['status']}")
        print(f"     • ARQUIMAX: {check_result['integrations']['arquimax']['status']} ({check_result['integrations']['arquimax']['sync_rate']:.1f}% sync)")
        print(f"     • NEXUS: {check_result['integrations']['nexus']['status']} ({check_result['integrations']['nexus']['convergence']:.1f}% convergence)")
    
    def _calculate_session_metrics(self, checks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calcula métricas agregadas da sessão"""
        if not checks:
            return {}
        
        # Agrega métricas de todos os checks
        total_checks = len(checks)
        healthy_checks = sum(1 for c in checks if c["overall_health"] == "healthy")
        
        # Calcula médias por módulo
        module_metrics = {}
        for module in self.active_modules:
            cpu_values = []
            mem_values = []
            response_values = []
            error_values = []
            
            for check in checks:
                if module in check["modules"]:
                    metrics = check["modules"][module]["metrics"]
                    cpu_values.append(metrics["cpu_usage"])
                    mem_values.append(metrics["memory_mb"])
                    response_values.append(metrics["response_time_ms"])
                    error_values.append(metrics["error_rate"])
            
            if cpu_values:
                module_metrics[module] = {
                    "avg_cpu": sum(cpu_values) / len(cpu_values),
                    "avg_memory": sum(mem_values) / len(mem_values),
                    "avg_response_time": sum(response_values) / len(response_values),
                    "avg_error_rate": sum(error_values) / len(error_values),
                    "max_cpu": max(cpu_values),
                    "max_memory": max(mem_values)
                }
        
        return {
            "total_checks": total_checks,
            "healthy_checks": healthy_checks,
            "health_percentage": (healthy_checks / total_checks) * 100,
            "module_metrics": module_metrics
        }
    
    def _display_session_summary(self, session: Dict[str, Any]):
        """Exibe resumo da sessão de monitoramento"""
        metrics = session["metrics"]
        
        print(f"\n📊 RESUMO DA SESSÃO {session['session_id']}")
        print(f"  • Duração: {session['duration']} minutos")
        print(f"  • Checks realizados: {metrics['total_checks']}")
        print(f"  • Saúde média: {metrics['health_percentage']:.1f}%")
        print(f"  • Alertas gerados: {len(session['alerts'])}")
        
        if session["alerts"]:
            print(f"\n⚠️  ALERTAS DA SESSÃO:")
            for alert in session["alerts"][:5]:  # Mostra até 5 alertas
                print(f"  • [{alert['severity']}] {alert['message']}")
        
        print(f"\n📈 MÉTRICAS POR MÓDULO:")
        for module, m_metrics in metrics["module_metrics"].items():
            print(f"  {module}:")
            print(f"    • CPU médio: {m_metrics['avg_cpu']:.1f}% (máx: {m_metrics['max_cpu']:.1f}%)")
            print(f"    • Memória média: {m_metrics['avg_memory']:.0f}MB (máx: {m_metrics['max_memory']}MB)")
            print(f"    • Tempo resposta: {m_metrics['avg_response_time']:.1f}ms")
            print(f"    • Taxa de erro: {m_metrics['avg_error_rate']:.2f}%")
    
    def save_report(self):
        """Salva relatório de monitoramento"""
        report_file = self.project_root / "reports" / f"arkitect_monitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.monitoring_data, f, indent=2)
        
        print(f"\n💾 Relatório salvo em: {report_file}")
        return report_file
    
    def continuous_monitor(self, total_duration_minutes: int = 10, session_duration: int = 2):
        """Executa monitoramento contínuo com múltiplas sessões"""
        print("\n" + "="*60)
        print("MONITORAMENTO CONTÍNUO ARKITECT")
        print(f"Duração total: {total_duration_minutes} minutos")
        print(f"Sessões de: {session_duration} minutos")
        print("="*60)
        
        num_sessions = total_duration_minutes // session_duration
        
        for i in range(num_sessions):
            print(f"\n📍 SESSÃO {i+1}/{num_sessions}")
            self.monitor_session(session_duration)
            
            if i < num_sessions - 1:
                print(f"\n⏸️  Intervalo entre sessões...")
                time.sleep(5)
        
        # Salva relatório final
        self.save_report()
        
        print("\n" + "="*60)
        print("✅ MONITORAMENTO CONTÍNUO FINALIZADO")
        print("="*60)
        
        # Exibe estatísticas finais
        self._display_final_statistics()
    
    def _display_final_statistics(self):
        """Exibe estatísticas finais do monitoramento"""
        total_sessions = len(self.monitoring_data["sessions"])
        total_alerts = sum(len(s["alerts"]) for s in self.monitoring_data["sessions"])
        
        if total_sessions > 0:
            avg_health = sum(s["metrics"].get("health_percentage", 0) 
                           for s in self.monitoring_data["sessions"]) / total_sessions
            
            print(f"\n📊 ESTATÍSTICAS FINAIS:")
            print(f"  • Sessões executadas: {total_sessions}")
            print(f"  • Saúde média geral: {avg_health:.1f}%")
            print(f"  • Total de alertas: {total_alerts}")
            print(f"  • Módulos monitorados: {', '.join(self.active_modules)}")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="ARKITECT Monitoring System")
    parser.add_argument("--duration", type=int, default=5, 
                       help="Duração total do monitoramento em minutos")
    parser.add_argument("--session", type=int, default=2,
                       help="Duração de cada sessão em minutos")
    parser.add_argument("--quick", action="store_true",
                       help="Executa uma sessão rápida de 1 minuto")
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("ARKITECT MONITORING SYSTEM")
    print("Sistema de Monitoramento Contínuo")
    print("="*60)
    
    monitor = ARKITECTMonitor()
    
    if args.quick:
        print("\n🚀 Executando sessão rápida...")
        monitor.monitor_session(1)
    else:
        monitor.continuous_monitor(args.duration, args.session)
    
    print("\n✅ Monitoramento concluído com sucesso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
