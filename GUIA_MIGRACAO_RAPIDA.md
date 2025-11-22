# 🚀 Guia Rápido de Migração

## ⚡ Passos Rápidos

### 1️⃣ Executar Script de Preparação
```bash
cd /Users/jx/WORKSPACE/PROJECTS/CHESS
./migrate_to_new_repo.sh
```

### 2️⃣ Criar Novo Repositório no GitHub

1. Acesse: **https://github.com/new**
2. **Nome do repositório:** (escolha um)
   - `aeon-chess-v2`
   - `chess-educational-platform`
   - `cultural-chess-ai`
3. **Descrição:** "Revolutionary chess platform with AI, cultural narratives, and gamification"
4. **Visibilidade:** Public ou Private
5. ⚠️ **IMPORTANTE:** NÃO marque nenhuma opção de inicialização (sem README, .gitignore ou licença)
6. Clique em **"Create repository"**

### 3️⃣ Atualizar Remote e Fazer Push

**Opção A - Remover e Adicionar:**
```bash
git remote remove origin
git remote add origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

**Opção B - Atualizar URL (mais rápido):**
```bash
git remote set-url origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

### 4️⃣ Atualizar Referências no Projeto

Após o push bem-sucedido, atualize:

**package.json:**
```bash
# Editar a linha 49 e 56-58
"repository": {
    "type": "git",
    "url": "git+https://github.com/SEU_USUARIO/NOME_DO_REPO.git"
}
```

**README.md:**
- Atualizar links do repositório (se houver)

---

## ✅ Checklist

- [ ] Executar `./migrate_to_new_repo.sh`
- [ ] Criar novo repositório no GitHub
- [ ] Atualizar remote com novo repositório
- [ ] Fazer push: `git push -u origin main`
- [ ] Verificar no GitHub que tudo foi enviado
- [ ] Atualizar `package.json` com novo URL
- [ ] Testar clone do novo repositório (opcional)

---

## 🔐 Verificar SSH (se necessário)

Se der erro de autenticação:

```bash
# Testar conexão SSH
ssh -T git@github.com

# Se não funcionar, adicionar chave SSH
ssh-add ~/.ssh/id_ed25519
```

---

## 📊 Status Atual

- **Repositório atual:** `SH1W4/eon-chess-v1` (sinalizado)
- **Branch:** `main`
- **Arquivos não rastreados:** 3 arquivos
- **Arquivos modificados:** 3 arquivos

---

## 🆘 Problemas Comuns

### Erro: "Permission denied (publickey)"
```bash
ssh-add ~/.ssh/id_ed25519
# Ou gerar nova chave se necessário
ssh-keygen -t ed25519 -C "seu_email@example.com"
```

### Erro: "Repository not found"
- Verifique se o repositório foi criado
- Verifique se o nome do usuário está correto
- Verifique permissões SSH no GitHub

### Erro: "Updates were rejected"
```bash
# Apenas na primeira vez, se necessário:
git push -u origin main --force
```

---

**✨ Todo o histórico de commits será preservado!**

