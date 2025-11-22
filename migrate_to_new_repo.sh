#!/bin/bash

# 🔄 Script de Migração para Novo Repositório GitHub
# Data: $(date +%Y-%m-%d)
# 
# Este script prepara o projeto para migração para um novo repositório GitHub

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Script de Migração de Repositório${NC}"
echo -e "${BLUE}=====================================${NC}\n"

# Verificar se está no diretório correto
if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Erro: Execute este script no diretório raiz do projeto CHESS${NC}"
    exit 1
fi

# 1. Verificar status do Git
echo -e "${YELLOW}📊 Verificando status do Git...${NC}"
git status

# 2. Adicionar arquivos específicos (evitando arquivos com instruções de token)
echo -e "\n${YELLOW}📦 Adicionando arquivos de documentação...${NC}"
git add ANALISE_PROJETO_COMPLETA_20251105.md
git add RESUMO_ANALISE_EXECUTIVA.md
git add MIGRACAO_REPOSITORIO.md
git add GUIA_MIGRACAO_RAPIDA.md
git add migrate_to_new_repo.sh
# Arquivos de configuração (opcional - adicione se necessário)
# git add CONFIGURAR_SH1W4.md
# git add INSTRUCOES_TOKEN.md
# git add SCRIPT_CONFIGURAR_SH1W4.sh

# 3. Verificar se há mudanças para commit
if git diff --staged --quiet; then
    echo -e "${GREEN}✅ Nenhuma mudança para commitar${NC}"
else
    echo -e "${YELLOW}💾 Criando commit das mudanças...${NC}"
    git commit -m "docs: Preparação para migração de repositório

- Adicionar análises do projeto
- Adicionar instruções de configuração
- Atualizar documentação de migração"
    echo -e "${GREEN}✅ Commit criado com sucesso${NC}"
fi

# 4. Mostrar remote atual
echo -e "\n${YELLOW}🔗 Remote atual:${NC}"
git remote -v

# 5. Solicitar novo repositório
echo -e "\n${BLUE}════════════════════════════════════════${NC}"
echo -e "${BLUE}📝 PRÓXIMOS PASSOS MANUAIS:${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

echo -e "${YELLOW}1. Crie um novo repositório no GitHub:${NC}"
echo -e "   - Acesse: ${GREEN}https://github.com/new${NC}"
echo -e "   - Nome sugerido: ${GREEN}aeon-chess-v2${NC} ou ${GREEN}chess-educational-platform${NC}"
echo -e "   - ${RED}NÃO${NC} inicialize com README, .gitignore ou licença\n"

echo -e "${YELLOW}2. Após criar o repositório, execute:${NC}"
echo -e "${GREEN}   git remote remove origin${NC}"
echo -e "${GREEN}   git remote add origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git${NC}"
echo -e "${GREEN}   git push -u origin main${NC}\n"

echo -e "${YELLOW}3. Ou use este comando completo (substitua os valores):${NC}"
echo -e "${GREEN}   git remote set-url origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git${NC}"
echo -e "${GREEN}   git push -u origin main${NC}\n"

echo -e "${BLUE}════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Preparação concluída!${NC}"
echo -e "${BLUE}════════════════════════════════════════${NC}\n"

# 6. Mostrar histórico de commits (últimos 5)
echo -e "${YELLOW}📜 Últimos 5 commits (serão preservados):${NC}"
git log --oneline -5

echo -e "\n${GREEN}✨ Todo o histórico será preservado na migração!${NC}\n"

