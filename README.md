# 🛡️ Mini Web Vulnerability Scanner

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

A simple, fast, and effective Python CLI tool for basic web application security audits. Designed for developers who want to quickly check their sites for common configuration errors.

## 🚀 Features (MVP 1.0)

* **Security Headers Analysis:** Checks for the presence of critical HTTP headers (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, etc.).
* **Terminal UI:** Convenient and intuitive color-coded output of results thanks to `colorama`.

## 📸 What it looks like
<img width="703" height="375" alt="image" src="https://github.com/user-attachments/assets/2c5105e0-2451-4a03-8e62-60225097770f" />

<!-- ![screenshot](path/to/image.png) -->

## 🛠️ Installation and setup

1. Clone the repository:
   ```bash
   git clone https://github.com/y-lebid/mini-web-scanner.git
   cd mini-web-scanner

2. Install dependencies
   ```bash
   pip install requests colorama
   ```
3. Run
   ```bash
   python scanner.py
   ```

## 🗺️ Roadmap
* **Advanced analysis of HTTP security headers**
* **Directory Bruteforce (search for hidden files: /.env, /.git, robots.txt)**
* **User-Agent spoofing to bypass basic WAFs**
* **Report generation in .txt and .json formats**
## 📄 License

This project is distributed under the GNU GPLv3 license. For more details, see the **LICENSE** file.

## ⚠️ Disclaimer

This tool is designed for both educational purposes and practical web application security audits. The end user bears sole responsibility for the use of this scanner.

Use this software product only on your own servers, systems, or targets for which you have **express permission** to test (for example, as part of Bug Bounty programs). The project author is not liable for any damages, server disruptions, or any other misuse of this tool.
