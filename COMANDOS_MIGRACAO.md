# 🚀 Comandos para Migração de Repositório

## ⚡ Passo a Passo Rápido

### 1️⃣ Criar Novo Repositório no GitHub

1. Acesse: **https://github.com/new**
2. **Nome:** `aeon-chess-v2` (ou outro nome de sua escolha)
3. **Descrição:** "Revolutionary chess platform with AI, cultural narratives, and gamification"
4. **Visibilidade:** Public ou Private
5. ⚠️ **IMPORTANTE:** NÃO marque nenhuma opção de inicialização
6. Clique em **"Create repository"**

---

### 2️⃣ Fazer Commit das Mudanças Locais

```bash
cd /Users/jx/WORKSPACE/PROJECTS/CHESS
git add -A
git commit -m "docs: Preparação para migração de repositório"
```

---

### 3️⃣ Atualizar Remote e Fazer Push

**Substitua `SEU_USUARIO` e `NOME_DO_REPO` pelos valores reais:**

```bash
# Remover remote antigo
git remote remove origin

# Adicionar novo remote
git remote add origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git

# Fazer push (todo o histórico será preservado)
git push -u origin main
```

**OU, se preferir atualizar a URL:**

```bash
git remote set-url origin git@github.com:SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

---

### 4️⃣ Atualizar Referências no Projeto (Opcional)

Após o push bem-sucedido, atualize o `package.json`:

```bash
# Editar package.json (linha 49 e 56-58)
# Substituir:
# "url": "git+https://github.com/SH1W4/eon-chess-v1.git"
# Por:
# "url": "git+https://github.com/SEU_USUARIO/NOME_DO_REPO.git"
```

---

## 🔐 Se Der Erro de Autenticação

### Para SSH:
```bash
# Testar conexão
ssh -T git@github.com

# Se não funcionar, adicionar chave
ssh-add ~/.ssh/id_ed25519
```

### Para HTTPS (com Personal Access Token):
```bash
# Mudar remote para HTTPS
git remote set-url origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git

# Fazer push (solicitará username e token)
git push -u origin main
# Username: SEU_USUARIO
# Password: [cole seu Personal Access Token aqui]
```

**Criar token:** https://github.com/settings/tokens
- Permissão: `repo` (full control)

---

## ✅ Verificação

Após o push, verifique no GitHub:
- Todos os arquivos foram enviados
- Histórico de commits está completo
- Branch `main` está atualizada

---

## 📊 Status Atual

- **Repositório atual:** `SH1W4/eon-chess-v1` (sinalizado)
- **Branch:** `main`
- **Commits locais:** 5 commits recentes
- **Arquivos modificados:** 3
- **Arquivos novos:** 5

**✨ Todo o histórico será preservado na migração!**

