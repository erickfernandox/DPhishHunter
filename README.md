<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DPhishHunter - Manual</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            color: #333;
        }
        code {
            background: #f4f4f4;
            padding: 5px;
            border-radius: 5px;
        }
        pre {
            background: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>DPhishHunter</h1>
    <h2>Ferramenta de Geração e Verificação de Domínios para Detecção de Phishing</h2>
    
    <h3>Funcionalidades</h3>
    <ul>
        <li>Geração automática de domínios suspeitos usando combinações de palavras.</li>
        <li>Verificação de registro WHOIS para detectar domínios recentemente criados.</li>
        <li>Testes de conectividade para determinar se os domínios estão online.</li>
        <li>Verificação automática de subdomínios relevantes.</li>
        <li>Extração do título da página para identificação visual rápida.</li>
    </ul>
    
    <h3>Requisitos</h3>
    <p>Para utilizar o DPhishHunter, você precisa ter instalado:</p>
    <ul>
        <li>Python 3.x</li>
        <li>Pacotes necessários: <code>requests</code>, <code>beautifulsoup4</code>, <code>whois</code>, <code>dns.resolver</code>, <code>colorama</code></li>
    </ul>
    
    <h3>Instalação</h3>
    <pre><code>git clone https://github.com/seu-usuario/DPhishHunter.git
cd DPhishHunter
pip install -r requirements.txt</code></pre>
    
    <h3>Como Usar</h3>
    <p>Para rodar o script, utilize o seguinte comando:</p>
    <pre><code>python phishhunter.py -p cnu,concurso,govbr,inscricao,inscricoes,2025,cadastro</code></pre>
    <p>Ou utilizando um arquivo de lista de palavras:</p>
    <pre><code>python phishhunter.py -l wordlist.txt</code></pre>
    
    <h3>Exemplo de Saída</h3>
    <pre><code>[REGISTRED/OFFLINE] inscricoescnu2025.com
      [Subdominio Found] cnu.inscricoescnu2025.com - Title: "Página Oficial"</code></pre>
</body>
</html>
