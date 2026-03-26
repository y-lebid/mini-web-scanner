# 🛡️ Mini Web Vulnerability Scanner

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Простий, швидкий та ефективний CLI-інструмент на Python для базового аудиту безпеки веб-додатків. Створений для розробників, які хочуть швидко перевірити свої сайти на поширені помилки конфігурації.

## 🚀 Можливості (MVP 1.0)

* **Аналіз Security Headers:** Перевірка наявності критичних HTTP-заголовків (HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy тощо).
* **Terminal UI:** Зручний та зрозумілий кольоровий вивід результатів завдяки `colorama`.

## 📸 Як це виглядає

<!-- ![screenshot](path/to/image.png) -->

## 🛠️ Встановлення та запуск

1. Склонуйте репозиторій:
   ```bash
   git clone https://github.com/y-lebid/mini-web-scanner.git
   cd mini-web-scanner

2. Встановіть залежності
   ```bash
   pip install requests colorama
   ```
3. Запустіть
   ```bash
   python scanner.py
   ```

## 🗺️ Roadmap
* **Розширений аналіз HTTP-заголовків безпеки**
* **Directory Bruteforce (пошук прихованих файлів: /.env, /.git, robots.txt)**
* **Підміна User-Agent для обходу базового WAF**
* **Генерація звітів у форматах .txt та .json**
## 📄 Ліцензія

Цей проєкт розповсюджується під ліцензією GNU GPLv3. Детальніше читайте у файлі **LICENSE**.

## ⚠️ Відмова від відповідальності

Цей інструмент створено виключно в освітніх цілях. Використовуйте його лише на власних серверах або системах, на сканування яких у вас є явний дозвіл. Автор не несе відповідальності за неправомірне використання.