"""
Symbiotic Framework for CHESS Project
Integrates NEXUS and ARQUIMAX for adaptive evolution
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging

# Import connectors
from .nexus_connector import NexusConnector, NexusConfig, initialize_nexus
from .arquimax_connector import ArquimaxConnector, ArquimaxConfig, initialize_arquimax, Task

logger = logging.getLogger(__name__)

class EvolutionPhase(Enum):
    """Evolution phases of the symbiotic system"""
    BOOTSTRAP = "bootstrap"
    ADAPTATION = "adaptation"
    EVOLUTION = "evolution"
    AUTONOMOUS = "autonomous"

@dataclass
class SymbioticConfig:
    """Configuration for symbiotic framework"""
    project_type: str = "git_repository"
    integration_mode: str = "full"  # full, partial, minimal
    adaptation_level: float = 0.7
    symbiotic_threshold: float = 0.7
    stability_threshold: float = 0.8
    evolution_interval: int = 3600  # seconds
    health_check_interval: int = 60

class SymbioticFramework:
    """Main symbiotic framework integrating NEXUS and ARQUIMAX"""
    
    def __init__(self, config: Optional[SymbioticConfig] = None):
        self.config = config or SymbioticConfig()
        self.nexus: Optional[NexusConnector] = None
        self.arquimax: Optional[ArquimaxConnector] = None
        self.current_phase = EvolutionPhase.BOOTSTRAP
        self.symbiotic_index = 0.0
        self.stability_score = 0.0
        self.capabilities = {
            "required": [],
            "optional": [],
            "active": []
        }
        self.evolution_history = []
        self.is_active = False
        
    async def symbiotic_init(self):
        """Initialize symbiotic mode"""
        logger.info("=== Initiating Symbiotic Mode ===")
        logger.info(f"Project type: {self.config.project_type}")
        logger.info(f"Integration mode: {self.config.integration_mode}")
        
        # Initialize NEXUS
        logger.info("Initializing NEXUS subsystem...")
        self.nexus = await initialize_nexus(
            project_type=self.config.project_type,
            mode=self.config.integration_mode
        )
        
        # Initialize ARQUIMAX
        logger.info("Initializing ARQUIMAX subsystem...")
        enable_all = self.config.integration_mode == "full"
        self.arquimax = initialize_arquimax(enable_all=enable_all)
        
        self.is_active = True
        logger.info("Symbiotic initialization complete")
        return True
    
    async def capability_analysis(self):
        """Analyze required and optional capabilities"""
        logger.info("Analyzing capabilities...")
        
        # Define capabilities based on project type
        capability_map = {
            "git_repository": {
                "required": ["task_management", "document_sync"],
                "optional": ["monitoring", "metrics"]
            },
            "ci_cd_pipeline": {
                "required": ["task_management", "monitoring"],
                "optional": ["metrics", "adaptive_execution"]
            },
            "document_management": {
                "required": ["document_sync", "connectors"],
                "optional": ["monitoring", "metrics"]
            }
        }
        
        project_caps = capability_map.get(self.config.project_type, {})
        self.capabilities["required"] = project_caps.get("required", [])
        self.capabilities["optional"] = project_caps.get("optional", [])
        
        # Check active capabilities
        active_caps = []
        
        # Check NEXUS capabilities
        if self.nexus and self.nexus.is_active:
            if "document_sync" in self.nexus.active_connectors:
                active_caps.append("document_sync")
            if "adaptive_execution" in self.nexus.active_connectors:
                active_caps.append("adaptive_execution")
            if "connectors" in self.nexus.active_connectors:
                active_caps.append("connectors")
        
        # Check ARQUIMAX capabilities
        if self.arquimax and self.arquimax.is_initialized:
            if "project_management" in self.arquimax.capabilities:
                active_caps.append("task_management")
            if "monitoring" in self.arquimax.capabilities:
                active_caps.append("monitoring")
            if self.arquimax.metrics:
                active_caps.append("metrics")
        
        self.capabilities["active"] = active_caps
        
        logger.info(f"Required capabilities: {self.capabilities['required']}")
        logger.info(f"Optional capabilities: {self.capabilities['optional']}")
        logger.info(f"Active capabilities: {self.capabilities['active']}")
        
        # Check if all required capabilities are active
        all_required = all(cap in active_caps for cap in self.capabilities["required"])
        
        if all_required:
            logger.info("✓ All required capabilities are active")
            self.transition_phase(EvolutionPhase.ADAPTATION)
        else:
            missing = [cap for cap in self.capabilities["required"] if cap not in active_caps]
            logger.warning(f"✗ Missing required capabilities: {missing}")
        
        return {
            "required": self.capabilities["required"],
            "optional": self.capabilities["optional"],
            "active": self.capabilities["active"],
            "all_required_active": all_required
        }
    
    async def arquimax_bridge(self):
        """Establish ARQUIMAX bridge for task management and monitoring"""
        if not self.arquimax:
            logger.error("ARQUIMAX not initialized")
            return False
        
        logger.info("Establishing ARQUIMAX bridge...")
        
        # Validate ARQUIMAX system
        is_valid = self.arquimax.system_validation()
        
        if is_valid:
            logger.info("✓ ARQUIMAX bridge established")
            
            # Create integration task
            task = Task(
                id="symbiotic_bridge_001",
                name="ARQUIMAX Bridge Integration",
                type="integration",
                priority=10
            )
            
            if self.arquimax.task_manager:
                await self.arquimax.task_manager.submit_task(task)
                result = await self.arquimax.task_manager.execute_task(task.id)
                logger.info(f"Bridge task result: {result}")
        else:
            logger.error("✗ ARQUIMAX bridge failed validation")
        
        return is_valid
    
    async def nexus_bridge(self):
        """Establish NEXUS bridge for document sync and adaptive execution"""
        if not self.nexus:
            logger.error("NEXUS not initialized")
            return False
        
        logger.info("Establishing NEXUS bridge...")
        
        # Validate NEXUS system
        is_valid = await self.nexus.validation()
        
        if is_valid:
            logger.info("✓ NEXUS bridge established")
            
            # Test adaptive execution
            test_task = {
                "id": "symbiotic_bridge_002",
                "type": "integration",
                "size": 10
            }
            
            result = await self.nexus.adaptive_execution(test_task)
            logger.info(f"Bridge task result: {result}")
        else:
            logger.error("✗ NEXUS bridge failed validation")
        
        return is_valid
    
    async def symbiotic_learning(self):
        """Execute symbiotic learning process"""
        logger.info("Executing symbiotic learning...")
        
        learning_data = {
            "timestamp": datetime.now().isoformat(),
            "phase": self.current_phase.value,
            "metrics": {}
        }
        
        # Collect metrics from NEXUS
        if self.nexus:
            convergence = await self.nexus.convergence()
            learning_data["metrics"]["nexus_convergence"] = convergence
        
        # Collect metrics from ARQUIMAX
        if self.arquimax:
            metrics = self.arquimax.get_metrics()
            learning_data["metrics"]["arquimax"] = metrics
        
        # Calculate adaptation rate
        adaptation_rate = self.calculate_adaptation_rate(learning_data["metrics"])
        learning_data["adaptation_rate"] = adaptation_rate
        
        # Update symbiotic index
        self.update_symbiotic_index(adaptation_rate)
        learning_data["symbiotic_index"] = self.symbiotic_index
        
        # Record learning
        self.evolution_history.append(learning_data)
        
        logger.info(f"Adaptation rate: {adaptation_rate:.2%}")
        logger.info(f"Symbiotic index: {self.symbiotic_index:.2%}")
        
        return learning_data
    
    async def capability_evolution(self):
        """Evolve system capabilities based on usage and performance"""
        logger.info("Evolving capabilities...")
        
        evolution_actions = []
        
        # Check for capability enhancement
        for cap in self.capabilities["active"]:
            usage_rate = self.get_capability_usage(cap)
            efficiency = self.get_capability_efficiency(cap)
            
            if usage_rate > 0.8 and efficiency > 0.7:
                logger.info(f"Enhancing capability: {cap}")
                evolution_actions.append({
                    "action": "enhance",
                    "capability": cap,
                    "reason": "high usage and efficiency"
                })
        
        # Check for new capability emergence
        if self.symbiotic_index > 0.9 and self.stability_score > 0.8:
            logger.info("Conditions met for new capability emergence")
            evolution_actions.append({
                "action": "emerge",
                "capability": "advanced_optimization",
                "reason": "high symbiotic index and stability"
            })
        
        # Apply evolution actions
        for action in evolution_actions:
            await self.apply_evolution_action(action)
        
        return evolution_actions
    
    async def symbiotic_health(self):
        """Monitor symbiotic system health"""
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "integration_health": 0.0,
            "capability_usage": {},
            "evolution_progress": 0.0,
            "alerts": []
        }
        
        # Check integration health
        nexus_health = 1.0 if (self.nexus and self.nexus.is_active) else 0.0
        arquimax_health = 1.0 if (self.arquimax and self.arquimax.is_initialized) else 0.0
        health_data["integration_health"] = (nexus_health + arquimax_health) / 2
        
        # Check capability usage
        for cap in self.capabilities["active"]:
            health_data["capability_usage"][cap] = self.get_capability_usage(cap)
        
        # Calculate evolution progress
        if self.current_phase == EvolutionPhase.AUTONOMOUS:
            health_data["evolution_progress"] = 1.0
        elif self.current_phase == EvolutionPhase.EVOLUTION:
            health_data["evolution_progress"] = 0.75
        elif self.current_phase == EvolutionPhase.ADAPTATION:
            health_data["evolution_progress"] = 0.5
        else:
            health_data["evolution_progress"] = 0.25
        
        # Check for alerts
        if health_data["integration_health"] < 0.5:
            health_data["alerts"].append("Low integration health")
        
        if self.symbiotic_index < self.config.symbiotic_threshold:
            health_data["alerts"].append("Symbiotic index below threshold")
        
        logger.info(f"Health check: Integration={health_data['integration_health']:.2%}, "
                   f"Evolution={health_data['evolution_progress']:.2%}")
        
        if health_data["alerts"]:
            logger.warning(f"Health alerts: {health_data['alerts']}")
        
        return health_data
    
    def transition_phase(self, new_phase: EvolutionPhase):
        """Transition to a new evolution phase"""
        old_phase = self.current_phase
        self.current_phase = new_phase
        logger.info(f"Phase transition: {old_phase.value} → {new_phase.value}")
    
    def calculate_adaptation_rate(self, metrics: Dict[str, Any]) -> float:
        """Calculate adaptation rate from metrics"""
        rates = []
        
        # NEXUS convergence contributes to adaptation
        if "nexus_convergence" in metrics:
            rates.append(metrics["nexus_convergence"])
        
        # ARQUIMAX success rate contributes to adaptation
        if "arquimax" in metrics and metrics["arquimax"]:
            success_str = metrics["arquimax"].get("success_rate", "0%")
            success_rate = float(success_str.rstrip("%")) / 100
            rates.append(success_rate)
        
        # Average adaptation rate
        if rates:
            return sum(rates) / len(rates)
        
        return self.config.adaptation_level
    
    def update_symbiotic_index(self, adaptation_rate: float):
        """Update symbiotic index based on adaptation rate"""
        # Exponential moving average
        alpha = 0.3
        self.symbiotic_index = alpha * adaptation_rate + (1 - alpha) * self.symbiotic_index
        
        # Update stability score
        if len(self.evolution_history) > 5:
            recent_indices = [h.get("symbiotic_index", 0) for h in self.evolution_history[-5:]]
            variance = sum((x - self.symbiotic_index) ** 2 for x in recent_indices) / len(recent_indices)
            self.stability_score = max(0, 1 - variance)
    
    def get_capability_usage(self, capability: str) -> float:
        """Get usage rate for a capability"""
        # Simulate usage metrics
        usage_map = {
            "task_management": 0.85,
            "document_sync": 0.75,
            "monitoring": 0.90,
            "metrics": 0.80,
            "adaptive_execution": 0.70,
            "connectors": 0.65
        }
        return usage_map.get(capability, 0.5)
    
    def get_capability_efficiency(self, capability: str) -> float:
        """Get efficiency score for a capability"""
        # Simulate efficiency metrics
        efficiency_map = {
            "task_management": 0.88,
            "document_sync": 0.82,
            "monitoring": 0.95,
            "metrics": 0.85,
            "adaptive_execution": 0.78,
            "connectors": 0.72
        }
        return efficiency_map.get(capability, 0.7)
    
    async def apply_evolution_action(self, action: Dict[str, Any]):
        """Apply an evolution action"""
        action_type = action.get("action")
        capability = action.get("capability")
        
        if action_type == "enhance":
            logger.info(f"Enhancing {capability} capability")
            # Increase adaptation level for enhanced capabilities
            if capability in ["adaptive_execution"] and self.nexus:
                self.nexus.config.adaptation_level = min(1.0, self.nexus.config.adaptation_level + 0.1)
        
        elif action_type == "emerge":
            logger.info(f"Emerging new capability: {capability}")
            self.capabilities["active"].append(capability)
    
    async def run_integration_workflow(self):
        """Run complete integration workflow"""
        logger.info("=== Starting Symbiotic Integration Workflow ===")
        
        try:
            # Phase 1: Bootstrap
            logger.info("--- Phase 1: Bootstrap ---")
            await self.symbiotic_init()
            analysis = await self.capability_analysis()
            
            if not analysis["all_required_active"]:
                logger.error("Failed to activate required capabilities")
                return False
            
            # Phase 2: Adaptation
            logger.info("--- Phase 2: Adaptation ---")
            arquimax_ok = await self.arquimax_bridge()
            nexus_ok = await self.nexus_bridge()
            
            if arquimax_ok and nexus_ok:
                self.transition_phase(EvolutionPhase.EVOLUTION)
            else:
                logger.error("Bridge establishment failed")
                return False
            
            # Phase 3: Evolution
            logger.info("--- Phase 3: Evolution ---")
            learning = await self.symbiotic_learning()
            evolution = await self.capability_evolution()
            
            if self.symbiotic_index >= 0.9:
                self.transition_phase(EvolutionPhase.AUTONOMOUS)
            
            # Phase 4: Autonomous
            logger.info("--- Phase 4: Autonomous Operation ---")
            health = await self.symbiotic_health()
            
            # Final report
            logger.info("=== Integration Workflow Complete ===")
            self.print_final_report()
            
            return True
            
        except Exception as e:
            logger.error(f"Integration workflow failed: {e}")
            return False
    
    def print_final_report(self):
        """Print final integration report"""
        logger.info("=== Symbiotic Integration Report ===")
        
        # ARQUIMAX Status
        if self.arquimax:
            metrics = self.arquimax.get_metrics()
            logger.info("ARQUIMAX Status:")
            logger.info(f"  - Capabilities: {len(self.arquimax.capabilities)}/3")
            logger.info(f"  - Task Manager: {'Active' if self.arquimax.task_manager else 'Inactive'}")
            if metrics:
                logger.info(f"  - Success Rate: {metrics.get('success_rate', 'N/A')}")
        
        # NEXUS Status
        if self.nexus:
            logger.info("NEXUS Status:")
            logger.info(f"  - Connectors: {len(self.nexus.active_connectors)}/3")
            logger.info(f"  - Convergence: {self.nexus.convergence_rate:.2%}")
            logger.info(f"  - Active: {'Yes' if self.nexus.is_active else 'No'}")
        
        # Symbiotic Status
        logger.info("Symbiotic Status:")
        logger.info(f"  - Current Phase: {self.current_phase.value}")
        logger.info(f"  - Symbiotic Index: {self.symbiotic_index:.2%}")
        logger.info(f"  - Stability Score: {self.stability_score:.2%}")
        logger.info(f"  - Active Capabilities: {len(self.capabilities['active'])}")

# Integration helper
async def initialize_symbiotic(project_type: str = "git_repository", mode: str = "full"):
    """Initialize symbiotic framework for CHESS project"""
    config = SymbioticConfig(
        project_type=project_type,
        integration_mode=mode,
        adaptation_level=0.8 if mode == "full" else 0.5
    )
    
    framework = SymbioticFramework(config)
    success = await framework.run_integration_workflow()
    
    return framework if success else None

if __name__ == "__main__":
    # Test symbiotic framework
    async def test():
        framework = await initialize_symbiotic()
        
        if framework:
            logger.info("Symbiotic framework initialized successfully")
            
            # Run health check
            health = await framework.symbiotic_health()
            logger.info(f"System health: {health}")
        else:
            logger.error("Failed to initialize symbiotic framework")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    asyncio.run(test())
