# Dependências do Sistema

## Visão Geral

Este documento detalha as dependências entre os diferentes componentes do AEON Chess, incluindo requisitos de sistema, bibliotecas e serviços externos.

## Dependências de Sistema

### Requisitos de Runtime

- **Node.js**: ≥ 18.0.0
  - Gerenciamento de pacotes via npm/yarn
  - Suporte a ES Modules
  - TypeScript runtime

- **Python**: ≥ 3.11.0
  - Virtual environments
  - pip para gerenciamento de pacotes
  - Suporte a async/await

- **Go**: ≥ 1.19.0
  - Módulos Go
  - Suporte a generics
  - Testing framework

### Infraestrutura

- **Docker**: ≥ 20.10
  - Docker Compose V2
  - Buildkit
  - Multi-stage builds

- **Banco de Dados**:
  - PostgreSQL ≥ 14
  - Redis ≥ 6.2
  - MinIO (compatível com S3)

## Dependências de Serviço

### Motor de Análise

- **TensorFlow**: 2.x
  - CUDA support (opcional)
  - TensorFlow Serving
  - Modelos pré-treinados

- **PyTorch**: 2.x
  - CUDA support (opcional)
  - TorchServe
  - Modelos customizados

### Sistema de Treinamento

- **Stockfish**: ≥ 15
  - Suporte UCI
  - Multithreading
  - NNUE

- **Leela Chess Zero**:
  - Redes neurais
  - Backend CUDA/OpenCL
  - Análise em lote

## Dependências de Frontend

### Web

- **React**: 18.x
  - React Router
  - React Query
  - Styled Components

- **Next.js**: 13.x
  - App Router
  - Server Components
  - API Routes

### Mobile

- **React Native**: 0.71+
  - React Navigation
  - Reanimated
  - AsyncStorage

### Rendering

- **Three.js**: Para tabuleiro 3D
- **WebGL**: Suporte browser
- **Canvas**: Fallback 2D

## Dependências de Backend

### API Gateway

- **Express.js**
- **FastAPI**
- **Nginx**

### Serviços

- **gRPC**: Comunicação entre serviços
- **Protocol Buffers**: Serialização
- **OpenAPI**: Documentação

## Dependências de Monitoramento

### Observabilidade

- **Prometheus**
- **Grafana**
- **ELK Stack**

### Logs

- **Winston**
- **Logrus**
- **Structured Logging**

## Dependências de Desenvolvimento

### Ferramentas

- **Git**: ≥ 2.30
- **Make**
- **Visual Studio Code**
- **Docker Desktop**

### Testing

- **Jest**
- **PyTest**
- **Go Testing**

### Linting e Formatação

- **ESLint**
- **Black**
- **gofmt**

## Matriz de Compatibilidade

| Componente | Versão Mínima | Versão Recomendada | Notas |
|------------|---------------|-------------------|--------|
| Node.js | 18.0.0 | 20.0.0 | LTS |
| Python | 3.11.0 | 3.11.5 | Dataclasses, AsyncIO |
| Go | 1.19.0 | 1.21.0 | Generics |
| PostgreSQL | 14.0 | 15.0 | JSON, Partitioning |
| Redis | 6.2 | 7.0 | Streams |

## Gerenciamento de Dependências

### Versionamento

- Semantic Versioning (SemVer)
- Lock files para todas as dependências
- Renovate Bot para atualizações

### Segurança

- Análise de vulnerabilidades
- Atualizações automáticas de segurança
- Auditoria de dependências

### Performance

- Otimização de bundle size
- Tree shaking
- Lazy loading

## Documentação Relacionada

- [Guia de Instalação](../setup.md)
- [Configuração de Ambiente](../environment.md)
- [Troubleshooting](../troubleshooting.md)
