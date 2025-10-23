from bs4 import BeautifulSoup
import requests as r
import json
import re

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


def safe_load_json(content: str):
    # Remove markdown code fences if any
    s = re.sub(r"```(?:json)?|```", "", s).strip()

    # Extract only the first JSON array (non-greedy)
    match = re.search(r"\[.*?\]", s, re.DOTALL)
    if not match:
        raise ValueError("No JSON array found in the string")
    s = match.group(0)

    # Fix common trailing commas
    s = re.sub(r",\s*]", "]", s)
    s = re.sub(r",\s*}", "}", s)

    return json.loads(s)