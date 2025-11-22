#!/bin/bash
# Script para configurar autenticação com conta SH1W4

echo "🔐 Configurando autenticação para conta SH1W4"
echo ""

# Verificar se está no diretório correto
if [ ! -d ".git" ]; then
    echo "❌ Erro: Execute este script no diretório do projeto CHESS"
    exit 1
fi

# Opção escolhida
echo "Escolha uma opção:"
echo "1) Usar HTTPS com Personal Access Token (mais fácil)"
echo "2) Configurar SSH com nova chave para SH1W4"
echo "3) Usar GitHub CLI (recomendado se já tem gh instalado)"
echo ""
read -p "Digite o número da opção (1-3): " opcao

case $opcao in
    1)
        echo ""
        echo "📝 Configurando HTTPS..."
        git remote set-url origin https://github.com/SH1W4/eon-chess-v1.git
        
        echo ""
        echo "✅ Remote atualizado para HTTPS"
        echo ""
        echo "📋 Próximos passos:"
        echo "1. Crie um Personal Access Token em: https://github.com/settings/tokens"
        echo "   - Use a conta SH1W4 para fazer login"
        echo "   - Permissões: repo (full control)"
        echo "2. Execute: git push -u origin main"
        echo "3. Quando solicitado:"
        echo "   - Username: SH1W4"
        echo "   - Password: [cole o token aqui]"
        ;;
        
    2)
        echo ""
        echo "🔑 Configurando SSH para conta SH1W4..."
        
        # Gerar nova chave SSH
        echo "Gerando nova chave SSH para SH1W4..."
        ssh-keygen -t ed25519 -C "sh1w4@github" -f ~/.ssh/id_ed25519_sh1w4
        
        # Adicionar ao ssh-agent
        echo "Adicionando chave ao ssh-agent..."
        eval "$(ssh-agent -s)"
        ssh-add ~/.ssh/id_ed25519_sh1w4
        
        # Configurar ~/.ssh/config
        echo "Configurando ~/.ssh/config..."
        if [ ! -f ~/.ssh/config ]; then
            touch ~/.ssh/config
            chmod 600 ~/.ssh/config
        fi
        
        cat >> ~/.ssh/config << EOF

# Conta SH1W4
Host github-sh1w4
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_sh1w4
    IdentitiesOnly yes
EOF
        
        # Atualizar remote
        git remote set-url origin git@github-sh1w4:SH1W4/eon-chess-v1.git
        
        echo ""
        echo "✅ Configuração SSH concluída!"
        echo ""
        echo "📋 Próximos passos:"
        echo "1. Copie a chave pública:"
        echo "   cat ~/.ssh/id_ed25519_sh1w4.pub"
        echo ""
        echo "2. Adicione no GitHub (conta SH1W4):"
        echo "   https://github.com/settings/keys"
        echo ""
        echo "3. Teste a conexão:"
        echo "   ssh -T git@github-sh1w4"
        echo ""
        echo "4. Faça o push:"
        echo "   git push -u origin main"
        ;;
        
    3)
        echo ""
        echo "🔐 Configurando GitHub CLI..."
        echo ""
        echo "Você será redirecionado para autenticar no navegador."
        echo "IMPORTANTE: Use a conta SH1W4 para fazer login!"
        echo ""
        read -p "Pressione Enter para continuar..."
        
        gh auth login --hostname github.com --web
        
        echo ""
        echo "✅ Autenticação concluída!"
        echo ""
        echo "Verificando autenticação:"
        gh auth status
        
        echo ""
        echo "📋 Próximo passo:"
        echo "   git push -u origin main"
        ;;
        
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "✅ Configuração concluída!"
echo ""
echo "Remote atual:"
git remote -v


