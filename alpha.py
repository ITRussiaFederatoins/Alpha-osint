import json
import socket
import urllib.request
import os
import sys
import time
import hashlib
import re
import html
import ctypes

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def logo():
    print(f"""{BLUE}{BOLD}
  /$$$$$$  /$$           /$$                
 /$$__  $$| $$          | $$                
| $$  \ $$| $$  /$$$$$$ | $$$$$$$   /$$$$$$ 
| $$$$$$$$| $$ /$$__  $$| $$__  $$ |____  $$
| $$__  $$| $$| $$  \ $$| $$  \ $$  /$$$$$$$
| $$  | $$| $$| $$  | $$| $$  | $$ /$$__  $$
| $$  | $$| $$| $$$$$$$/| $$  | $$|  $$$$$$$
|__/  |__/|__/| $$____/ |__/  |__/ \_______/
              | $$                          
              | $$                          
              |__/                          
          @qertyaaj
Введите Ip-Адрес или номер телефона для поиска
    {RESET}""")


def clear():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\n" * 100)


def check_internet():
    try:
        urllib.request.urlopen('https://google.com', timeout=7)
        return True
    except urllib.error.URLError:
        return False


def strip_tags(html_text):
    return re.sub('<[^<]+?>', '', html_text)


def scan_phoneradar(phone):
    try:
        FRURL = f'http://phoneradar.ru/phone/{phone}'
        with urllib.request.urlopen(FRURL, timeout=7) as response:
            html_content = response.read().decode('utf-8')

        match_danger = re.search(r'<div class="alert alert-danger">(.*?)</div>', html_content, re.DOTALL)
        match_table = re.search(r'<table class="table">(.*?)</table>', html_content, re.DOTALL)

        if match_danger:
            reviews_rev = match_danger.group(1).strip()
        elif match_table:
            reviews_rev = match_table.group(1).strip()
        else:
            reviews_rev = 'Не удалось найти информацию на PhoneRadar.'

        reviews_rev = html.unescape(reviews_rev)
        reviews_rev = strip_tags(reviews_rev)

        lines = reviews_rev.split('\n')
        lines = [line.strip() for line in lines if line.strip()]  # Убираем лишние пробелы и пустые строки

        formatted_lines = []
        i = 0
        while i < len(lines):
            if i + 1 < len(lines):
                key = lines[i]
                value = lines[i + 1]
                formatted_line = f"{YELLOW}├ {BOLD}{BLUE}{key}: {value}{RESET}"
                formatted_lines.append(formatted_line)
                i += 2
            else:
                # На случай, если количество строк нечетное
                formatted_line = f"{YELLOW}├ {BOLD}{BLUE}{lines[i]}{RESET}"
                formatted_lines.append(formatted_line)
                i += 1

        reviews_rev = '\n'.join(formatted_lines)

        return {
            "reviews_rev": reviews_rev,
            "FRURL": FRURL
        }
    except urllib.error.URLError:
        return None
    except Exception as e:
        print(f"{RED}{BOLD}В ходе PhoneRadar сканирования произошла ошибка!{RESET}")
        print(e)
        return None


def get_ip_info(ip_address):
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip_address}") as response:
            data = json.loads(response.read().decode('utf-8'))
        return data
    except urllib.error.URLError as e:
        print(f"{RED}{BOLD}Ошибка при запросе к API: {e}{RESET}")
        return None


def print_ip_info(ip_info):
    if not ip_info:
        print(f"{RED}{BOLD}Информация об IP-адресе не найдена.{RESET}")
        return

    print(f"{YELLOW}{BOLD}Информация об IP-адресе:{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}IP-адрес: {ip_info.get('query', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Страна: {ip_info.get('country', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Город: {ip_info.get('city', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Регион: {ip_info.get('regionName', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Почтовый индекс: {ip_info.get('zip', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Широта: {ip_info.get('lat', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Долгота: {ip_info.get('lon', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Часовой пояс: {ip_info.get('timezone', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Провайдер: {ip_info.get('isp', 'N/A')}{RESET}")
    print(f"{YELLOW}├ {BOLD}{BLUE}Организация: {ip_info.get('org', 'N/A')}{RESET}")
    print(f"{YELLOW}└ {BOLD}{BLUE}AS: {ip_info.get('as', 'N/A')}{RESET}")


def is_valid_ip(ip_address):
    try:
        socket.inet_aton(ip_address)
        return True
    except socket.error:
        return False


if __name__ == "__main__":
    clear()
    logo()

    while True:
        try:
            user_input = input(f"({CYAN}{BOLD}root@ReaperSoft{RESET}{BLUE}{BOLD}){RESET} Введите запрос: ")
            if user_input.startswith("+"):
                phone = re.sub(r"\D", "", user_input)
                FormattedPhoneNumber = "+" + phone
                if check_internet():
                    print(f"\n{GREEN}{BOLD}Интернет-соединение установлено.{RESET}")

                    phoneradar_data = scan_phoneradar(phone)
                    if phoneradar_data is not None:
                        time.sleep(0.5)
                        print(f"\n{GREEN}{BOLD}PhoneRadar сканирование завершено.{RESET}")
                        print(
                            f"\n{YELLOW}{BOLD}Результаты PhoneRadar сканирования:{RESET}\n{phoneradar_data['reviews_rev']}\n{YELLOW}├\n{YELLOW}├ {BOLD}{BLUE}Полный отчёт:{RESET}\n{YELLOW}└ {BOLD}{BLUE}{UNDERLINE}{phoneradar_data['FRURL']}{RESET}{YELLOW}{BOLD}{BLUE}.{RESET}")
                    else:
                        print(f"\n{RED}{BOLD}Ошибка: Не удалось получить данные с PhoneRadar.{RESET}")

                    print(
                        f"\n{YELLOW}{BOLD}Дополнительная информация:{RESET}\n{YELLOW}├ {BOLD}{BLUE}WhatsApp: {UNDERLINE}https://api.WhatsApp.com/send?phone={phone}{RESET}{YELLOW}{BOLD}{BLUE};{RESET}\n{YELLOW}├ {BOLD}{BLUE}Viber: {UNDERLINE}viber://add?number={phone}{RESET}{YELLOW}{BOLD}{BLUE};{RESET}\n{YELLOW}└ {BOLD}{BLUE}Skype звонок: {UNDERLINE}skype:{phone}?call{RESET}{YELLOW}{BOLD}{BLUE}.{RESET}")
                    print(
                        f"\n{YELLOW}{BOLD}Проверка номера в социальных сетях:{RESET}\n{YELLOW}├ {BOLD}{BLUE}Instagram: {UNDERLINE}https://www.instagram.com/accounts/password/reset{RESET}{YELLOW}{BOLD}{BLUE};{RESET}\n{YELLOW}├ {BOLD}{BLUE}ВКонтакте: {UNDERLINE}https://vk.com/restore{RESET}{YELLOW}{BOLD}{BLUE};{RESET}\n{YELLOW}├ {BOLD}{BLUE}FaceBook: {UNDERLINE}https://facebook.com/login/identify/?ctx=recover&ars=royal_blue_bar{RESET}{YELLOW}{BOLD}{BLUE};{RESET}\n{YELLOW}├ {BOLD}{BLUE}Twitter: {UNDERLINE}https://twitter.com/account/begin_password_reset{RESET}{YELLOW}{BOLD}{BLUE};{RESET}\n{YELLOW}└ {BOLD}{BLUE}Linkedin: {UNDERLINE}https://linkedin.com/checkpoint/rp/request-password-reset-submit{RESET}{YELLOW}{BOLD}{BLUE}.{RESET}")
                else:
                    print(f"{RED}{BOLD}Отсутствует интернет-соединение!{RESET}")
            elif is_valid_ip(user_input):
                ip_info = get_ip_info(user_input)
                print_ip_info(ip_info)
            else:
                print(f"{RED}{BOLD}Неверный формат ввода. Введите номер телефона с '+' или корректный IP-адрес.{RESET}")

        except KeyboardInterrupt:
            print(f"\n{RED}{BOLD}Программа завершена.{RESET}")
            break
