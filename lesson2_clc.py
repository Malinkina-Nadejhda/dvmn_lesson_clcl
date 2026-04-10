import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os


def is_bit_link(user_url):
    parsed_url = urlparse(user_url["url"])
    scheme = "https"
    url = f"{scheme}://{parsed_url.netloc}{parsed_url.path}"
    response = requests.get(url)
    response.raise_for_status()
    bit_link = "clc.li" in url
    return bit_link


def get_shorten_link(user_url, token):
    url = "https://clc.li/api/url/add"
    headers = {"Authorization": f"Bearer {token}",
               "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=user_url)
    response.raise_for_status()
    short_url = response.json().get("shorturl")
    parsed_short_url = urlparse(short_url)
    short_link = f"{parsed_short_url.netloc}{parsed_short_url.path}"
    return short_link


def count_clicks(token):
    url = "https://clc.li/api/urls"
    params = {
        "limit": 2,
        "page": 1,
        "order": "date"
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    clicks = response.json().get("data").get("urls")[1].get("clicks")
    return clicks


def main():
    load_dotenv()
    user_url = {"url": input("Введите URL: ")}
    try:
        token = os.environ["CLC_LI_TOKEN"]
        bit_link = is_bit_link(user_url)
        if bit_link:
            clicks = count_clicks(token)
            print("Всего кликов: ", clicks)
        else:
            short_link = get_shorten_link(user_url, token)
            print("Короткая ссылка: ", short_link)
    except KeyError:
        print("Ошибка, не найден токен авторизации!")
    except requests.exceptions.HTTPError:
        print("Пожалуйста, проверьте URL или токен")
    except Exception:
        print("Ошибка: Введите действующий url")


if __name__ == "__main__":
    main()





