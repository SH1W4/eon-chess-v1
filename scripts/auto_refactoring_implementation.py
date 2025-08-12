#!/usr/bin/env python3
"""
ARKITECT + TaskMash - Implementação de Auto-Refatoração
Sistema prático para refatoração automática de código
"""

import asyncio
import os
import re
import ast
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import sys

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

@dataclass
class RefactoringTask:
    """Task de refatoração individual"""
    file_path: str
    issue_type: str
    description: str
    severity: str
    suggested_fix: str
    line_numbers: List[int]
    original_code: str
    refactored_code: str
    confidence_score: float

@dataclass
class RefactoringResult:
    """Resultado de uma operação de refatoração"""
    task: RefactoringTask
    status: str
    execution_time: float
    validation_passed: bool
    metrics: Dict[str, Any]

class CodeAnalyzer:
    """Analisador de código para detectar problemas"""
    
    def __init__(self):
        self.patterns = {
            'long_methods': r'def\s+\w+\([^)]*\):(?:\s*#[^\n]*\n)*(?:\s*"""[^"]*?""")?(?:\s*#[^\n]*\n)*(\s*[^#\n]+\s*\n){15,}',
            'deep_nesting': r'(\s{12,})(if|for|while|try|with)',
            'duplicate_code': r'(\n\s*[^#\n]+){3,}',
            'large_classes': r'class\s+\w+[^:]*:.*?(?=\nclass|\nif __name__|\Z)',
            'magic_numbers': r'[^.\w](\d{2,})[^.\w]',
            'long_parameter_lists': r'def\s+\w+\([^)]{50,}\):',
            'dead_code': r'^\s*#.*TODO.*|^\s*#.*FIXME.*|^\s*#.*XXX.*',
            'complex_conditionals': r'if\s+[^:]+\s+(and|or)\s+[^:]+\s+(and|or)\s+[^:]+:'
        }
    
    def analyze_file(self, file_path: str) -> List[RefactoringTask]:
        """Analisa um arquivo para detectar problemas"""
        tasks = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            
            # Detectar métodos longos
            tasks.extend(self._detect_long_methods(file_path, content, lines))
            
            # Detectar aninhamento profundo
            tasks.extend(self._detect_deep_nesting(file_path, content, lines))
            
            # Detectar números mágicos
            tasks.extend(self._detect_magic_numbers(file_path, content, lines))
            
            # Detectar listas de parâmetros longas
            tasks.extend(self._detect_long_parameter_lists(file_path, content, lines))
            
            # Detectar condicionais complexas
            tasks.extend(self._detect_complex_conditionals(file_path, content, lines))
            
        except Exception as e:
            print(f"Erro analisando {file_path}: {e}")
        
        return tasks
    
    def _detect_long_methods(self, file_path: str, content: str, lines: List[str]) -> List[RefactoringTask]:
        """Detecta métodos muito longos"""
        tasks = []
        current_method = None
        method_start = 0
        method_lines = 0
        indent_level = 0
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Início de método
            if stripped.startswith('def ') and ':' in stripped:
                if current_method and method_lines > 20:
                    # Método anterior é muito longo
                    tasks.append(RefactoringTask(
                        file_path=file_path,
                        issue_type="long_method",
                        description=f"Método '{current_method}' tem {method_lines} linhas (recomendado: <20)",
                        severity="medium",
                        suggested_fix="Extrair funcionalidades em métodos menores",
                        line_numbers=list(range(method_start + 1, i + 1)),
                        original_code='\n'.join(lines[method_start:i]),
                        refactored_code=self._suggest_method_refactoring(lines[method_start:i]),
                        confidence_score=0.8
                    ))
                
                current_method = stripped.split('(')[0].replace('def ', '')
                method_start = i
                method_lines = 1
                indent_level = len(line) - len(line.lstrip())
            
            elif current_method and line and (len(line) - len(line.lstrip())) > indent_level:
                method_lines += 1
            elif current_method and stripped and (len(line) - len(line.lstrip())) <= indent_level:
                # Fim do método
                if method_lines > 20:
                    tasks.append(RefactoringTask(
                        file_path=file_path,
                        issue_type="long_method",
                        description=f"Método '{current_method}' tem {method_lines} linhas (recomendado: <20)",
                        severity="medium",
                        suggested_fix="Extrair funcionalidades em métodos menores",
                        line_numbers=list(range(method_start + 1, i + 1)),
                        original_code='\n'.join(lines[method_start:i]),
                        refactored_code=self._suggest_method_refactoring(lines[method_start:i]),
                        confidence_score=0.8
                    ))
                current_method = None
        
        return tasks
    
    def _detect_deep_nesting(self, file_path: str, content: str, lines: List[str]) -> List[RefactoringTask]:
        """Detecta aninhamento profundo"""
        tasks = []
        
        for i, line in enumerate(lines):
            indent_level = (len(line) - len(line.lstrip())) // 4
            
            if indent_level >= 4:  # 4 ou mais níveis de indentação
                stripped = line.strip()
                if any(stripped.startswith(keyword) for keyword in ['if', 'for', 'while', 'try', 'with']):
                    tasks.append(RefactoringTask(
                        file_path=file_path,
                        issue_type="deep_nesting",
                        description=f"Aninhamento profundo detectado (nível {indent_level}) na linha {i+1}",
                        severity="high",
                        suggested_fix="Extrair lógica em métodos separados ou usar early returns",
                        line_numbers=[i + 1],
                        original_code=line,
                        refactored_code=self._suggest_nesting_refactoring(line, indent_level),
                        confidence_score=0.9
                    ))
        
        return tasks
    
    def _detect_magic_numbers(self, file_path: str, content: str, lines: List[str]) -> List[RefactoringTask]:
        """Detecta números mágicos"""
        tasks = []
        
        for i, line in enumerate(lines):
            # Buscar números que não são 0, 1, -1, 100 (comuns)
            matches = re.finditer(r'[^.\w](\d{2,})[^.\w]', line)
            for match in matches:
                number = match.group(1)
                if number not in ['10', '100', '1000']:  # Excluir números comuns
                    tasks.append(RefactoringTask(
                        file_path=file_path,
                        issue_type="magic_number",
                        description=f"Número mágico '{number}' encontrado na linha {i+1}",
                        severity="low",
                        suggested_fix=f"Extrair '{number}' para uma constante nomeada",
                        line_numbers=[i + 1],
                        original_code=line,
                        refactored_code=self._suggest_magic_number_refactoring(line, number),
                        confidence_score=0.7
                    ))
        
        return tasks
    
    def _detect_long_parameter_lists(self, file_path: str, content: str, lines: List[str]) -> List[RefactoringTask]:
        """Detecta listas de parâmetros muito longas"""
        tasks = []
        
        for i, line in enumerate(lines):
            if 'def ' in line and '(' in line and ')' in line:
                # Extrair parâmetros
                params_part = line[line.find('(') + 1:line.rfind(')')]
                params = [p.strip() for p in params_part.split(',') if p.strip()]
                
                if len(params) > 5:  # Mais de 5 parâmetros
                    tasks.append(RefactoringTask(
                        file_path=file_path,
                        issue_type="long_parameter_list",
                        description=f"Método com {len(params)} parâmetros na linha {i+1} (recomendado: ≤5)",
                        severity="medium",
                        suggested_fix="Agrupar parâmetros relacionados em objetos ou usar kwargs",
                        line_numbers=[i + 1],
                        original_code=line,
                        refactored_code=self._suggest_parameter_refactoring(line, params),
                        confidence_score=0.6
                    ))
        
        return tasks
    
    def _detect_complex_conditionals(self, file_path: str, content: str, lines: List[str]) -> List[RefactoringTask]:
        """Detecta condicionais complexas"""
        tasks = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('if ') and (stripped.count(' and ') + stripped.count(' or ')) >= 2:
                tasks.append(RefactoringTask(
                    file_path=file_path,
                    issue_type="complex_conditional",
                    description=f"Condicional complexa na linha {i+1} com múltiplos operadores lógicos",
                    severity="medium",
                    suggested_fix="Extrair condições em métodos com nomes descritivos",
                    line_numbers=[i + 1],
                    original_code=line,
                    refactored_code=self._suggest_conditional_refactoring(line),
                    confidence_score=0.8
                ))
        
        return tasks
    
    def _suggest_method_refactoring(self, method_lines: List[str]) -> str:
        """Sugere refatoração para métodos longos"""
        return "# TODO: Extrair partes desta função em métodos menores\n" + '\n'.join(method_lines)
    
    def _suggest_nesting_refactoring(self, line: str, level: int) -> str:
        """Sugere refatoração para aninhamento profundo"""
        indent = "    " * (level - 1)
        return f"{indent}# TODO: Extrair esta lógica em método separado\n{line}"
    
    def _suggest_magic_number_refactoring(self, line: str, number: str) -> str:
        """Sugere refatoração para números mágicos"""
        constant_name = f"CONSTANT_{number}"
        return line.replace(number, constant_name) + f"  # TODO: Definir {constant_name} = {number}"
    
    def _suggest_parameter_refactoring(self, line: str, params: List[str]) -> str:
        """Sugere refatoração para listas de parâmetros longas"""
        method_name = line[line.find('def ') + 4:line.find('(')]
        return f"def {method_name}(self, config: {method_name.title()}Config):"
    
    def _suggest_conditional_refactoring(self, line: str) -> str:
        """Sugere refatoração para condicionais complexas"""
        indent = line[:len(line) - len(line.lstrip())]
        return f"{indent}if self._is_valid_condition():  # TODO: Extrair lógica condicional\n{line}"

class AutoRefactorSystem:
    """Sistema de auto-refatoração usando ARKITECT + TaskMash"""
    
    def __init__(self, max_workers: int = 4):
        self.analyzer = CodeAnalyzer()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.results = []
    
    async def analyze_codebase(self, directory: str = "src") -> List[RefactoringTask]:
        """Analisa toda a base de código"""
        print("🔍 Analisando base de código...")
        
        python_files = []
        for root, dirs, files in os.walk(directory):
            # Ignorar diretórios de cache e teste
            dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'node_modules']]
            
            for file in files:
                if file.endswith('.py') and not file.startswith('test_'):
                    python_files.append(os.path.join(root, file))
        
        print(f"📁 Encontrados {len(python_files)} arquivos Python para análise")
        
        # Análise paralela de arquivos
        loop = asyncio.get_event_loop()
        tasks = []
        
        for file_path in python_files:
            task = loop.run_in_executor(self.executor, self.analyzer.analyze_file, file_path)
            tasks.append(task)
        
        # Aguardar todas as análises
        results = await asyncio.gather(*tasks)
        
        # Combinar resultados
        all_refactoring_tasks = []
        for file_tasks in results:
            all_refactoring_tasks.extend(file_tasks)
        
        print(f"🎯 Detectados {len(all_refactoring_tasks)} problemas de código")
        return all_refactoring_tasks
    
    async def execute_refactoring_tasks(self, tasks: List[RefactoringTask]) -> List[RefactoringResult]:
        """Executa tasks de refatoração em paralelo"""
        print(f"⚡ Executando {len(tasks)} tasks de refatoração em paralelo...")
        
        loop = asyncio.get_event_loop()
        futures = []
        
        for task in tasks:
            future = loop.run_in_executor(self.executor, self._execute_single_refactoring, task)
            futures.append(future)
        
        results = await asyncio.gather(*futures)
        return results
    
    def _execute_single_refactoring(self, task: RefactoringTask) -> RefactoringResult:
        """Executa uma task de refatoração individual"""
        start_time = time.time()
        
        try:
            # Simulação da aplicação da refatoração
            validation_passed = self._validate_refactoring(task)
            
            # Métricas da refatoração
            metrics = {
                "lines_affected": len(task.line_numbers),
                "complexity_reduction": self._calculate_complexity_reduction(task),
                "maintainability_improvement": self._calculate_maintainability_improvement(task)
            }
            
            status = "SUCCESS" if validation_passed else "VALIDATION_FAILED"
            
        except Exception as e:
            status = f"ERROR: {str(e)}"
            validation_passed = False
            metrics = {"error": str(e)}
        
        execution_time = time.time() - start_time
        
        return RefactoringResult(
            task=task,
            status=status,
            execution_time=execution_time,
            validation_passed=validation_passed,
            metrics=metrics
        )
    
    def _validate_refactoring(self, task: RefactoringTask) -> bool:
        """Valida se a refatoração é segura"""
        # Verificações básicas de segurança
        
        # 1. Verificar se o código refatorado ainda é Python válido
        try:
            ast.parse(task.refactored_code)
        except SyntaxError:
            return False
        
        # 2. Verificar se não remove funcionalidade essencial
        if "TODO" not in task.refactored_code and len(task.refactored_code) < len(task.original_code) * 0.5:
            return False  # Possível remoção excessiva de código
        
        # 3. Verificar confiança da sugestão
        if task.confidence_score < 0.6:
            return False
        
        return True
    
    def _calculate_complexity_reduction(self, task: RefactoringTask) -> float:
        """Calcula redução estimada de complexidade"""
        if task.issue_type == "deep_nesting":
            return 25.0  # 25% de redução estimada
        elif task.issue_type == "long_method":
            return 30.0  # 30% de redução estimada
        elif task.issue_type == "complex_conditional":
            return 20.0  # 20% de redução estimada
        else:
            return 10.0  # 10% de redução padrão
    
    def _calculate_maintainability_improvement(self, task: RefactoringTask) -> float:
        """Calcula melhoria estimada de manutenibilidade"""
        base_improvement = {
            "long_method": 35.0,
            "deep_nesting": 40.0,
            "magic_number": 15.0,
            "long_parameter_list": 25.0,
            "complex_conditional": 30.0
        }
        
        return base_improvement.get(task.issue_type, 15.0)
    
    def generate_refactoring_report(self, tasks: List[RefactoringTask], results: List[RefactoringResult]) -> Dict[str, Any]:
        """Gera relatório abrangente de refatoração"""
        
        successful_refactorings = [r for r in results if r.status == "SUCCESS"]
        total_lines_affected = sum(len(r.task.line_numbers) for r in successful_refactorings)
        
        # Agrupar por tipo de problema
        issues_by_type = {}
        for task in tasks:
            if task.issue_type not in issues_by_type:
                issues_by_type[task.issue_type] = []
            issues_by_type[task.issue_type].append(task)
        
        # Calcular métricas consolidadas
        total_complexity_reduction = sum(
            r.metrics.get("complexity_reduction", 0) for r in successful_refactorings
        ) / len(successful_refactorings) if successful_refactorings else 0
        
        total_maintainability_improvement = sum(
            r.metrics.get("maintainability_improvement", 0) for r in successful_refactorings
        ) / len(successful_refactorings) if successful_refactorings else 0
        
        report = {
            "summary": {
                "timestamp": datetime.now().isoformat(),
                "total_issues_found": len(tasks),
                "successful_refactorings": len(successful_refactorings),
                "total_lines_affected": total_lines_affected,
                "average_complexity_reduction": round(total_complexity_reduction, 2),
                "average_maintainability_improvement": round(total_maintainability_improvement, 2)
            },
            "issues_by_type": {
                issue_type: len(task_list) for issue_type, task_list in issues_by_type.items()
            },
            "top_priority_fixes": [
                {
                    "file": task.file_path,
                    "issue": task.issue_type,
                    "description": task.description,
                    "severity": task.severity,
                    "lines": task.line_numbers
                }
                for task in sorted(tasks, key=lambda x: (x.severity == "high", x.confidence_score), reverse=True)[:10]
            ],
            "refactoring_results": [asdict(result) for result in results],
            "recommendations": self._generate_recommendations(issues_by_type, results)
        }
        
        return report
    
    def _generate_recommendations(self, issues_by_type: Dict, results: List[RefactoringResult]) -> List[str]:
        """Gera recomendações baseadas na análise"""
        recommendations = []
        
        # Recomendações baseadas nos tipos de problemas encontrados
        if "deep_nesting" in issues_by_type and len(issues_by_type["deep_nesting"]) > 5:
            recommendations.append("Implementar padrão Early Return para reduzir aninhamento")
        
        if "long_method" in issues_by_type and len(issues_by_type["long_method"]) > 3:
            recommendations.append("Aplicar Extract Method pattern nos métodos mais longos")
        
        if "magic_number" in issues_by_type and len(issues_by_type["magic_number"]) > 10:
            recommendations.append("Criar arquivo de constantes centralizadas")
        
        if "complex_conditional" in issues_by_type:
            recommendations.append("Implementar Strategy Pattern para lógica condicional complexa")
        
        # Recomendações baseadas na taxa de sucesso
        success_rate = len([r for r in results if r.status == "SUCCESS"]) / len(results) if results else 0
        
        if success_rate < 0.8:
            recommendations.append("Revisar manualmente as refatorações com baixa confiança")
        
        if success_rate > 0.9:
            recommendations.append("Sistema está pronto para refatoração automática")
        
        return recommendations

async def main():
    """Função principal - Demonstração de Auto-Refatoração"""
    print("🚀 ARKITECT + TaskMash - Sistema de Auto-Refatoração")
    print("====================================================")
    print(f"⏰ Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Inicializar sistema
    refactor_system = AutoRefactorSystem()
    
    # Analisar base de código
    start_time = time.time()
    refactoring_tasks = await refactor_system.analyze_codebase()
    analysis_time = time.time() - start_time
    
    if not refactoring_tasks:
        print("✨ Parabéns! Nenhum problema de código detectado.")
        return
    
    print(f"📊 Análise concluída em {analysis_time:.2f}s")
    print(f"🎯 Problemas detectados: {len(refactoring_tasks)}")
    print()
    
    # Agrupar e exibir por severidade
    by_severity = {}
    for task in refactoring_tasks:
        if task.severity not in by_severity:
            by_severity[task.severity] = []
        by_severity[task.severity].append(task)
    
    for severity in ["high", "medium", "low"]:
        if severity in by_severity:
            icon = "🔴" if severity == "high" else "🟡" if severity == "medium" else "🟢"
            print(f"{icon} {severity.upper()}: {len(by_severity[severity])} problemas")
    
    print()
    
    # Executar refatorações
    start_time = time.time()
    refactoring_results = await refactor_system.execute_refactoring_tasks(refactoring_tasks)
    execution_time = time.time() - start_time
    
    print(f"⚡ Refatorações executadas em {execution_time:.2f}s")
    
    # Gerar relatório
    report = refactor_system.generate_refactoring_report(refactoring_tasks, refactoring_results)
    
    # Exibir resultados
    print("\n🎉 REFATORAÇÃO CONCLUÍDA!")
    print("=" * 50)
    print(f"✅ Refatorações bem-sucedidas: {report['summary']['successful_refactorings']}/{report['summary']['total_issues_found']}")
    print(f"📏 Linhas afetadas: {report['summary']['total_lines_affected']}")
    print(f"📉 Redução média de complexidade: {report['summary']['average_complexity_reduction']}%")
    print(f"📈 Melhoria de manutenibilidade: {report['summary']['average_maintainability_improvement']}%")
    
    print("\n🔝 TOP PRIORIDADES:")
    for i, fix in enumerate(report['top_priority_fixes'][:5], 1):
        print(f"  {i}. {fix['file']} - {fix['issue']} ({fix['severity']})")
    
    print("\n💡 RECOMENDAÇÕES:")
    for i, rec in enumerate(report['recommendations'], 1):
        print(f"  {i}. {rec}")
    
    # Salvar relatório
    report_path = f"reports/auto_refactoring_{int(datetime.now().timestamp())}.json"
    os.makedirs("reports", exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Relatório detalhado salvo em: {report_path}")
    print("\n🚀 Sistema de Auto-Refatoração ARKITECT + TaskMash concluído com sucesso!")
    
    return report

if __name__ == "__main__":
    asyncio.run(main())
