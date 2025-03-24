import itertools
import argparse
import concurrent.futures
import socket
from colorama import Fore, Style, init
import re
import requests
from bs4 import BeautifulSoup
import whois  # Biblioteca para consulta WHOIS
import dns.resolver  # Biblioteca para consulta DNS
from datetime import datetime, timedelta

init(autoreset=True)  # Inicializa colorama para colorir o output

def generate_combinations(words):
    """Gera combinações de domínios, garantindo que o domínio principal contenha pelo menos 2 palavras."""
    combinations = []
    special_chars = ["-", "."]  # Caracteres comuns em domínios fraudulentos

    # Gera combinações com pelo menos 2 palavras no domínio principal
    for i in range(2, len(words) + 1):
        for combo in itertools.permutations(words, i):
            # Combinações sem caracteres especiais
            base_combo = "".join(combo)
            combinations.append(base_combo)

            # Combinações com caracteres especiais entre as palavras
            for char in special_chars:
                # Adiciona combinações com caracteres especiais entre todas as palavras
                combinations.append(char.join(combo))

                # Adiciona combinações com subdomínios aninhados
                if char == ".":
                    # Exemplo: cnu.inscricoescnu2025
                    for j in range(1, len(combo)):
                        subdomain = f"{combo[0]}.{''.join(combo[1:])}"
                        combinations.append(subdomain)

    return combinations

def is_valid_domain(domain, words):
    """Verifica se o domínio é válido e se o domínio principal contém pelo menos 2 palavras."""
    # Extrai o domínio principal (parte antes do TLD)
    domain_parts = domain.split(".")
    if len(domain_parts) < 2:
        return False  # Domínio inválido se não houver TLD

    domain_main = domain_parts[-2]  # Domínio principal (ex: "inscricoescnu2025" em "cnu.inscricoescnu2025.org")

    # Verifica se o domínio principal contém pelo menos 2 palavras da wordlist
    word_count = sum(1 for word in words if word in domain_main)
    return word_count >= 2

def get_dns_info(domain):
    """Resolve o domínio para um endereço IP."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

def get_whois_info(domain):
    """Obtém informações WHOIS do domínio (data de registro)."""
    try:
        whois_info = whois.whois(domain)
        creation_date = whois_info.creation_date
        if isinstance(creation_date, list):  # Alguns WHOIS retornam uma lista de datas
            creation_date = creation_date[0]
        return creation_date
    except Exception:
        return None

def get_hosting_info(domain):
    """Obtém informações sobre onde o domínio está hospedado (nameservers)."""
    try:
        answers = dns.resolver.resolve(domain, "NS")
        nameservers = [str(ns) for ns in answers]
        return ", ".join(nameservers)
    except Exception:
        return "Unknown"

def is_cloudflare_hosted(domain):
    """Verifica se o domínio está atrás da Cloudflare."""
    try:
        # Verifica se os nameservers contêm "cloudflare"
        nameservers = get_hosting_info(domain).lower()
        if "cloudflare" in nameservers:
            return True

        # Verifica se o IP pertence à Cloudflare
        ip = get_dns_info(domain)
        if ip:
            # Lista de IP ranges da Cloudflare (exemplo simplificado)
            cloudflare_ranges = [
                "173.245.48.0/20",
                "103.21.244.0/22",
                "103.22.200.0/22",
                "103.31.4.0/22",
                "141.101.64.0/18",
                "108.162.192.0/18",
                "190.93.240.0/20",
                "188.114.96.0/20",
                "197.234.240.0/22",
                "198.41.128.0/17",
                "162.158.0.0/15",
                "104.16.0.0/13",
                "104.24.0.0/14",
                "172.64.0.0/13",
                "131.0.72.0/22"
            ]
            from ipaddress import ip_address, ip_network
            ip_addr = ip_address(ip)
            for range in cloudflare_ranges:
                if ip_addr in ip_network(range):
                    return True
    except Exception:
        pass
    return False

def check_domain(domain, checked_domains, words):
    """Verifica se o host existe (resolução DNS) e exibe informações."""
    try:
        # Verifica se o domínio já foi verificado
        if domain in checked_domains:
            return False
        checked_domains.add(domain)

        # Verifica se o domínio é válido
        if not is_valid_domain(domain, words):
            return False

        # Verifica se o domínio resolve para um IP
        ip = get_dns_info(domain)
        if not ip:
            return False

        # Obtém informações WHOIS e de hospedagem
        whois_info = get_whois_info(domain)
        hosting_info = get_hosting_info(domain)

        # Exibe as informações
        if whois_info:
            creation_date = whois_info
            print(f"{Fore.GREEN}[VALID] {domain} - DNS: {ip} - Registered: {creation_date.strftime('%Y-%m-%d')} - Hosting: {hosting_info}\n")
        else:
            print(f"{Fore.GREEN}[VALID] {domain} - DNS: {ip} - Registered: Unknown - Hosting: {hosting_info}\n")
        return True
    except Exception as e:
        print(Fore.RED + f"[ERROR] {domain} - {str(e)}\n")
    return False

def main():
    """Função principal para gerar e verificar domínios."""
    parser = argparse.ArgumentParser(description="Generate and check possible fraudulent domains.")
    parser.add_argument("-l", "--list", help="Path to wordlist file")
    parser.add_argument("-p", "--params", help="Comma-separated list of words")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent requests")
    args = parser.parse_args()
    
    # Carrega as palavras da wordlist ou do parâmetro -p
    if args.list:
        with open(args.list, 'r', encoding='utf-8') as f:
            words = [line.strip() for line in f if line.strip()]
    elif args.params:
        words = [word.strip() for word in args.params.split(",")]
    else:
        print(Fore.RED + "[-] Error: You must provide either a wordlist file (-l) or a comma-separated list of words (-p).\n")
        return
    
    combinations = generate_combinations(words)
    tlds = [".com", ".net", ".org", ".com.br", ".online", ".shop", ".info", ".biz", ".top", ".site", ".xyz"]
    
    print(f"[+] Checking {len(combinations) * len(tlds)} possible domains using {args.threads} threads...\n")
    
    # Gera domínios com TLDs
    domains = [f"{combo}{tld}" for combo in combinations for tld in tlds]
    
    # Filtra domínios válidos
    valid_domains = [domain for domain in domains if is_valid_domain(domain, words)]
    
    # Conjunto para armazenar domínios já verificados
    checked_domains = set()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = list(executor.map(lambda domain: check_domain(domain, checked_domains, words), valid_domains))
    
    valid_resolved_domains = [domain for domain, valid in zip(valid_domains, results) if valid]
    
    print(Fore.CYAN + f"\n[+] Found {len(valid_resolved_domains)} valid domains:\n")
    for domain in valid_resolved_domains:
        print(Fore.GREEN + f"[VALID] {domain}\n")

if __name__ == "__main__":
    main()
