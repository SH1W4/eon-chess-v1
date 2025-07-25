#!/bin/bash

# Script para gerenciar templates do DocSync
DOCSYNC_ROOT="$(dirname "$(dirname "$0")")"
TEMPLATE_CONFIG="$DOCSYNC_ROOT/templates/config.yaml"
TEMPLATE_DIR="$DOCSYNC_ROOT/templates"

# Função para criar novo documento a partir de template
create_from_template() {
    local template_type="$1"
    local output_path="$2"
    local title="$3"
    local author="$4"
    local date=$(date +"%d de %B de %Y")
    
    # Verificar template
    if [[ ! -f "$TEMPLATE_DIR/${template_type}.md" ]]; then
        echo "Erro: Template '${template_type}' não encontrado"
        exit 1
    fi
    
    # Criar diretório se não existir
    mkdir -p "$(dirname "$output_path")"
    
    # Copiar e personalizar template
    sed -e "s/\[Título do Documento\]/$title/g" \
        -e "s/\[Nome do Autor\]/$author/g" \
        -e "s/\[Data\]/$date/g" \
        -e "s/\[Versão\]/1.0.0/g" \
        "$TEMPLATE_DIR/${template_type}.md" > "$output_path"
    
    echo "Documento criado: $output_path"
}

# Função para validar documento
validate_document() {
    local doc_path="$1"
    local template_type="$2"
    
    echo "Validando documento: $doc_path"
    
    # Verificar metadados obrigatórios
    if ! grep -q "^**Autor**: " "$doc_path" || \
       ! grep -q "^**Data**: " "$doc_path" || \
       ! grep -q "^**Versão**: " "$doc_path"; then
        echo "ERRO: Metadados obrigatórios ausentes"
        return 1
    fi
    
    # Verificar seções obrigatórias (baseado no config.yaml)
    if [[ "$template_type" == "technical" ]]; then
        if ! grep -q "^## Visão Geral" "$doc_path" || \
           ! grep -q "^## Especificações Técnicas" "$doc_path" || \
           ! grep -q "^## Implementação" "$doc_path"; then
            echo "ERRO: Seções obrigatórias ausentes"
            return 1
        fi
    elif [[ "$template_type" == "analysis" ]]; then
        if ! grep -q "^## Objetivo" "$doc_path" || \
           ! grep -q "^## Metodologia" "$doc_path" || \
           ! grep -q "^## Resultados" "$doc_path" || \
           ! grep -q "^## Conclusões" "$doc_path"; then
            echo "ERRO: Seções obrigatórias ausentes"
            return 1
        fi
    fi
    
    echo "Documento válido!"
    return 0
}

# Função para listar templates disponíveis
list_templates() {
    echo "Templates disponíveis:"
    echo "1. technical - Template para documentação técnica"
    echo "2. analysis - Template para documentos de análise"
}

# Função de ajuda
show_help() {
    echo "Uso: $0 <comando> [opções]"
    echo ""
    echo "Comandos:"
    echo "  create <tipo> <caminho> <título> <autor> - Criar novo documento"
    echo "  validate <caminho> <tipo>               - Validar documento existente"
    echo "  list                                    - Listar templates disponíveis"
    echo ""
    echo "Exemplos:"
    echo "  $0 create technical docs/tecnico/novo-doc.md \"Meu Documento\" \"João Silva\""
    echo "  $0 validate docs/tecnico/documento.md technical"
    echo "  $0 list"
}

# Processamento principal
case "$1" in
    create)
        if [[ $# -lt 5 ]]; then
            show_help
            exit 1
        fi
        create_from_template "$2" "$3" "$4" "$5"
        ;;
    validate)
        if [[ $# -lt 3 ]]; then
            show_help
            exit 1
        fi
        validate_document "$2" "$3"
        ;;
    list)
        list_templates
        ;;
    *)
        show_help
        exit 1
        ;;
esac
