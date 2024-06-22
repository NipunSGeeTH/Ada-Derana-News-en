import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_adaderana_page(url):
    """Scrapes news articles from a single page of Ada Derana."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'lxml')
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []

    articles = []
    article_elements = soup.find_all('div', class_='news-story')

    for article_element in article_elements:
        try:
            # Extract title and link
            title_element = article_element.find('h2').find('a')
            title = title_element.text.strip() if title_element else "N/A"
            link = title_element['href'] if title_element else "N/A"
            news_id = link.split("/")[-1] if link else "N/A"

            # Extract date and time
            date_time_element = article_element.find('span')
            date_time = date_time_element.text.strip() if date_time_element else "N/A"

            # Extract image link
            image_element = article_element.find('div', class_='thumb-image').find('img')
            image_link = image_element['src'] if image_element else "N/A"

            # Extract short paragraph
            short_paragraph_element = article_element.find('p')
            short_paragraph = short_paragraph_element.text.strip() if short_paragraph_element else "N/A"

            articles.append({
                'news_id': news_id,
                'title': title,
                'link': link,
                'date_time': date_time,
                'image_link': image_link,
                'short_paragraph': short_paragraph
            })
        except Exception as e:
            print(f"Error scraping article: {e}")

    return articles

if __name__ == '__main__':
    base_url = 'https://www.adaderana.lk/hot-news/?pageno='
    num_pages = 1  # Scrape the first 1 pages (adjust as needed)

    all_articles = []

    for page in range(1, num_pages + 1):
        url = f"{base_url}{page}"
        print(f"Scraping page: {url}")
        try:
            articles = scrape_adaderana_page(url)
            all_articles.extend(articles)
        except Exception as e:
            print(f"Error scraping page {page}: {e}")
        time.sleep(1)

    try:
        with open("Adaderana_articles_headlines.json", "w", encoding='utf-8') as json_file:
            json.dump(all_articles, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

    # Output or further process the scraped data
    for article in all_articles:
        print("News ID:", article['news_id'])
        print("Title:", article['title'])
        print("Link:", article['link'])
        print("Date/Time:", article['date_time'])
        print("Image:", article['image_link'])
        print("\n")


    # Load the news articles
try:
    with open('Adaderana_articles_headlines.json', 'r', encoding='utf-8') as f:
        articles = json.load(f)
except Exception as e:
    print(f"Error loading JSON file: {e}")
    articles = []

if articles:
    Full_News_With_Contents = []
    for article in articles:
        try:
            url = article['link']
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Fetch the article page
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Parse the page content
            soup = BeautifulSoup(response.content, 'lxml')

            # Find the news content
            paragraph_div = soup.find('div', class_='news-content')
            if paragraph_div:
                paragraphs = paragraph_div.find_all('p', recursive=False)
                full_text = '\n'.join([p.text.strip() for p in paragraphs])
                print(full_text)
            else:
                full_text = "Full article content not found."

            # Prepare the news item
            news_item = {
                "ID": article['news_id'],
                "Title": article['title'],
                "Link": article['link'],
                "Date": article['date_time'],
                "Image": article['image_link'],
                "short_paragraph": article.get('short_paragraph', ''),
                "Paragraph": full_text
            }
            Full_News_With_Contents.append(news_item)
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
        except Exception as e:
            print(f"Error processing article {article['news_id']}: {e}")

    # Save the news with contents to a new JSON file
    try:
        with open('Full_News_With_Contents.json', 'w', encoding='utf-8') as f:
            json.dump(Full_News_With_Contents, f, ensure_ascii=False, indent=4)
        print("Full news with contents saved successfully.")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
else:
    print("No articles to process.")