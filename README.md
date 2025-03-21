<h1 align="center">DPhishHunter</h1>
<p align="center">
  <strong>Ferramenta de Geração e Verificação de Domínios para Detecção de Phishing</strong>
</p>
<p align="center">
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#requisitos">Requisitos</a> •
  <a href="#instalação">Instalação</a> •
  <a href="#como-usar">Como Usar</a> •
</p>

---

## Funcionalidades

O **DPhishHunter** é uma ferramenta poderosa para gerar e verificar domínios potencialmente maliciosos, com foco em detecção de phishing. Ele oferece as seguintes funcionalidades:

- **Geração de Combinações de Domínios**:
  - Gera combinações de domínios com pontos (`.`) e hífens (`-`).
  - Exemplo: `cnu.inscricoesconcurso.com`, `inscricoes.concursocnu.org`.

- **Validação de Domínios**:
  - Verifica se os domínios são válidos com base em padrões comuns.
  - Filtra domínios inválidos, como aqueles com anos isolados entre pontos (`2026`) ou dois pontos consecutivos (`..`).

- **Verificação de Atividade**:
  - Resolve domínios para endereços IP.
  - Verifica se o domínio está ativo (conexão HTTP/HTTPS).

- **Classificação de Risco**:
  - Obtém informações WHOIS (data de registro) e nameservers.
  - Classifica o risco de fraude com base na idade do domínio e uso de serviços como Cloudflare.

- **Saída Detalhada**:
  - Exibe domínios válidos e inválidos.
  - Classifica os domínios válidos em **Alto Risco**, **Médio Risco** e **Baixo Risco**.

---

## Requisitos

- **Python 3.7 ou superior**.
- Bibliotecas Python:
  - `colorama`
  - `requests`
  - `beautifulsoup4`
  - `python-whois`
  - `dnspython`

---

## Instalação

Siga os passos abaixo para configurar o **DPhishHunter**:

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/DPhishHunter.git
   cd DPhishHunter
   ```

2. Instale as dependências:
   ```bash
    pip install -r requirements.txt
   ```
    Se o arquivo requirements.txt não existir, instale as bibliotecas manualmente:
     ```bash
      pip install colorama requests beautifulsoup4 python-whois dnspython
     ```

## Como Usar

O DPhishHunter pode ser executado com uma lista de palavras fornecida em um arquivo ou diretamente como argumento.

Opções de Execução

-l ou --list: Caminho para um arquivo de wordlist (uma palavra por linha).

-p ou --params: Lista de palavras separadas por vírgulas.

-t ou --threads: Número de threads para execução concorrente (padrão: 10).

Exemplos
Usando uma wordlist:

   ```bash
python DPhishHunter.py -l wordlist.txt
O arquivo wordlist.txt deve conter uma palavra por linha, por exemplo:
   ```

   ```
govbr
pagamento
concurso
2025
   ```
Usando uma lista de palavras diretamente:

   ```
python DPhishHunter.py -p govbr,pagamento,concurso,2025
   ```
Aumentando o número de threads para 20:

   ```
python DPhishHunter.py -p cnu,inscricoes,concurso,2025 -t 20
   ```

## Saída

A ferramenta exibe:

Domínios válidos e ativos, com classificação de risco:

Alto Risco: Domínios registrados há menos de 2 meses e hospedados na Cloudflare.

Médio Risco: Domínios registrados há menos de 3 meses.

Baixo Risco: Domínios registrados há mais de 3 meses.

Domínios inválidos: Domínios que não atendem aos critérios de validação.
