import json
import time
import random
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import os
sys.stdout.reconfigure(encoding='utf-8')

def scrape_times_of_india(url, max_articles=3):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = '/usr/bin/chromium-browser'

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))

    articles = []
    article_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/articleshow/")]')

    article_urls = set()
    for link in article_links:
        href = link.get_attribute("href")
        if href and "/articleshow/" in href:
            article_urls.add(href)
        if len(article_urls) >= max_articles:
            break

    print(f"Found {len(article_urls)} articles on {url}.")

    for article_url in article_urls:
        driver.get(article_url)

        try:
            title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
        except:
            title = "Title Not Found"

        try:
            content_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "_s30J")]'))
            )
            content = content_element.text.replace("\n", " ")
        except:
            content = "Content Not Found"

        articles.append({
            "title": title,
            "url": article_url,
            "content": content
        })

        time.sleep(random.uniform(1, 3))

    driver.quit()
    return articles

if __name__ == "__main__":
    
    try:
        with open("urls.json", "r", encoding="utf-8") as f:
            urls = json.load(f)
    except FileNotFoundError:
        print("❌ Error: 'urls.json' file not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ Error: Invalid JSON format in 'urls.json'.")
        sys.exit(1)

    all_articles = []
    for url in urls:
        articles = scrape_times_of_india(url)
        all_articles.extend(articles)

    if all_articles:
        with open("toi_articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=4)
        print("✅ Scraping completed. Data saved to 'toi_articles.json'.")
    else:
        print("❌ No articles found.")
