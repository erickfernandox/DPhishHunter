# DPhishHunter

### Ferramenta de geração combinatória de domínios potencialmente suspeitos para a prevenção de ataques de phishing.

### Funcionalidades
- Geração automática de domínios suspeitos usando combinações de palavras.
- Verificação de registro WHOIS para detectar domínios recentemente criados.
- Testes de conectividade para determinar se os domínios estão online.
- Verificação automática de subdomínios relevantes.
- Extração do título da página para identificação visual rápida.

### Requisitos
Para utilizar o **DPhishHunter**, você precisa ter instalado:
- Python 3.x
- Pacotes necessários:
  ```bash
  pip install requests beautifulsoup4 whois dns.resolver colorama
  ```

### Instalação
```bash
git clone https://github.com/seu-usuario/DPhishHunter.git
cd DPhishHunter
pip install -r requirements.txt
```

### Como Usar
Para rodar o script, utilize o seguinte comando:
```bash
python3 phishhunter.py -p inscricoes,concurso,2025,cadastro
```
Ou utilizando um arquivo de lista de palavras:
```bash
python phishhunter.py -l wordlist.txt
```

<img src=https://i.ibb.co/JwtkwwF9/Captura-de-tela-de-2025-03-24-20-32-49.png>

### Exemplo de Saída
```bash
[REGISTRED/OFFLINE] inscricoesconcurso2025.com
      [Subdominio Found] cadastro.inscricoesconcurso2025.com - Title: "Página Oficial"
```

