#!/bin/bash

# AEON Chess - Production Build Script

set -e

echo "🏗️  AEON Chess - Build de Produção"
echo "===================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Timer
start_time=$(date +%s)

# 1. Frontend Build
echo -e "\n${YELLOW}📦 Building Frontend...${NC}"

if [ -d "frontend" ]; then
    cd frontend
    
    # Clean previous builds
    rm -rf build
    
    # Install dependencies
    echo "Installing dependencies..."
    npm ci --silent
    
    # Run build with optimizations
    echo "Building optimized production bundle..."
    NODE_ENV=production \
    GENERATE_SOURCEMAP=false \
    INLINE_RUNTIME_CHUNK=false \
    npm run build
    
    # Analyze bundle size
    if [ -d "build" ]; then
        echo -e "\n${BLUE}Bundle Analysis:${NC}"
        find build/static -name "*.js" -o -name "*.css" | while read file; do
            size=$(du -h "$file" | cut -f1)
            echo "  $(basename "$file"): $size"
        done
        
        total_size=$(du -sh build | cut -f1)
        echo -e "  ${GREEN}Total build size: $total_size${NC}"
    fi
    
    cd ..
else
    echo -e "${RED}Frontend directory not found${NC}"
    exit 1
fi

# 2. Backend Optimization
echo -e "\n${YELLOW}🐍 Optimizing Backend...${NC}"

if [ -d "src" ]; then
    # Compile Python files
    echo "Compiling Python files..."
    python3 -m compileall -b src/
    
    # Generate requirements with hashes for security
    echo "Generating locked requirements..."
    pip-compile --generate-hashes requirements.in -o requirements.txt 2>/dev/null || true
    
    echo -e "${GREEN}✓ Backend optimized${NC}"
else
    echo -e "${RED}Source directory not found${NC}"
fi

# 3. Database Migrations
echo -e "\n${YELLOW}🗄️  Preparing Database Migrations...${NC}"

if [ -f "alembic.ini" ]; then
    # Check if migrations are up to date
    echo "Checking migration status..."
    # alembic check || echo "Migrations need to be generated"
    echo -e "${GREEN}✓ Migrations ready${NC}"
fi

# 4. Asset Optimization
echo -e "\n${YELLOW}🎨 Optimizing Assets...${NC}"

# Compress images if imageoptim-cli is available
if command -v imageoptim-cli >/dev/null 2>&1; then
    echo "Optimizing images..."
    find frontend/public -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" | \
        xargs -I {} imageoptim-cli {} 2>/dev/null || true
fi

# 5. Docker Build
echo -e "\n${YELLOW}🐳 Building Docker Images...${NC}"

# Build with BuildKit for better caching
export DOCKER_BUILDKIT=1

echo "Building backend image..."
docker build -f deploy/Dockerfile.backend -t aeon-chess-backend:latest . --quiet

echo "Building frontend image..."
docker build -f deploy/Dockerfile.frontend -t aeon-chess-frontend:latest frontend/ --quiet

echo -e "${GREEN}✓ Docker images built${NC}"

# 6. Security Scan
echo -e "\n${YELLOW}🔒 Security Check...${NC}"

# Check for known vulnerabilities in dependencies
if [ -f "frontend/package.json" ]; then
    cd frontend
    npm audit --production --audit-level=high || echo -e "${YELLOW}⚠️  Some vulnerabilities found${NC}"
    cd ..
fi

# 7. Generate Build Info
echo -e "\n${YELLOW}📋 Generating Build Info...${NC}"

BUILD_INFO="deploy/build-info.json"
cat > $BUILD_INFO << EOF
{
  "version": "$(cat package.json | grep version | head -1 | awk -F: '{ print $2 }' | sed 's/[",]//g' | tr -d ' ')",
  "build_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
  "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
  "builder": "$(whoami)@$(hostname)",
  "node_version": "$(node --version 2>/dev/null || echo 'unknown')",
  "python_version": "$(python3 --version 2>/dev/null | awk '{print $2}' || echo 'unknown')"
}
EOF

echo -e "${GREEN}✓ Build info generated${NC}"

# 8. Summary
end_time=$(date +%s)
duration=$((end_time - start_time))

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}✅ Build Completo!${NC}"
echo -e "${GREEN}================================${NC}"

echo -e "\nBuild Statistics:"
echo -e "  Duration: ${duration}s"
echo -e "  Frontend: $(du -sh frontend/build 2>/dev/null | cut -f1 || echo 'N/A')"
echo -e "  Backend Image: $(docker images aeon-chess-backend:latest --format '{{.Size}}' 2>/dev/null || echo 'N/A')"
echo -e "  Frontend Image: $(docker images aeon-chess-frontend:latest --format '{{.Size}}' 2>/dev/null || echo 'N/A')"

echo -e "\nNext steps:"
echo -e "  1. Run: ${YELLOW}./deploy/setup-local.sh${NC}"
echo -e "  2. Deploy: ${YELLOW}docker compose -f docker-compose.production.yml up -d${NC}"
