import json
import random
from pathlib import Path
from urllib.parse import urlparse

import pyfiglet
import requests
from colorama import Fore, Style, init
from tqdm import tqdm


# Constants used throughout the scanner.
DEFAULT_TIMEOUT = 5

# Paths and files that are often sensitive and should not be publicly accessible.
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
    ".DS_Store",
]

# Random user agents help avoid simplistic bot blocking.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
]

# Security headers to check on the target website.
SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def print_banner() -> None:
    """Display the program banner in the terminal."""
    ascii_banner = pyfiglet.figlet_format("MWVS")
    print(Fore.CYAN + Style.BRIGHT + ascii_banner + Style.RESET_ALL)
    print(Fore.YELLOW + "         v2.0 - Developed by l_yehor\n" + Style.RESET_ALL)
    print(Fore.CYAN + "_" * 60 + Style.RESET_ALL)


def get_random_headers() -> dict[str, str]:
    """Return a random User-Agent header for each request."""
    return {"User-Agent": random.choice(USER_AGENTS)}


def normalize_url(url: str) -> str:
    """Ensure the URL starts with http:// or https://."""
    if not url.startswith(("http://", "https://")):
        return f"http://{url}"
    return url


def get_domain_name(url: str) -> str:
    """Convert a URL into a safe filename prefix."""
    domain = urlparse(url).netloc.replace(".", "_").replace(":", "_")
    return domain or "scan_result"


def scan_headers(url: str) -> dict:
    """Check the target URL for common security headers."""
    results = {
        "url": url,
        "status": "error",
        "headers": {},
        "error_message": None,
    }

    try:
        response = requests.get(url, headers=get_random_headers(), timeout=DEFAULT_TIMEOUT)
        results["status"] = "success"
        response_headers = response.headers

        for header_name in SECURITY_HEADERS:
            results["headers"][header_name] = {
                "present": header_name in response_headers,
                "value": response_headers.get(header_name),
            }
    except requests.exceptions.RequestException as caught_error:
        results["error_message"] = str(caught_error)

    return results


def scan_sensitive_files(base_url: str) -> list[tuple[str, str]]:
    """Scan common sensitive file locations on the target host."""
    print(Fore.CYAN + "\n[+] Scanning for sensitive files...")
    print(Fore.CYAN + "_" * 60)

    found_files = []

    for path in tqdm(SENSITIVE_PATHS, desc="Scanning", colour="green", ncols=80):
        target_url = f"{base_url.rstrip('/')}/{path}"

        try:
            response = requests.get(target_url, headers=get_random_headers(), timeout=DEFAULT_TIMEOUT)
            if response.status_code == 200:
                tqdm.write(Fore.GREEN + f"[+] FOUND: {target_url}")
                found_files.append((target_url, "accessible"))
            elif response.status_code == 403:
                tqdm.write(Fore.YELLOW + f"[!] FORBIDDEN (exists?): {target_url}")
                found_files.append((target_url, "forbidden"))
        except requests.RequestException:
            # Ignore connection errors and continue scanning.
            continue

    if not found_files:
        print(Fore.CYAN + "[-] No sensitive files found.")

    return found_files


def print_results_to_terminal(scan_data: dict) -> None:
    """Print the header scan results to the console."""
    print(Fore.CYAN + f"\n[*] Analyzing security headers for: {scan_data['url']}")
    print(Fore.CYAN + "_" * 60)

    if scan_data["status"] == "error":
        print(Fore.RED + Style.BRIGHT + f"[!] Not connected to {scan_data['url']}.")
        print(Fore.RED + f"Error: {scan_data['error_message']}")
        return

    for header, details in scan_data["headers"].items():
        if details["present"]:
            print(Fore.GREEN + f"[+] FOUND: {header} -> {details['value']}")
        else:
            print(Fore.RED + f"[-] MISSING: {header} (Potential vulnerability!)")


def write_json_report(scan_data: dict) -> None:
    """Save the scan results as a JSON report."""
    filename = Path(f"{get_domain_name(scan_data['url'])}_report.json")
    filename.write_text(json.dumps(scan_data, indent=4, ensure_ascii=False), encoding="utf-8")
    print(Fore.GREEN + f"\n[+] JSON report saved to {filename}" + Style.RESET_ALL)


def write_text_report(scan_data: dict) -> None:
    """Save the scan results as a plain text report."""
    filename = Path(f"{get_domain_name(scan_data['url'])}_report.txt")
    lines = [
        "Security Report",
        f"URL: {scan_data['url']}",
        "-" * 50,
    ]

    if scan_data["status"] == "error":
        lines.append(f"[!] Scan error: {scan_data['error_message']}")
    else:
        lines.append("\n--- Security Headers ---")
        for header, details in scan_data["headers"].items():
            if details["present"]:
                lines.append(f"[+] FOUND: {header} -> {details['value']}")
            else:
                lines.append(f"[-] MISSING: {header} (Potential vulnerability!)")

    lines.append("\n--- Sensitive Files ---")
    sensitive_files = scan_data.get("sensitive_files", [])
    if sensitive_files:
        lines.extend(f"[{status.upper()}] {url}" for url, status in sensitive_files)
    else:
        lines.append("No sensitive files found.")

    filename.write_text("\n".join(lines), encoding="utf-8")
    print(Fore.GREEN + f"\n[+] TXT report saved to {filename}" + Style.RESET_ALL)


def ask_save_choice() -> str:
    """Ask the user whether to save the report."""
    return input(
        Fore.YELLOW
        + "\nDo you want to save the report? (j - JSON, t - TXT, jt - both, n - No): "
        + Style.RESET_ALL
    ).strip().lower()


def main() -> None:
    """Main program flow: banner, scan, and optional report saving."""
    print_banner()
    target_url = normalize_url(
        input(Fore.YELLOW + "Enter the URL to scan (e.g., example.com): " + Style.RESET_ALL).strip()
    )

    scan_data = scan_headers(target_url)
    print_results_to_terminal(scan_data)

    scan_data["sensitive_files"] = (
        scan_sensitive_files(target_url) if scan_data["status"] == "success" else []
    )

    save_choice = ask_save_choice()
    if save_choice == "j":
        write_json_report(scan_data)
    elif save_choice == "t":
        write_text_report(scan_data)
    elif save_choice in {"jt", "tj"}:
        write_json_report(scan_data)
        write_text_report(scan_data)


if __name__ == "__main__":
    init(autoreset=True)
    main()
