import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


def is_bit_link(data):
    parsed_link = urlparse(data["url"])
    url = "https://" + parsed_link.netloc + parsed_link.path
    true_url = False
    clc_bit_link = False
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.ok:
            true_url = True
            if "clc.li" in url:
                clc_bit_link = True
        return true_url, clc_bit_link
    except requests.exceptions.HTTPError:
        return None
    except Exception:
        return None


def get_shorten_link(data, token):
    url = "https://clc.li/api/url/add"
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        get_link = response.json().get("shorturl")
        parsed_link = urlparse(get_link)
        short_link = parsed_link.netloc + parsed_link.path
        return short_link
    except requests.exceptions.HTTPError:
        return None


def count_clicks(token):
    try:
        url = f"https://clc.li/api/urls?limit=2&page=1&order=date"
        headers = {"Authorization": "Bearer {token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        clicks = response.json().get("data").get("urls")[0].get("clicks")
        return clicks
    except requests.exceptions.HTTPError:
        return None


def main():
    load_dotenv()
    token = os.getenv("AUTH_TOKEN")
    data = {"url": input("Введите URL: ")}
    check_link = is_bit_link(data)
    if not check_link:
        print("Ошибка: Введите действующий url")
    else:
        true_url, clc_bit_link = is_bit_link(data)
        if clc_bit_link:
            clicks = count_clicks(token)
            print("Всего кликов: ", clicks)
        else:
            short_link = get_shorten_link(data, token)
            print("Короткая ссылка: ", short_link)


if __name__ == "__main__":
    main()

