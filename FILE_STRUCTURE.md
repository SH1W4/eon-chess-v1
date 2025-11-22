# AEON CHESS - Estrutura de Arquivos

## 📁 Organização Atual

### `/public` - Assets Públicos (Servidos Estaticamente)
```
public/
├── landing.html          # ✅ Landing page principal (acessível em /)
├── dashboard.html        # ✅ Hub de protótipos
├── favicon.ico
├── css/
│   └── chess-theme.css   # ✅ Estilos consolidados
├── images/               # ✅ Assets da landing page
└── web/                  # ✅ Protótipos e demos
    ├── pages/            # HTMLs de protótipos
    ├── styles/           # Estilos dos protótipos
    └── js/               # Scripts dos protótipos
```

### `/src` - Código Fonte
```
src/
├── pages/                # Páginas Next.js
│   ├── index.tsx         # ✅ Redireciona para /landing.html
│   ├── _app.tsx
│   └── _document.tsx
├── api/                  # Backend FastAPI
│   ├── main.py           # ✅ API com documentação Swagger
│   └── requirements.txt
├── core/                 # Lógica de xadrez
│   └── board/
│       ├── __init__.py
│       └── board.py      # ✅ Engine python-chess
└── cultural/             # Sistema de narrativas
    ├── storyteller.py
    └── narrative.py
```

## 🎯 Fonte da Verdade

### Páginas Principais
- **Landing Page:** `/public/landing.html` (acessível em `/` e `/landing.html`)
- **Dashboard:** `/public/dashboard.html`
- **API Docs:** `/docs` (Swagger UI) e `/redoc` (ReDoc)

### Assets
- **CSS:** `/public/css/chess-theme.css`
- **Imagens:** `/public/images/`
- **Protótipos:** `/public/web/pages/`

## 🔗 URLs Disponíveis

### Frontend
- `http://localhost:3000/` → Landing page
- `http://localhost:3000/landing.html` → Landing page (direto)
- `http://localhost:3000/dashboard.html` → Hub de protótipos

### Backend API
- `http://localhost:8000/health` → Status do sistema
- `http://localhost:8000/docs` → Documentação Swagger
- `http://localhost:8000/redoc` → Documentação ReDoc
- `http://localhost:8000/api/narrative/init` → Gerar narrativa

### Proxy (via Frontend)
- `http://localhost:3000/health` → Proxied para backend
- `http://localhost:3000/api/narrative/init` → Proxied para backend

## ⚠️ Arquivos Obsoletos (Podem ser Removidos)

- `/landing-page/` - Backup original (já copiado para `/public`)
- `/web/` (raiz) - Duplicado em `/public/web/`

## 📝 Notas

1. **Next.js** está configurado mas serve principalmente como proxy
2. **Landing page** é HTML estático (não React) por escolha de design
3. **API** tem documentação automática via FastAPI
4. **Assets** estão consolidados em `/public` para fácil acesso
