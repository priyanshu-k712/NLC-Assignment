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
        return f.read()

def load_ppt(path):
    with open(path, 'rb') as f:
        return f.read()


def safe_load_json_from_string(input_str: str):
    if not input_str:
        raise ValueError("Input string is empty")

    # Remove Markdown code fences
    cleaned_str = re.sub(r"```(?:json)?|```", "", input_str).strip()

    # Remove Markdown formatting (**bold**, *italic*, `code`, # headings)
    cleaned_str = re.sub(r"\*\*(.*?)\*\*", r"\1", cleaned_str)
    cleaned_str = re.sub(r"\*(.*?)\*", r"\1", cleaned_str)
    cleaned_str = re.sub(r"`(.*?)`", r"\1", cleaned_str)
    cleaned_str = re.sub(r"#+\s*", "", cleaned_str)

    # Try to extract JSON array or object
    match = re.search(r"(\[.*\]|\{.*\})", cleaned_str, re.DOTALL)
    if not match:
        raise ValueError("No JSON structure found in the string")

    json_str = match.group(0)

    # Remove trailing commas
    json_str = re.sub(r",\s*([\]}])", r"\1", json_str)

    # Try parsing safely
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print("\n⚠️ JSON parsing failed. Here's what was received:\n", json_str[:500])
        raise ValueError(f"Invalid JSON format: {e}")
