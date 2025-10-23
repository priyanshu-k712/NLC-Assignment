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
    # Remove markdown and whitespace
    content = re.sub(r"```(?:json)?|```", "", content).strip()

    # Extract first JSON array/object
    match = re.search(r"(\[.*\]|\{.*\})", content, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM output")

    json_text = match.group(0)

    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        snippet = json_text[max(0, e.pos - 20):e.pos + 20]
        raise ValueError(f"JSON parsing failed near: {snippet}\nOriginal error: {e}")