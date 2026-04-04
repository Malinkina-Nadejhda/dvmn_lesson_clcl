import requests
from urllib.parse import urlparse


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
            if  "clc.li" in url:
                clc_bit_link = True
        return true_url, clc_bit_link
    except requests.exceptions.HTTPError:
        return None
    except Exception:
        return None


def get_shorten_link(data):
    url = "https://clc.li/api/url/add"
    headers = {"Authorization": "TOKEN",
               "Content-Type": "application/json"}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        short_link = response.json().get("shorturl")
        link_id = response.json().get("id")
        return short_link, link_id
    except requests.exceptions.HTTPError:
        return None

def count_clicks(link_id):
    try:
        url = f"https://clc.li/api/url/{link_id}"
        headers = {"Authorization": "TOKEN"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        clicks = response.json().get("data").get("clicks")
        return clicks
    except requests.exceptions.HTTPError:
        return None

def main():
    data = {"url": input("Введите URL: ")}
    check_link = is_bit_link(data)
    if not check_link:
        print("Ошибка: Введите действующий url")
    else:
        true_url, clc_bit_link = is_bit_link(data)
        if clc_bit_link:
            parsed_link = urlparse(data["url"])
            link_id = parsed_link.path[1:]
            clicks = count_clicks(link_id)
            print("Всего кликов", clicks)



if __name__ == "__main__":
    main()