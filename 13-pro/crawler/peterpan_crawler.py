import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

def fetch_peterpan_rooms_by_query(query: str, page_limit: int = 1) -> pd.DataFrame:
    base_url = "https://www.peterpan.co.kr/searchRoom/result"
    encoded_query = quote(query)
    headers = {"User-Agent": "Mozilla/5.0"}

    results = []

    for page in range(1, page_limit + 1):
        params = {
            "currentPage": page,
            "searchType": "search",
            "room": "0",
            "price": "",
            "region": encoded_query,
        }

        try:
            response = requests.get(base_url, headers=headers, params=params, timeout=5)
            if response.status_code != 200:
                continue
        except Exception as e:
            print(f"Error: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select("div.a-house")

        for item in listings:
            try:
                price = item.select_one(".m-content__price").get_text(strip=True)
                address = item.select_one(".m-content__address").get_text(strip=True)
                structure = item.select(".m-content__text")[0].get_text(strip=True)
                rooms = item.select(".m-content__text")[1].get_text(strip=True)
                floor = item.select(".m-content__text")[2].get_text(strip=True)
                area = item.select(".m-content__text")[3].get_text(strip=True)
                desc = item.select_one(".m-content__description").get_text(strip=True)

                image_tag = item.select_one(".slider-image")
                img_url = image_tag['src'] if image_tag else ""

                tags = [tag.get_text(strip=True) for tag in item.select(".tag__wrapper p")]

                results.append({
                    "가격": price,
                    "주소": address,
                    "구조": structure,
                    "방": rooms,
                    "층수": floor,
                    "면적": area,
                    "설명": desc,
                    "썸네일": img_url,
                    "태그": ", ".join(tags)
                })

            except Exception as e:
                print(f"[ERROR] Skipped one item: {e}")
                continue

    return pd.DataFrame(results)