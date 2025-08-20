#!/usr/bin/env python3
"""
🧪 Teste Simples da API Python
"""

import requests
import time

def test_api():
    """Testar se a API está funcionando"""
    try:
        print("🧪 Testando API Python...")
        
        # Testar endpoint de saúde
        response = requests.get('http://localhost:5000/health', timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"📊 Resposta: {response.json()}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ API não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_api()
