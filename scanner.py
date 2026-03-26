import requests
from colorama import init, Fore, Style

init(autoreset=True)

def check_security_headers(url):
    print(f"\n[*] Analyzing security headers for {url}")
    print("-" * 50)

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        sequrity_headers = [
            'Strict-Transport-Security',
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Referrer-Policy',
            'Permissions-Policy'
        ]

        for header in sequrity_headers:
            if header in  headers:
                print(Fore.GREEN +f"[+] Found: {header} -> {headers[header]}")
            else:
                print(Fore.RED + f"[-] MISSING: {header} (Potential vulnerability!)")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"[!] No connection to {url}. Error: {e}")

    
if __name__ == "__main__":
    target_url = input("Enter the URL to scan for security headers: ")
    check_security_headers(target_url)