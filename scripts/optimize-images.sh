
#!/bin/bash
# Script de otimização de imagens

echo "🖼️  Otimizando imagens..."

# Instalar ferramentas de otimização
npm install -g imagemin-cli imagemin-mozjpeg imagemin-pngquant

# Otimizar imagens PNG
find public/images -name "*.png" -exec imagemin {} --out-dir=public/images/optimized --plugin=mozjpeg \;

# Otimizar imagens JPEG
find public/images -name "*.jpg" -exec imagemin {} --out-dir=public/images/optimized --plugin=mozjpeg \;

echo "✅ Otimização concluída!"
