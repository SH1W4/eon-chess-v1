# 🔐 Configurar Autenticação para Conta SH1W4

**Data:** 05/11/2025  
**Objetivo:** Configurar acesso ao repositório `SH1W4/eon-chess-v1`

---

## ✅ Status Atual

- [x] Remote atualizado: `git@github.com:SH1W4/eon-chess-v1.git`
- [x] Conta NEO-SH1W4 desautenticada do GitHub CLI
- [ ] Autenticação SH1W4 configurada

---

## 🔧 Opções de Autenticação

### **Opção 1: SSH com Chave Específica (Recomendado)**

Se você já tem uma chave SSH para a conta SH1W4:

**1. Configurar SSH para usar conta SH1W4:**

```bash
# Editar ~/.ssh/config
nano ~/.ssh/config
```

Adicione:
```
Host github-sh1w4
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_sh1w4
    IdentitiesOnly yes
```

**2. Atualizar remote:**
```bash
cd /Users/jx/WORKSPACE/PROJECTS/CHESS
git remote set-url origin git@github-sh1w4:SH1W4/eon-chess-v1.git
```

**3. Testar conexão:**
```bash
ssh -T git@github-sh1w4
```

**4. Fazer push:**
```bash
git push -u origin main
```

---

### **Opção 2: GitHub CLI com Conta SH1W4**

**1. Autenticar com GitHub CLI:**
```bash
gh auth login --hostname github.com
# Selecione: GitHub.com
# Escolha: Login with a web browser
# Use a conta SH1W4 para autenticar
```

**2. Verificar autenticação:**
```bash
gh auth status
```

**3. Fazer push:**
```bash
git push -u origin main
```

---

### **Opção 3: Personal Access Token (HTTPS)**

**1. Criar Personal Access Token:**
- Acesse: https://github.com/settings/tokens (com conta SH1W4)
- Clique em "Generate new token" > "Generate new token (classic)"
- Nome: `eon-chess-v1-push`
- Permissões: `repo` (full control)
- Copie o token gerado

**2. Configurar remote para HTTPS:**
```bash
cd /Users/jx/WORKSPACE/PROJECTS/CHESS
git remote set-url origin https://github.com/SH1W4/eon-chess-v1.git
```

**3. Fazer push (usar token como senha):**
```bash
git push -u origin main
# Username: SH1W4
# Password: [cole o token aqui]
```

**4. Salvar credenciais (opcional):**
```bash
git config --global credential.helper osxkeychain
# Na próxima vez, o token será salvo automaticamente
```

---

### **Opção 4: SSH com Múltiplas Contas**

Se você precisa usar ambas as contas:

**1. Gerar nova chave SSH para SH1W4:**
```bash
ssh-keygen -t ed25519 -C "sh1w4@github" -f ~/.ssh/id_ed25519_sh1w4
```

**2. Adicionar chave ao ssh-agent:**
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519_sh1w4
```

**3. Copiar chave pública:**
```bash
cat ~/.ssh/id_ed25519_sh1w4.pub
```

**4. Adicionar no GitHub (conta SH1W4):**
- Acesse: https://github.com/settings/keys (com conta SH1W4)
- Clique em "New SSH key"
- Cole a chave pública
- Salve

**5. Configurar ~/.ssh/config:**
```bash
# Conta NEO-SH1W4 (padrão)
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519

# Conta SH1W4
Host github-sh1w4
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_sh1w4
    IdentitiesOnly yes
```

**6. Atualizar remote:**
```bash
git remote set-url origin git@github-sh1w4:SH1W4/eon-chess-v1.git
```

**7. Testar e fazer push:**
```bash
ssh -T git@github-sh1w4
git push -u origin main
```

---

## 📋 Checklist Rápido

### Para SSH (Opção 1 ou 4):
- [ ] Chave SSH configurada no GitHub (conta SH1W4)
- [ ] ~/.ssh/config configurado
- [ ] Remote atualizado com host correto
- [ ] Teste de conexão bem-sucedido
- [ ] Push realizado

### Para GitHub CLI (Opção 2):
- [ ] Autenticado com conta SH1W4
- [ ] `gh auth status` mostra SH1W4
- [ ] Push realizado

### Para HTTPS/Token (Opção 3):
- [ ] Token criado com permissão `repo`
- [ ] Remote configurado para HTTPS
- [ ] Push realizado com token
- [ ] Credenciais salvas (opcional)

---

## 🔍 Verificações

```bash
# Verificar remote atual
git remote -v

# Verificar autenticação SSH
ssh -T git@github.com
# ou
ssh -T git@github-sh1w4

# Verificar autenticação GitHub CLI
gh auth status

# Verificar permissões no repositório
gh api repos/SH1W4/eon-chess-v1 --jq '.permissions'
```

---

## 🎯 Comando Rápido (Depois de Configurar)

Após configurar a autenticação, execute:

```bash
cd /Users/jx/WORKSPACE/PROJECTS/CHESS
git push -u origin main
```

---

## ⚠️ Importante

- Certifique-se de estar autenticado com a conta **SH1W4** (não NEO-SH1W4)
- O repositório `SH1W4/eon-chess-v1` já existe e está vazio
- Você precisa ter permissão de escrita no repositório

---

**Criado por:** WARP Symbiotic Agent  
**Status:** Aguardando configuração de autenticação


