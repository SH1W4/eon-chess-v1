#!/bin/bash

echo "🔍 AEON Chess - Status do Deploy Local"
echo "======================================="

# Verificar containers
echo -e "\n📦 Status dos Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep aeon-chess

# Verificar health do backend
echo -e "\n🏥 Health Check Backend:"
curl -s http://localhost/health | json_pp

# Verificar documentação da API
echo -e "\n📚 API Documentation:"
echo "- Swagger UI: http://localhost/docs"
echo "- ReDoc: http://localhost/redoc"

# Verificar frontend
echo -e "\n🌐 Frontend:"
if curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q "200"; then
    echo "✅ Frontend está servindo (HTTP 200)"
else
    echo "❌ Frontend não está acessível"
fi

# Verificar endpoints da API
echo -e "\n🔌 Testando Endpoints da API:"
echo -n "- GET /api/v1/game/test-123: "
curl -s -o /dev/null -w "%{http_code}" http://localhost/api/v1/game/test-123

echo -e "\n\n✨ URLs de Acesso:"
echo "- Frontend: http://localhost/"
echo "- API Docs: http://localhost/docs"
echo "- Health: http://localhost/health"

echo -e "\n📝 Logs dos containers:"
echo "- Backend: docker logs aeon-chess-backend"
echo "- Nginx: docker logs aeon-chess-nginx"
echo "- PostgreSQL: docker logs aeon-chess-postgres"
echo "- Redis: docker logs aeon-chess-redis"
