# CHESS Project - GitHub Pages

Esta pasta contém os arquivos para o GitHub Pages do projeto CHESS.

## Como ativar o GitHub Pages

1. Faça push das mudanças para o GitHub:
   ```bash
   git push origin main
   ```

2. Vá para **Settings** no repositório GitHub

3. Role até a seção **Pages**

4. Em **Source**, selecione **Deploy from a branch**

5. Em **Branch**, selecione **main** e **/docs**

6. Clique em **Save**

O site estará disponível em:
- https://[seu-usuario].github.io/[nome-do-repo]/
- Exemplo: https://neo-sh1w4.github.io/aeon-chess/

## Estrutura

- `index.html` - Landing page principal
- `favicon.svg` - Ícone do site
- `_config.yml` - Configuração do Jekyll (opcional)
- `CNAME` - Para domínio customizado (opcional)

## Atualização

Para atualizar o site, simplesmente faça commit das mudanças na pasta `docs` e faça push para o GitHub. As mudanças serão refletidas automaticamente em alguns minutos.
