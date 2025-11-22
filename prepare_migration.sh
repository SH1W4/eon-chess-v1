#!/bin/bash

# 🔄 Script de Preparação para Migração de Repositório
# Este script apenas prepara o repositório, sem fazer commit automático

set -e

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔄 Preparação para Migração de Repositório${NC}"
echo -e "${BLUE}===========================================${NC}\n"

# Verificar diretório
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Execute no diretório raiz do projeto${NC}"
    exit 1
fi

# Mostrar status
echo -e "${YELLOW}📊 Status atual do Git:${NC}"
git status --short

echo -e "\n${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}📝 INSTRUÇÕES PARA MIGRAÇÃO:${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}1. CRIAR NOVO REPOSITÓRIO NO GITHUB:${NC}"
echo -e "   ${GREEN}https://github.com/new${NC}"
echo -e "   - Nome: aeon-chess-v2 (ou outro)"
echo -e "   - ${RED}NÃO${NC} inicialize com README/.gitignore/licença\n"

echo -e "${YELLOW}2. APÓS CRIAR O REPOSITÓRIO, EXECUTE:${NC}\n"

echo -e "${GREEN}# Opção A - Remover e adicionar novo remote:${NC}"
echo -e "git remote remove origin"
echo -e "git remote add origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git"
echo -e "git push -u origin main\n"

echo -e "${GREEN}# Opção B - Atualizar URL do remote:${NC}"
echo -e "git remote set-url origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git"
echo -e "git push -u origin main\n"

echo -e "${YELLOW}3. ANTES DO PUSH, FAÇA COMMIT DAS MUDANÇAS:${NC}"
echo -e "${GREEN}git add -A${NC}"
echo -e "${GREEN}git commit -m \"docs: Preparação para migração de repositório\"${NC}\n"

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Preparação concluída!${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

# Mostrar remote atual
echo -e "${YELLOW}🔗 Remote atual:${NC}"
git remote -v

echo -e "\n${YELLOW}📜 Últimos 5 commits (serão preservados):${NC}"
git log --oneline -5

echo -e "\n${GREEN}✨ Todo o histórico será preservado!${NC}\n"

