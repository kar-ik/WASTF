import requests
from bs4 import BeautifulSoup
import os

def log_to_report(message):
    os.makedirs("report", exist_ok=True)
    with open("report/test_report.txt", "a") as report:
        report.write(message + "\n")

def send_request(url):
    try:
        response = requests.get(url)
        return response
    except requests.RequestException as e:
        log_to_report(f"[!] Error reaching {url}: {e}")
        return None

