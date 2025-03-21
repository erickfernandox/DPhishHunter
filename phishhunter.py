import itertools
import argparse
import requests
from urllib.parse import urlparse

def load_wordlist(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]
    return words

def generate_combinations(words):
    combinations = []
    for i in range(2, len(words) + 1):
        for combo in itertools.permutations(words, i):
            combinations.append("".join(combo))
    return combinations

def check_domain(domain):
    try:
        url = f"https://{domain}"
        response = requests.get(url, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate and check possible fraudulent domains.")
    parser.add_argument("-l", "--list", required=True, help="Path to wordlist file")
    args = parser.parse_args()
    
    words = load_wordlist(args.list)
    combinations = generate_combinations(words)
    
    print(f"[+] Checking {len(combinations)} possible domains...")
    
    for combo in combinations:
        domain = f"{combo}.com"  # Pode mudar para outras TLDs, como .net, .org, etc.
        if check_domain(domain):
            print(f"[VALID] {domain} exists!")
        else:
            print(f"[INVALID] {domain} not found.")

if __name__ == "__main__":
    main()
