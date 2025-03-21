import itertools
import argparse
import requests
import concurrent.futures
import socket
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)  # Inicializa colorama para colorir o output

def load_wordlist(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def generate_combinations(words):
    combinations = []
    current_year = datetime.now().year
    years = [str(current_year + i) for i in range(-2, 3)]  # Ano atual, 2 anos atrás e 2 anos à frente
    special_chars = ["-", "_", "."]  # Caracteres comuns em domínios fraudulentos
    
    for i in range(2, len(words) + 1):
        for combo in itertools.permutations(words, i):
            base_combo = "".join(combo)
            combinations.append(base_combo)
            for year in years:
                combinations.append(f"{base_combo}{year}")
                combinations.append(f"{year}{base_combo}")
            for char in special_chars:
                for year in years:
                    combinations.append(f"{base_combo}{char}{year}")
                    combinations.append(f"{year}{char}{base_combo}")
                combinations.append(f"{base_combo}{char}")
    return combinations

def get_page_title(url):
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"
            return title
    except requests.RequestException:
        pass
    return "No Title"

def get_dns_info(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return "No DNS Record"

def check_domain(domain):
    try:
        url = f"https://{domain}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            title = get_page_title(url)
            dns_info = get_dns_info(domain)
            print(Fore.GREEN + f"[VALID] {domain} - [{title}] - DNS: {dns_info}")
            return True
    except requests.RequestException:
        pass
    return False

def main():
    parser = argparse.ArgumentParser(description="Generate and check possible fraudulent domains.")
    parser.add_argument("-l", "--list", required=True, help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent requests")
    args = parser.parse_args()
    
    words = load_wordlist(args.list)
    combinations = generate_combinations(words)
    tlds = [".com", ".net", ".org", ".com.br", ".online", ".shop", ".info", ".biz", ".top", ".site", ".xyz"]
    
    print(f"[+] Checking {len(combinations) * len(tlds)} possible domains using {args.threads} threads...")
    
    domains = [f"{combo}{tld}" for combo in combinations for tld in tlds]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = executor.map(check_domain, domains)
    
    valid_domains = [domain for domain, valid in zip(domains, results) if valid]
    
    for domain in valid_domains:
        print(Fore.GREEN + f"[VALID] {domain}")

if __name__ == "__main__":
    main()
