#!/bin/bash

# Script para atualizar metadados dos documentos
echo "Iniciando atualização de metadados..."

update_metadata() {
    local file="$1"
    local title=$(basename "$file" .md)
    local date=$(date +"%d de %B de %Y")
    local temp_file=$(mktemp)
    
    # Criar cabeçalho temporário
    cat > "$temp_file" << EOF
# $title

**Autor**: Sistema XadrezMaster  
**Data**: $date  
**Versão**: 1.0  

EOF

    # Adicionar conteúdo existente (pulando cabeçalho antigo se existir)
    if grep -q "^# " "$file"; then
        sed '1,/^$/d' "$file" >> "$temp_file"
    else
        cat "$file" >> "$temp_file"
    fi

    # Substituir arquivo original
    mv "$temp_file" "$file"
    echo "Atualizado: $file"
}

# Atualizar todos os arquivos markdown
find docs -name "*.md" -type f | while read -r file; do
    if [[ "$file" != *"/templates/"* ]]; then
        echo "Processando $file..."
        update_metadata "$file"
    fi
done

echo "Atualização de metadados concluída."
