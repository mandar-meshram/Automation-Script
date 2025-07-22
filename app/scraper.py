import requests
from bs4 import BeautifulSoup
from datetime import datetime
from .utils import save_debug_html, DELAY, HEADERS, logger
import time


def fetch_news(url):
    try:
        logger.info(f'[Scraping] {url}')
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            logger.error(f'[Error] Failed to fetch {url} with status code {response.status_code}')
            return []
        save_debug_html(response)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = []

        for article in soup.select('div.story-card'):
            headline_elem = article.select_one('a[data-testid="Heading"]')
            if not headline_elem:
                continue
            headline = headline_elem.text.strip()
            link = "https://www.reuters.com" + headline_elem['href']
            time_elem = article.find('time')
            date_str = time_elem['datetime'] if time_elem else str(datetime.now().date())

            articles.append({
                'headline': headline,
                'link': link,
                'date': date_str[:10],
                'source':'Reuters'
            })

            logger.info(f'Found {len(articles)} articles.')
            return articles
        
    except Exception as e:
        logger.error(f'Scraper error: {str(e)}')
        return []