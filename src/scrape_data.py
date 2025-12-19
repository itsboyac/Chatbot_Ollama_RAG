import requests, time, os

cat_article = {"page1": "https://theconversation.com/europe/search?q=cat",
       "page2": "https://theconversation.com/europe/search?page=2&q=cat",
       "page3": "https://theconversation.com/europe/search?page=3&q=cat",
       "page4": "https://theconversation.com/europe/search?page=4&q=cat",
       "page5": "https://theconversation.com/europe/search?page=5&q=cat",
       "page6": "https://theconversation.com/europe/search?page=6&q=cat",
       "page7": "https://theconversation.com/europe/search?page=7&q=cat",
       "page8": "https://theconversation.com/europe/search?page=8&q=cat",
       "page9": "https://theconversation.com/europe/search?page=9&q=cat",
       "page10": "https://theconversation.com/europe/search?page=10&q=cat"}

os.makedirs("data/raw", exist_ok=True)

for label, url in cat_article.items():
    filename = f"data/raw/{label}.html"
    respnse = requests.get(url)
    with open(filename, "wb") as f:
        f.write(respnse.content)
        time.sleep(2)
    print(f"Saved {filename}")
    
