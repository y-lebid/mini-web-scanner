# 🛡️ Mini Web Vulnerability Scanner

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A simple, fast, and effective Python CLI tool for basic web application security audits. Designed for developers who want to quickly check their sites for common configuration errors.

## 🚀 Features (Release 2.0)

- [x] - **Security Headers Analysis:** Checks for the presence of critical HTTP headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, etc.).
- [x] - **Directory Bruteforce:** Actively scans for exposed hidden files and directories (e.g., `/.env`, `/.git/`, `backup.zip`, `wp-config.php`).
- [x] - **Report Generation:** Export your scan results in structured `.json` or readable `.txt` formats for further analysis.
- [x] - **Anti-Bot Evasion:** Uses randomized `User-Agent` headers to bypass basic WAFs and server restrictions.
- [x] - **Interactive Terminal UI:** Convenient color-coded output (`colorama`) with a sleek real-time progress bar (`tqdm`).

## 📸 What it looks like
<img width="863" height="401" alt="image" src="https://github.com/user-attachments/assets/5463bd8f-96ce-4ac9-8774-4754c30e1806" />


<!-- ![screenshot](path/to/image.png) -->

## 🛠️ Installation and setup

1. Clone the repository:
   ```bash
   git clone https://github.com/y-lebid/mini-web-scanner.git
   cd mini-web-scanner

2. Install dependencies
   ```bash
   pip install requests colorama tqdm
   ```
3. Run
   ```bash
   python scanner.py
   ```

## 🗺️ Roadmap
- [ ] - **Port Scanner Module: Add functionality to check for common open ports (e.g., 21, 22, 80, 443, 3306).**
- [ ] - **Multithreading: Speed up directory scanning using Python's ThreadPoolExecutor.**
- [ ] - **Basic Vulnerability Checks: Add simple payload injections to test for basic SQLi or XSS reflections.**
- [ ] - **ASCII Art Logo: Add a cool startup banner for extra hacker aesthetics.**
## 📄 License

This project is distributed under the GNU GPLv3 license. For more details, see the **LICENSE** file.

## ⚠️ Disclaimer

This tool is designed for both educational purposes and practical web application security audits. The end user bears sole responsibility for the use of this scanner.

Use this software product only on your own servers, systems, or targets for which you have **express permission** to test (for example, as part of Bug Bounty programs). The project author is not liable for any damages, server disruptions, or any other misuse of this tool.
