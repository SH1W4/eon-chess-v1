# 🧠 AEON CHESS - ARKITECT Integration
# Dockerfile para empacotamento completo do sistema

FROM node:18-alpine AS base

# Instalar dependências do sistema
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    curl

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY package*.json ./
COPY next.config.js ./
COPY tsconfig.json ./

# Instalar dependências Node.js
RUN npm ci --only=production

# Copiar código fonte
COPY . .

# Construir aplicação Next.js
RUN npm run build

# Estágio de produção
FROM node:18-alpine AS production

# Instalar dependências Python para ARKITECT
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copiar aplicação construída
COPY --from=base /app/public ./public
COPY --from=base /app/.next/standalone ./
COPY --from=base /app/.next/static ./.next/static

# Copiar arquivos de configuração ARKITECT
COPY --from=base /app/ARKITECT_INTEGRATION.md ./
COPY --from=base /app/VERIFICATION_REPORT.md ./
COPY --from=base /app/src/components/ARKITECTChessBoard.tsx ./src/components/
COPY --from=base /app/src/pages/chess-test.tsx ./src/pages/

# Definir permissões
RUN chown -R nextjs:nodejs /app
USER nextjs

# Expor porta
EXPOSE 3000

# Variáveis de ambiente
ENV NODE_ENV=production
ENV ARKITECT_ENABLED=true
ENV NEXT_TELEMETRY_DISABLED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/chess-test || exit 1

# Comando de inicialização
CMD ["node", "server.js"]
