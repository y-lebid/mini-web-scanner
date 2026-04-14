import requests
from tqdm import tqdm
from colorama import init, Fore, Style
import json
from urllib.parse import urlparse
import random
import pyfiglet


def print_banner():
    ascii_banner = pyfiglet.figlet_format("MWVS")
    print (Fore.CYAN + ascii_banner + Style.RESET_ALL)

    print(Fore.YELLOW + "         v2.0 - Developed by l_yehor")
    print(Fore.CYAN + "_" * 60 + "\n")


init(autoreset=True)

SENSITIVE_PATHS = [
    ".env",
    ".git/",
    ".git/config",
    ".gitignore",
    ".htaccess",
    ".htpasswd",
    "config.php",
    "wp-config.php",
    "backup.zip",
    "db.sql",
    ".DS_Store"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

def scan_headers(url):
    results = {
        'url': url,
        'status': 'error',
        'headers': {},
        'error_message': None
    }
    
    security_headers = [
        'Strict-Transport-Security', 
        'Content-Security-Policy',   
        'X-Frame-Options',           
        'X-Content-Type-Options',
        'Referrer-Policy',
        'Permissions-Policy'
    ]

    headers_to_send = {'User-Agent': random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, headers=headers_to_send, timeout=5)
        results['status'] = 'success'
        response_headers = response.headers

        for header in security_headers:
            if header in response_headers:
                results['headers'][header] = {
                    'present': True,
                    'value': response_headers[header]
                }
            else:
                results['headers'][header] = {
                    'present': False,
                    'value': None
                }
    except requests.exceptions.RequestException as e:
        results['status'] = 'error'
        results['error_message'] = str(e)

    return results
    
def print_results_to_terminal(scan_data):
    url = scan_data['url']
    print(Fore.CYAN + f'\n[*] Analyzing security headers for: {url}')
    print(Fore.CYAN + '_' * 60)

    if scan_data['status'] == 'error':
        print(Fore.RED + Style.BRIGHT + f'[!] Not connected to {url}.')
        print(Fore.RED + f'Error: {scan_data["error_message"]}')
        return

    for header, details in scan_data['headers'].items():
        if details['present']:
            print(Fore.GREEN + f"[+] FOUND: {header} -> {details['value']}")
        else:
            print(Fore.RED + f'[-] MISSING: {header} (Potential vulnerability!)')

def scan_sensitive_files(base_url):
    print(Fore.MAGENTA + "\n[+] Scanning for sensitive files...")
    print(Fore.MAGENTA + "_" * 60)

    found = []
    headers_to_send = {'User-Agent': random.choice(USER_AGENTS)}

    for path in tqdm(SENSITIVE_PATHS, desc="Scanning", colour="green"):
        url = f"{base_url.rstrip('/')}/{path}"

        try:
            response = requests.get(url, headers=headers_to_send, timeout=5)

            if response.status_code == 200:
                tqdm.write(Fore.GREEN + f"[+] FOUND: {url}")
                found.append((url, "accessible"))

            elif response.status_code == 403:
                tqdm.write(Fore.YELLOW + f"[!] FORBIDDEN (exists?): {url}")
                found.append((url, "forbidden"))

        except requests.RequestException:
            pass

    if not found:
        print(Fore.CYAN + "[-] No sensitive files found.")

    return found

def get_domain_name(url):
    domain = urlparse(url).netloc.replace('.', '_').replace(':', '_')
    if not domain:
        domain = "scan_result"
    return domain

def save_to_json(scan_data):
    domain = get_domain_name(scan_data['url'])
    filename = f'{domain}_report.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scan_data, f, indent=4)
    
    print(Fore.YELLOW + f'\n[+] JSON-Report saved to {filename}')

def save_to_txt(scan_data):
    domain = get_domain_name(scan_data['url'])
    filename = f'{domain}_report.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'Security Report \n')
        f.write(f'URL: {scan_data["url"]}\n')
        f.write('-' * 50 + '\n')

        if scan_data['status'] == 'error':
            f.write(f'[!] Scan error: {scan_data["error_message"]}\n')
        else:
            f.write('\n--- Security Headers ---\n')
            for header, details in scan_data['headers'].items():
                if details['present']:
                    f.write(f"[+] FOUND: {header} -> {details['value']}\n")
                else:
                    f.write(f"[-] MISSING: {header} (Potential vulnerability!)\n")

        if 'sensitive_files' in scan_data and scan_data['sensitive_files']:
            f.write('\n--- Sensitive Files ---\n')
            for file_url, status in scan_data['sensitive_files']:
                f.write(f"[{status.upper()}] {file_url}\n")
        elif 'sensitive_files' in scan_data:
            f.write('\n--- Sensitive Files ---\n')
            f.write('No sensitive files found.\n')
                
    print(Fore.YELLOW + f'\n[+] TXT-Report saved to {filename}')
    
if __name__ == '__main__':
    print_banner()
    target_url = input("Enter the URL to scan (e.g., example.com): ").strip()
    
    if not target_url.startswith(('http://', 'https://')):
        target_url = 'http://' + target_url

    data = scan_headers(target_url)
    print_results_to_terminal(data)
    if data['status'] != 'error':
        sensitive_results = scan_sensitive_files(target_url)
    else:
        sensitive_results = []

    save_choice = input("\n Do you want to save the report? (j - JSON, t - TXT, jt - both, n - No): ").lower()

    data['sensitive_files'] = sensitive_results

    if save_choice == 'j':
        save_to_json(data)
    elif save_choice == 't':
        save_to_txt(data)
    elif save_choice in ['jt', 'tj']:
        save_to_json(data)
        save_to_txt(data)