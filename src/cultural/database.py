"""
Banco de dados de referências culturais para o xadrez.
"""

from typing import Dict, List
import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CulturalReference:
    """Referência cultural para uma peça ou conceito do xadrez."""
    name: str  # Nome do elemento
    region: str  # Região cultural
    era: str  # Era histórica
    description: str  # Descrição cultural
    historical_significance: str  # Significado histórico
    variations: List[str]  # Variações culturais
    sources: List[str]  # Fontes de referência

class CulturalDatabase:
    """Gerencia o banco de dados de referências culturais."""
    
    def __init__(self):
        self.references: Dict[str, List[CulturalReference]] = {}
        self.regions: List[str] = []
        self.eras: List[str] = []
        
    def load_database(self, filepath: str) -> bool:
        """
        Carrega banco de dados de referências culturais.
        Retorna True se o carregamento foi bem-sucedido.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Carrega regiões e eras disponíveis
            self.regions = data.get('regions', [])
            self.eras = data.get('eras', [])
            
            # Carrega referências
            references_data = data.get('references', {})
            for key, refs in references_data.items():
                self.references[key] = [
                    CulturalReference(**ref) for ref in refs
                ]
            
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False
            
    def get_reference(self, element: str, region: str, era: str) -> CulturalReference:
        """Retorna uma referência cultural específica."""
        refs = self.references.get(element, [])
        for ref in refs:
            if ref.region == region and ref.era == era:
                return ref
        return None
        
    def get_all_references(self, element: str) -> List[CulturalReference]:
        """Retorna todas as referências para um elemento."""
        return self.references.get(element, [])
        
    def get_regional_references(self, region: str) -> Dict[str, List[CulturalReference]]:
        """Retorna todas as referências de uma região específica."""
        regional_refs = {}
        for element, refs in self.references.items():
            region_refs = [ref for ref in refs if ref.region == region]
            if region_refs:
                regional_refs[element] = region_refs
        return regional_refs
        
    def get_era_references(self, era: str) -> Dict[str, List[CulturalReference]]:
        """Retorna todas as referências de uma era específica."""
        era_refs = {}
        for element, refs in self.references.items():
            era_refs_list = [ref for ref in refs if ref.era == era]
            if era_refs_list:
                era_refs[element] = era_refs_list
        return era_refs
        
    def add_reference(self, element: str, reference: CulturalReference):
        """Adiciona uma nova referência cultural."""
        if element not in self.references:
            self.references[element] = []
            
        # Verifica se já existe uma referência similar
        existing = False
        for i, ref in enumerate(self.references[element]):
            if ref.region == reference.region and ref.era == reference.era:
                self.references[element][i] = reference
                existing = True
                break
                
        if not existing:
            self.references[element].append(reference)
            
        # Atualiza listas de regiões e eras se necessário
        if reference.region not in self.regions:
            self.regions.append(reference.region)
        if reference.era not in self.eras:
            self.eras.append(reference.era)
            
    def save_database(self, filepath: str):
        """Salva o banco de dados em disco."""
        data = {
            'regions': self.regions,
            'eras': self.eras,
            'references': {
                element: [
                    {
                        'name': ref.name,
                        'region': ref.region,
                        'era': ref.era,
                        'description': ref.description,
                        'historical_significance': ref.historical_significance,
                        'variations': ref.variations,
                        'sources': ref.sources
                    }
                    for ref in refs
                ]
                for element, refs in self.references.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def search_references(self, query: str) -> List[CulturalReference]:
        """Pesquisa referências culturais."""
        query = query.lower()
        results = []
        
        for element_refs in self.references.values():
            for ref in element_refs:
                if (query in ref.name.lower() or
                    query in ref.description.lower() or
                    query in ref.historical_significance.lower()):
                    results.append(ref)
                    
        return results
        
    def get_available_variations(self, element: str) -> List[str]:
        """Retorna todas as variações culturais disponíveis para um elemento."""
        variations = set()
        for ref in self.references.get(element, []):
            variations.update(ref.variations)
        return list(variations)
        
    def get_related_references(self, reference: CulturalReference) -> List[CulturalReference]:
        """Retorna referências culturais relacionadas."""
        related = []
        
        # Procura referências da mesma região ou era
        for element_refs in self.references.values():
            for ref in element_refs:
                if ref != reference and (
                    ref.region == reference.region or 
                    ref.era == reference.era
                ):
                    related.append(ref)
                    
        return related
