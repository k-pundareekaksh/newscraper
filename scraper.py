import json
import requests
from bs4 import BeautifulSoup

def get_top_three_articles(homepage_url):
    response = requests.get(homepage_url)
    if response.status_code != 200:
        print(f"Failed to fetch {homepage_url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = []

    for a_tag in soup.find_all('a', href=True):
        link = a_tag['href']
        if 'articleshow' in link:  # Ensuring it's an article link
            if link.startswith('/'):
                link = "https://timesofindia.indiatimes.com" + link  # Convert to absolute URL
            article_links.append(link)
            if len(article_links) == 3:  # Limit to top 3 articles
                break

    return article_links

def extract_article_content(article_url):
    response = requests.get(article_url)
    if response.status_code != 200:
        print(f"Failed to fetch {article_url}")
        return {"title": "", "url": article_url, "content": "."}  # Ensuring required fields
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    title_tag = soup.find('title')
    title = title_tag.text.strip() if title_tag else ""

    # Extract article content
    content_div = soup.find('div', class_='_s30J clearfix') or soup.find('div', class_='Normal')
    content = " ".join(content_div.stripped_strings) if content_div else ""

    return {"title": title, "url": article_url, "content": content if content else "."}  # Ensuring content is not empty

def main():
    with open('urls.json', 'r') as file:
        urls = json.load(file)
    
    scraped_articles = []  # Flat list of article dictionaries

    for homepage in urls:
        top_articles = get_top_three_articles(homepage)
        
        for article_url in top_articles:
            article_details = extract_article_content(article_url)
            scraped_articles.append(article_details)
    
    with open('toi_articles.json', 'w', encoding="utf-8") as outfile:
        json.dump(scraped_articles, outfile, ensure_ascii=False, indent=4)  # Output in expected format
    
    print("Scraping complete. Saved to toi_articles.json")

if __name__ == "__main__":
    main()
