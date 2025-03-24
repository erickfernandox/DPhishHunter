# DPhishHunter

## Ferramenta de Geração e Verificação de Domínios para Detecção de Phishing

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
python phishhunter.py -p cnu,concurso,govbr,inscricao,inscricoes,2025,cadastro
```
Ou utilizando um arquivo de lista de palavras:
```bash
python phishhunter.py -l wordlist.txt
```

### Exemplo de Saída
```bash
[REGISTRED/OFFLINE] inscricoescnu2025.com
      [Subdominio Found] cnu.inscricoescnu2025.com - Title: "Página Oficial"
```

### Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

### Licença
Este projeto está sob a licença MIT.
