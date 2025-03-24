import itertools
import argparse
import concurrent.futures
import socket
from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup
import whois
from datetime import datetime, timedelta
import logging

logging.getLogger("whois").setLevel(logging.CRITICAL)
init(autoreset=True)

def generate_combinations(words):
    combinations = []
    special_chars = ["-"]
    
    for i in range(2, len(words) + 1):
        for combo in itertools.permutations(words, i):
            base_combo = "".join(combo)
            combinations.append(base_combo)
            for char in special_chars:
                combinations.append(char.join(combo))
    
    return combinations

def get_registration_date(domain):
    try:
        whois_info = whois.whois(domain)
        creation_date = whois_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        return creation_date
    except Exception:
        return None

def is_registered(domain):
    return get_registration_date(domain) is not None

def is_online(domain):
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def get_page_title(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.title.string.strip() if soup.title else "No Title"
    except Exception:
        return "No Title"

def check_domain(domain, checked_domains, subdomain_words):
    if domain in checked_domains:
        return False
    checked_domains.add(domain)

    registration_date = get_registration_date(domain)
    if not registration_date:
        return False

    now = datetime.now()
    time_since_registration = now - registration_date
    days_since_registration = time_since_registration.days
    formatted_time = f"({days_since_registration} days ago)"
    three_months_ago = now - timedelta(days=90)
    date_str = registration_date.strftime('%Y-%m-%d') if registration_date else "Unknown"
    date_color = Fore.RED if registration_date and registration_date > three_months_ago else ""

    if is_online(domain):
        title = get_page_title(domain)
        print(f"{Fore.GREEN}[REGISTRED/ONLINE] {domain} - {date_color}{date_str} {formatted_time}{Style.RESET_ALL} - Title: {title}")
        check_subdomains(domain, subdomain_words)
    else:
        print(f"{Fore.YELLOW}[REGISTRED/OFFLINE] {domain} - {date_color}{date_str} {formatted_time}{Style.RESET_ALL}")
    return True

def check_subdomains(domain, subdomain_words):
    for word in subdomain_words:
        subdomain = f"{word}.{domain}"
        if is_online(subdomain):
            title = get_page_title(subdomain)
            print(f"      {Fore.CYAN}[Subdominio Found] {subdomain} - Title: \"{title}\"{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Generate and check possible fraudulent domains.")
    parser.add_argument("-l", "--list", help="Path to wordlist file")
    parser.add_argument("-p", "--params", help="Comma-separated list of words")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent requests")
    args = parser.parse_args()
    
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
    
    domains = [f"{combo}{tld}" for combo in combinations for tld in tlds]
    
    checked_domains = set()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = list(executor.map(lambda domain: check_domain(domain, checked_domains, words), domains))
    
    valid_resolved_domains = [domain for domain, valid in zip(domains, results) if valid]
    
    print(Fore.CYAN + f"\n[+] Found {len(valid_resolved_domains)} valid domains:\n")
    for domain in valid_resolved_domains:
        print(Fore.GREEN + f"[VALID] {domain}\n")

if __name__ == "__main__":
    main()
