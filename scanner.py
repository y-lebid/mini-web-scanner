import requests
from colorama import init, Fore, Style
import json
from urllib.parse import urlparse

init(autoreset=True)

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

    try:
        response = requests.get(url, timeout=5)
        results['status'] = 'success'
        response_headers = response.headers

        for header in security_headers:
            if header in  response_headers:
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

    return results
    
def print_results_to_terminal(scan_data):
    url = scan_data['url']
    print(Fore.CYAN + f'\n[*] Analyzing security headers for: {url}')
    print(Fore.CYAN + '_' * 60)

    if scan_data['status'] == 'error':
        print(Fore.RED + Style.BRIGHT + f'[!] No connected to {url}.')
        print(Fore.RED + f'Error: {scan_data["error_message"]}')

    for header, details in scan_data['headers'].items():
        if details['present']:
            print(Fore.GREEN + f'[+] FOUND: {header} -> {details['value']}')
        else:
            print(Fore.RED + f'[-] MISSING: {header} (Potential vulnerability!)')


def save_to_json(scan_data):
    domain = urlparse(scan_data['url']).netloc.replace('.', '_')
    filename = f'{domain}_report.json'

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scan_data, f, indent=4)
    
    print(Fore.YELLOW + f'\n[+] JSON-Report saved to {filename}')

def save_to_txt(scan_data):
    domain = urlparse(scan_data['url']).netloc.replace('.', '_')
    filename = f'{domain}_report.txt'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f'Security Report (Security Headers) \n')
        f.write(f'URL: {scan_data["url"]}\n')
        f.write('-' * 50 + '\n')

        if scan_data['status'] == 'error':
            f.write(f'[!] Scan error: {scan_data["error_message"]}\n')
        else:
            for header, details in scan_data['headers'].items():
                if details['present']:
                    f.write(f'[+] FOUND: {header} -> {details['value']}\n')
                else:
                    f.write(f'[-] MISSING: {header} (Potential vulnerability!)\n')

                
    print(Fore.YELLOW + f'\n[+] TXT-Report saved to {filename}')
    
if __name__ == '__main__':
    target_url = input("Enter the URL to scan for security headers: ")
    data = scan_headers(target_url)
    print_results_to_terminal(data)
    save_choice = input("\nDo you want to save the report? (j - JSON, t - TXT, n - No): ").lower()
    if save_choice == 'j':
        save_to_json(data)
    elif save_choice == 't':
        save_to_txt(data)
    elif save_choice == 'jt' or save_choice == 'tj':
        save_to_json(data)
        save_to_txt(data)