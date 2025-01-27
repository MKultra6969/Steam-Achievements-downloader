import re
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from colorama import Fore, Style
import pyfiglet


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_achievements_from_steam(game_id, output_dir):
    url = f"https://steamcommunity.com/stats/{game_id}/achievements"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    resolution_choice = input(Fore.YELLOW +
                              "Скачать в оригинальном разрешении " + Fore.GREEN + "(О)\n" +
                              Fore.YELLOW + "Или 100x100 pix для стикеров Телеграм " + Fore.GREEN + "(1)?").strip().lower()
    if resolution_choice == '1':
        img_size = (100, 100)
    else:
        img_size = None

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"{Fore.RED}Не удалось загрузить страницу. Код ответа: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}URL: {url}{Style.RESET_ALL}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        achievements_section = soup.find_all('div', class_='achieveRow')
        if not achievements_section:
            print(f"{Fore.RED}Достижения отсутствуют или они скрыты.{Style.RESET_ALL}")
            return

        for achievement in achievements_section:
            title_tag = achievement.find('h3')
            if not title_tag:
                print(f"{Fore.RED}Название достижения не найдено, пропущено.{Style.RESET_ALL}")
                continue

            title = title_tag.text.strip()

            img_tag = achievement.find('img')
            if not img_tag or 'src' not in img_tag.attrs:
                print(f"{Fore.RED}Пропущено: {title}{Style.RESET_ALL}")
                continue

            img_url = img_tag['src']

            if not img_url.startswith("http"):
                img_url = "https://cdn.cloudflare.steamstatic.com" + img_url

            img_response = requests.get(img_url, headers=headers)
            if img_response.status_code != 200:
                print(f"{Fore.RED}Не удалось скачать изображение для: {title}. Код ответа: {img_response.status_code}{Style.RESET_ALL}")
                continue

            img = Image.open(BytesIO(img_response.content))
            if img_size:
                img_resized = img.resize(img_size)
            else:
                img_resized = img

            sanitized_title = sanitize_filename(title)
            img_path = os.path.join(output_dir, f"{sanitized_title}.png")
            img_resized.save(img_path, 'PNG')

            print(f"{Fore.LIGHTGREEN_EX}Сохранено: {title} -> {img_path}{Style.RESET_ALL}")

        next_step()

    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Ошибка при выполнении запроса: {e}{Style.RESET_ALL}")


def show_menu():
    logo = pyfiglet.figlet_format("SA D", font="defleppard")
    print(Fore.CYAN + Style.BRIGHT + logo + Style.RESET_ALL)
    print(Fore.CYAN + "Steam Achievements Downloader" + Style.RESET_ALL)
    print(Fore.MAGENTA + "By MKultra69" + Style.RESET_ALL)
    print(Fore.BLUE + "\n1. Скачать иконки достижений")
    print(Fore.YELLOW + "2. Инфо")
    print(Fore.RED + Style.BRIGHT + "3. EXIT")


def show_info():
    print(Fore.MAGENTA + """
    Этот скрипт позволяет скачивать иконки достижений игр напрямую с Steam.
    Просто введите ID игры, и скрипт автоматом загрузит все доступные иконки и сохранит их в виде PNG.
    Скрипт создавался па приколу, поэтому мне ваще пахую хех=)
    By MKultra69
    """ + Style.RESET_ALL)

    input(Fore.LIGHTGREEN_EX + "ТЫК 'enter' для возврата в главное меню..." + Style.RESET_ALL)


def next_step():
    print(Fore.CYAN + "\nЧе делаем дальше?")
    print(Fore.BLUE + "1. Другая игра")
    print(Fore.RED + "2. Выйти")

    choice = input(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Выберите действие (1-2): ").strip()

    if choice == "1":

        game_id = input(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Введите ID игры: ").strip()

        output_dir = f"achievements_{game_id}"

        download_achievements_from_steam(game_id, output_dir)

    elif choice == "2":
        print(Fore.RED + "Выход из программы..." + Style.RESET_ALL)
        exit()

    else:
        print(Fore.RED + "Неверный выбор, попробуйте снова." + Style.RESET_ALL)
        next_step()


def main():
    while True:
        show_menu()
        choice = input(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Выберите действие (1-3): ").strip()

        if choice == "1":

            game_id = input(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Введите ID игры: ").strip()

            output_dir = f"achievements_{game_id}"

            download_achievements_from_steam(game_id, output_dir)

        elif choice == "2":
            show_info()

        elif choice == "3":
            print(Fore.RED + "Выход из программы..." + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Неверный выбор, попробуйте снова." + Style.RESET_ALL)


# Запуск программы
if __name__ == "__main__":
    main()



# Комментарии добавил M.K.

# Я БАЛЬНОЙ НАГАЛАВУ

# САНЯ ПРИВЕТ

# ███████████████████████████████████████████████████████████████████
# █▌                                                               ▐█
# █▌  ███▄ ▄███▓ ██ ▄█▀ █    ██  ██▓  ▄▄▄█████▓ ██▀███   ▄▄▄       ▐█
# █▌ ▓██▒▀█▀ ██▒ ██▄█▒  ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄     ▐█
# █▌ ▓██    ▓██░▓███▄░ ▓██  ▒██░▒██░  ▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄   ▐█
# █▌ ▒██    ▒██ ▓██ █▄ ▓▓█  ░██░▒██░  ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██  ▐█
# █▌ ▒██▒   ░██▒▒██▒ █▄▒▒█████▓ ░██████▒▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒ ▐█
# █▌ ░ ▒░   ░  ░▒ ▒▒ ▓▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▐█
# █▌ ░  ░      ░░ ░▒ ▒░░░▒░ ░ ░ ░ ░ ▒  ░  ░      ░▒ ░ ▒░  ▒   ▒▒ ░ ▐█
# █▌ ░      ░   ░ ░░ ░  ░░░ ░ ░   ░ ░   ░        ░░   ░   ░   ▒    ▐█
# █▌        ░   ░  ░      ░         ░  ░          ░           ░  ░ ▐█
# █▌                                                               ▐█
# ███████████████████████████████████████████████████████████████████