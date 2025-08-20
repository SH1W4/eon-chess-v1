# Dockerfile para AEON CHESS com ARKITECT
# Multi-stage build para otimização

# Estágio base para dependências
FROM node:18-alpine AS base

# Instalar dependências do sistema
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    curl

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração
COPY package*.json ./
COPY next.config.js ./
COPY tsconfig.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Instalar dependências Node.js
RUN npm ci --only=production

# Copiar código fonte
COPY . .

# Construir aplicação Next.js
RUN npm run build

# Estágio de produção
FROM node:18-alpine AS production

# Instalar dependências do sistema
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências e aplicação construída
COPY --from=base /app/package*.json ./
COPY --from=base /app/next.config.js ./
COPY --from=base /app/.next ./.next
COPY --from=base /app/node_modules ./node_modules

# Mudar propriedade para usuário não-root
RUN chown -R nextjs:nodejs /app

# Mudar para usuário não-root
USER nextjs

# Expor porta
EXPOSE 3000

# Variáveis de ambiente
ENV NODE_ENV=production
ENV PORT=3000
ENV ARKITECT_ENABLED=true
ENV NEXT_TELEMETRY_DISABLED=1

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/ || exit 1

# Comando de inicialização
CMD ["npm", "start"]
