#!/bin/bash

# Remove arquivos de log
find . -name "*.log" -type f -delete

# Remove arquivos de backup
find . -name "*.bak" -type f -delete

# Remove caches e backups do docsync
rm -rf .docsync/backup/
rm -rf .docsync/cache/

# Remove caches Python
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -type f -delete
find . -name "*.pyo" -type f -delete
find . -name "*.pyd" -type f -delete

# Remove arquivos de sistema
find . -name ".DS_Store" -type f -delete
find . -name "*.swp" -type f -delete
find . -name "*.swo" -type f -delete

# Remove caches de teste
rm -rf .pytest_cache/
rm -rf .coverage
rm -rf htmlcov/

# Remove diretórios temporários
find . -name "temp" -type d -exec rm -rf {} +
find . -name "tmp" -type d -exec rm -rf {} +

# Remove caches específicos
rm -rf .aeon_cache/
rm -rf cultural_cache/
rm -rf narrative_cache/
rm -rf .cultural_backup/
rm -rf .narrative_backup/

echo "Limpeza concluída!"
