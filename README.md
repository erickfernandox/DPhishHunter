# DPhishHunter

### Ferramenta criada para a geração automatizada de combinações entre palavras-chave estratégicas, com o objetivo de identificar domínios potencialmente maliciosos ou suspeitos antes que sejam utilizados em campanhas de phishing.

### Funcionalidades
- Geração automatizada de domínios com base em combinações de palavras-chave relevantes:
  Criação de possíveis variações de domínios que imitariam marcas, serviços ou termos populares para fins de monitoramento preventivo de phishing
- Consulta WHOIS para identificação de domínios recentemente registrados:
  Verificação do status de registro, data de criação e outras informações relevantes para priorizar domínios recém-criados e potencialmente maliciosos.
- Detecção de atividade online e serviços hospedados:
  Validação da presença de serviços ativos (HTTP/HTTPS) nos domínios gerados
- Varredura automatizada de subdomínios relevantes:
  Descoberta e verificação de subdomínios associados que possam estar sendo utilizados.
- Extração de título da página e informações de hospedagem:
  Coleta de metadados como o título HTML e informações de infraestrutura (IP, ASN, provedor), auxiliando na classificação e análise de risco.

### Requisitos
Para utilizar o **DPhishHunter**, você precisa ter instalado:
- Python 3.x
- Pacotes necessários:
  ```bash
  pip install requests beautifulsoup4 whois dns.resolver colorama
  ```

### Instalação
```bash
git clone https://github.com/erickfernandox/DPhishHunter
cd DPhishHunter
pip install -r requirements.txt
```

### Como Usar
Para rodar o script, utilize o seguinte comando:
```bash
python3 dphishhunter.py -p inscricoes,concurso,2025,cadastro,govbr
```
Ou utilizando um arquivo de lista de palavras:
```bash
python3 dphishhunter.py -l wordlist.txt
```



### Exemplo de Saída
```bash
[REGISTRED/OFFLINE] inscricoesconcurso2025.com
      [Subdominio Found] cadastro.inscricoesconcurso2025.com - Title: "Página Oficial"
```

<img src="https://i.ibb.co/JwtkwwF9/Captura-de-tela-de-2025-03-24-20-32-49.png">
