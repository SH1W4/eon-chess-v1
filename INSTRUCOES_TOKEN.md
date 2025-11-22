# 🔐 Instruções para Criar Personal Access Token

**Data:** 05/11/2025  
**Conta:** SH1W4  
**Repositório:** SH1W4/eon-chess-v1

---

## ✅ Passo 1: Remote Configurado

O remote já está configurado para HTTPS:
```
origin  https://github.com/SH1W4/eon-chess-v1.git
```

---

## 📝 Passo 2: Criar Personal Access Token

### Instruções:

1. **Acesse (com conta SH1W4):**
   ```
   https://github.com/settings/tokens
   ```
   
   ⚠️ **IMPORTANTE:** Faça login com a conta **SH1W4**, não NEO-SH1W4!

2. **Clique em:**
   - "Generate new token" > "Generate new token (classic)"

3. **Configure o token:**
   - **Note:** `eon-chess-v1-push`
   - **Expiration:** Escolha (90 dias, 1 ano, ou sem expiração)
   - **Scopes:** Marque apenas:
     - ✅ `repo` (full control of private repositories)
       - Isso inclui: repo:status, repo_deployment, public_repo, repo:invite, security_events

4. **Clique em:** "Generate token"

5. **COPIE O TOKEN IMEDIATAMENTE!**
   - ⚠️ Você só verá o token uma vez
   - Formato: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## 🚀 Passo 3: Fazer Push

Após criar o token, execute:

```bash
cd /Users/jx/WORKSPACE/PROJECTS/CHESS
git push -u origin main
```

Quando solicitado:
- **Username:** `SH1W4`
- **Password:** Cole o token (não sua senha do GitHub!)

O macOS Keychain vai salvar suas credenciais automaticamente.

---

## ✅ Verificação

Após o push bem-sucedido, você verá:
```
Enumerating objects: ...
Writing objects: ...
To https://github.com/SH1W4/eon-chess-v1.git
 * [new branch]      main -> main
```

---

## 🔍 Troubleshooting

### Erro: Authentication failed
- Verifique se está usando a conta **SH1W4** (não NEO-SH1W4)
- Confirme que o token tem permissão `repo`
- Tente criar um novo token

### Erro: Permission denied
- Verifique se o token não expirou
- Confirme que você tem acesso ao repositório SH1W4/eon-chess-v1

### Token não está sendo aceito
- Certifique-se de copiar o token completo (começa com `ghp_`)
- Não adicione espaços extras ao colar
- Se necessário, limpe credenciais salvas:
  ```bash
  git credential-osxkeychain erase
  host=github.com
  protocol=https
  ```

---

## 📋 Checklist

- [ ] Login feito com conta SH1W4
- [ ] Token criado com permissão `repo`
- [ ] Token copiado e salvo em local seguro
- [ ] Remote configurado para HTTPS
- [ ] Push realizado com sucesso

---

**Criado por:** WARP Symbiotic Agent  
**Status:** Aguardando criação do token


