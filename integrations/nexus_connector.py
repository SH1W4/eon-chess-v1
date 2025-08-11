"""
NEXUS Connector for CHESS Project
Implements document synchronization and adaptive execution
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class NexusConfig:
    """Configuration for NEXUS integration"""
    sync_mode: str = "adaptive"  # adaptive, full, partial
    document_path: str = "./docs"
    connector_types: List[str] = None
    adaptation_level: float = 0.8
    health_check_interval: int = 3600
    
    def __post_init__(self):
        if self.connector_types is None:
            self.connector_types = ["document_sync", "adaptive_execution", "connectors"]

class NexusConnector:
    """Main NEXUS connector for CHESS integration"""
    
    def __init__(self, config: Optional[NexusConfig] = None):
        self.config = config or NexusConfig()
        self.active_connectors = {}
        self.sync_status = {}
        self.convergence_rate = 0.0
        self.is_active = False
        
    async def activate_all(self):
        """Activate all NEXUS subsystems"""
        logger.info("Activating NEXUS subsystems...")
        
        # Activate connectors based on configuration
        for connector_type in self.config.connector_types:
            await self.activate_connector(connector_type)
        
        self.is_active = True
        logger.info(f"NEXUS activated with {len(self.active_connectors)} connectors")
        return True
    
    async def activate_connector(self, connector_type: str):
        """Activate a specific connector"""
        if connector_type == "document_sync":
            self.active_connectors[connector_type] = DocumentSyncConnector(self.config)
        elif connector_type == "adaptive_execution":
            self.active_connectors[connector_type] = AdaptiveExecutionConnector(self.config)
        elif connector_type == "connectors":
            self.active_connectors[connector_type] = ConnectorManager(self.config)
        
        await self.active_connectors[connector_type].initialize()
        logger.info(f"Activated connector: {connector_type}")
    
    async def adaptive_execution(self, task: Dict[str, Any]):
        """Execute task with adaptive optimization"""
        if "adaptive_execution" not in self.active_connectors:
            raise RuntimeError("Adaptive execution connector not active")
        
        return await self.active_connectors["adaptive_execution"].execute(task)
    
    async def convergence(self):
        """Calculate and update convergence metrics"""
        total_health = 0
        active_count = 0
        
        for name, connector in self.active_connectors.items():
            if hasattr(connector, 'get_health'):
                health = await connector.get_health()
                total_health += health
                active_count += 1
        
        if active_count > 0:
            self.convergence_rate = total_health / active_count
        
        logger.info(f"Convergence rate: {self.convergence_rate:.2%}")
        return self.convergence_rate
    
    async def validation(self):
        """Validate all active connectors"""
        validation_results = {}
        
        for name, connector in self.active_connectors.items():
            if hasattr(connector, 'validate'):
                validation_results[name] = await connector.validate()
            else:
                validation_results[name] = True
        
        all_valid = all(validation_results.values())
        logger.info(f"Validation {'passed' if all_valid else 'failed'}: {validation_results}")
        return all_valid
    
    async def finalize(self):
        """Finalize NEXUS operations"""
        logger.info("Finalizing NEXUS operations...")
        
        # Save sync status
        status_file = os.path.join(self.config.document_path, "nexus_status.json")
        with open(status_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "convergence_rate": self.convergence_rate,
                "active_connectors": list(self.active_connectors.keys()),
                "sync_status": self.sync_status
            }, f, indent=2)
        
        # Shutdown connectors
        for connector in self.active_connectors.values():
            if hasattr(connector, 'shutdown'):
                await connector.shutdown()
        
        self.is_active = False
        logger.info("NEXUS finalized successfully")
        return True

class DocumentSyncConnector:
    """Document synchronization connector"""
    
    def __init__(self, config: NexusConfig):
        self.config = config
        self.synced_documents = set()
        self.sync_queue = asyncio.Queue()
        
    async def initialize(self):
        """Initialize document sync connector"""
        # Scan for documents to sync
        if os.path.exists(self.config.document_path):
            for root, dirs, files in os.walk(self.config.document_path):
                for file in files:
                    if file.endswith(('.md', '.json', '.yaml')):
                        doc_path = os.path.join(root, file)
                        await self.sync_queue.put(doc_path)
        
        logger.info(f"Document sync initialized with {self.sync_queue.qsize()} documents")
    
    async def sync_document(self, doc_path: str):
        """Sync a single document"""
        # Simulate document synchronization
        self.synced_documents.add(doc_path)
        logger.debug(f"Synced document: {doc_path}")
        return True
    
    async def get_health(self):
        """Get health score of document sync"""
        if self.sync_queue.qsize() == 0:
            return 1.0
        
        synced_ratio = len(self.synced_documents) / (len(self.synced_documents) + self.sync_queue.qsize())
        return synced_ratio
    
    async def validate(self):
        """Validate document sync status"""
        return len(self.synced_documents) > 0

class AdaptiveExecutionConnector:
    """Adaptive execution optimization connector"""
    
    def __init__(self, config: NexusConfig):
        self.config = config
        self.execution_history = []
        self.optimization_cache = {}
        
    async def initialize(self):
        """Initialize adaptive execution"""
        logger.info(f"Adaptive execution initialized with level {self.config.adaptation_level}")
    
    async def execute(self, task: Dict[str, Any]):
        """Execute task with adaptive optimization"""
        task_id = task.get('id', 'unknown')
        
        # Check optimization cache
        if task_id in self.optimization_cache:
            logger.debug(f"Using cached optimization for task {task_id}")
            optimization = self.optimization_cache[task_id]
        else:
            # Generate new optimization
            optimization = await self.optimize_task(task)
            self.optimization_cache[task_id] = optimization
        
        # Execute with optimization
        result = await self.run_optimized_task(task, optimization)
        
        # Record execution
        self.execution_history.append({
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "optimization": optimization,
            "success": result.get('success', False)
        })
        
        return result
    
    async def optimize_task(self, task: Dict[str, Any]):
        """Generate optimization for task"""
        optimization = {
            "parallel": task.get('size', 1) > 10,
            "cache_enabled": True,
            "adaptation_level": self.config.adaptation_level
        }
        return optimization
    
    async def run_optimized_task(self, task: Dict[str, Any], optimization: Dict[str, Any]):
        """Run task with optimizations applied"""
        # Simulate optimized execution
        await asyncio.sleep(0.1)  # Simulate work
        
        return {
            "success": True,
            "task_id": task.get('id'),
            "optimization_applied": optimization
        }
    
    async def get_health(self):
        """Get health score of adaptive execution"""
        if not self.execution_history:
            return 1.0
        
        recent_executions = self.execution_history[-10:]
        success_count = sum(1 for e in recent_executions if e.get('success', False))
        return success_count / len(recent_executions)
    
    async def validate(self):
        """Validate adaptive execution"""
        return self.config.adaptation_level > 0

class ConnectorManager:
    """Manages dynamic connectors"""
    
    def __init__(self, config: NexusConfig):
        self.config = config
        self.connectors = {}
        
    async def initialize(self):
        """Initialize connector manager"""
        logger.info("Connector manager initialized")
    
    async def add_connector(self, name: str, connector: Any):
        """Add a new connector dynamically"""
        self.connectors[name] = connector
        logger.info(f"Added connector: {name}")
    
    async def remove_connector(self, name: str):
        """Remove a connector"""
        if name in self.connectors:
            del self.connectors[name]
            logger.info(f"Removed connector: {name}")
    
    async def get_health(self):
        """Get health score of connector manager"""
        return 1.0 if self.connectors else 0.5
    
    async def validate(self):
        """Validate connector manager"""
        return True

# Integration helper functions
async def initialize_nexus(project_type: str = "git_repository", mode: str = "full"):
    """Initialize NEXUS for CHESS project"""
    config = NexusConfig(
        sync_mode=mode,
        document_path="./docs",
        adaptation_level=0.8 if mode == "full" else 0.5
    )
    
    connector = NexusConnector(config)
    await connector.activate_all()
    
    return connector

if __name__ == "__main__":
    # Test NEXUS connector
    async def test():
        connector = await initialize_nexus()
        
        # Test adaptive execution
        test_task = {
            "id": "test_001",
            "type": "analysis",
            "size": 15
        }
        result = await connector.adaptive_execution(test_task)
        print(f"Task result: {result}")
        
        # Check convergence
        convergence = await connector.convergence()
        print(f"Convergence rate: {convergence:.2%}")
        
        # Validate
        is_valid = await connector.validation()
        print(f"Validation: {'Passed' if is_valid else 'Failed'}")
        
        # Finalize
        await connector.finalize()
    
    asyncio.run(test())
