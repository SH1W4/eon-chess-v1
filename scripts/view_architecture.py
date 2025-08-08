#!/usr/bin/env python3

import http.server
import socketserver
import webbrowser
import os

def create_html_file():
    # Lê o conteúdo do arquivo .mmd
    with open('docs/architecture.mmd', 'r') as f:
        mermaid_content = f.read()
    
    # Template HTML
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>AEON CHESS - Arquitetura</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{
                useMaxWidth: false,
                htmlLabels: true,
                curve: 'basis'
            }}
        }});
    </script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .mermaid {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AEON CHESS - Arquitetura Neural Simbiótica</h1>
        <div class="mermaid">
{mermaid_content}
        </div>
    </div>
</body>
</html>
"""
    
    # Salva o arquivo HTML
    with open('docs/architecture.html', 'w') as f:
        f.write(html_content)

def serve_html():
    # Configura o servidor
    PORT = 3001
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Servidor iniciado em http://localhost:{PORT}/docs/architecture.html")
        print("Pressione Ctrl+C para encerrar o servidor")
        
        # Abre o navegador
        webbrowser.open(f"http://localhost:{PORT}/docs/architecture.html")
        
        # Inicia o servidor
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")

if __name__ == "__main__":
    create_html_file()
    serve_html()
