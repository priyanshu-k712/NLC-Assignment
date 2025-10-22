from bs4 import BeautifulSoup
import requests as r


def load_content_from_url(url):
    header = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/126.0.0.0 Safari/537.36"
    }
    response = r.get(url, headers=header, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    p_tags = soup.find_all("p")
    text = [tag.get_text(strip=True) for tag in p_tags if len(tag.get_text(strip=True)) > 0]
    return text


def load_content_from_file(filename):
    with open(filename, 'rb') as f:
        print(f.read())
        return f.read()

def load_ppt(path):
    with open(path, 'rb') as f:
        return f.read()