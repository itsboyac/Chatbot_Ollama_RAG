import time  # FIXED: Correct import for sleep
from bs4 import BeautifulSoup
import pandas as pd
import os, glob, requests

all_links = []
base_url = "https://theconversation.com"

for filepath in glob.glob("data/raw/*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article", class_="result")
        
        for article in articles:
            # Safer tag finding to avoid NoneType errors
            h1 = article.find("h1", class_="legacy")
            if h1:
                title_tag = h1.find("a")
                if title_tag:
                    all_links.append({
                        "title": title_tag.get_text(strip=True), 
                        "url": base_url + title_tag['href']
                    })

df = pd.DataFrame(all_links).drop_duplicates(subset=['url'])
print(f"Extracted {len(df)} unique links. Starting deep scrape...")


full_data = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
for index, row in df.iterrows():
    try:
        response = requests.get(row['url'], headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        article_body = (
            soup.find("div", class_="content-body") or 
            soup.find("div", class_="article-body") or 
            soup.find("article")
        )
        if article_body:
            '''
            # Clean up the HTML before extracting text
            for div in article_body.find_all("div", class_="newsletter-signup"):
                div.decompose()
            '''
            content = article_body.get_text(separator="\n", strip=True)
            full_data.append({
                "title": row['title'],
                "url": row['url'],
                "content": content
            })
            print(f"Success: {row['title'][:30]}...")
        time.sleep(1.5) 
    except Exception as e:
        print(f"Error fetching {row['url']}: {e}")


os.makedirs("data/processed", exist_ok=True) 
df_final = pd.DataFrame(full_data)
df_final.to_csv("data/processed/cat_articles.csv", index=False)
print("Saved processed data to data/processed/cat_articles.csv")