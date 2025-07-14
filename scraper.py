import requests                   # imports the request library to handle HTTP requests
from bs4 import BeautifulSoup     # imports BeautifulSoup for parsing and navigating HTML content
from textblob import TextBlob     # imports TEXTBLOB for performing sentiment analysis on text
import pandas as pd               # imports pandas for data manupulation and saving the results to csv
import time                       # imports the time module 
from datetime import datetime     # imports datetime to handle and format date/time values

# Configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}                                 # sets up HTTP request headers to mimic a real browser (helps avoid blocking)
BASE_URL = 'https://www.reuters.com/business/finance/'      # sets the base URL for the Reuters finance news section
DELAY = 2  # Delay between requests

def debug_page(response):            # defines a function to save the HTML of the fetched page for troubleshooting
    """Save page HTML for debugging"""
    with open('debug_reuters.html', 'w', encoding='utf-8') as f:       # opens a file to write the HTML content
        f.write(response.text)                           # writes the response content to the file
    print("ℹ️ Saved page HTML to debug_reuters.html")        # prints a message confirming the file was saved

def fetch_news(url):                         # defines the main functon to scrape news articles from Reuters
    """Scrape news from Reuters with updated selectors"""
    try:
        print(f"📡 Fetching: {url}")           # logs the URL being fetched
        response = requests.get(url, headers=HEADERS, timeout=10)       # sends a GET request to the URL with headers and a 10-second timeout
        response.raise_for_status()           # raises an error if the response status is not 200 (OK)
        
        # Debug: Save HTML if no articles found
        debug_page(response)
        
        soup = BeautifulSoup(response.text, 'html.parser')         # parses the HTML with BeautifulSoup
        articles = []              # initializes an empty list to store article data
        
        # Current Reuters selectors (June 2024)
        for article in soup.select('div.story-card'):            # loops through each news article card found by the selector
            try:
                # Updated headline selector
                headline_elem = article.select_one('a[data-testid="Heading"]')     # finds the headline link within the article card
                if not headline_elem:               # skips if no headline link is found
                    continue
                
                headline = headline_elem.text.strip()          # extracts and trims the haedline text
                link = "https://www.reuters.com" + headline_elem['href']         # constructs the full article URL
                
                # Updated date selector
                time_elem = article.select_one('time')         # tries to find the time element for the article  
                date_str = time_elem['datetime'] if time_elem else str(datetime.now().date())      # gets the article's data or uses the current date if not found
                
                articles.append({
                    'headline': headline,
                    'link': link,
                    'date': date_str[:10],
                    'source': 'Reuters'
                })                           # adds the article's date or uses the current date if not found
                time.sleep(DELAY)           # waits for the specified delay before the next request
                
            except Exception as e:            # skips the article if any error occurs
                print(f"⚠️ Skipping article: {str(e)}")    # logs the number of articles found 
                continue
                
        print(f"✅ Found {len(articles)} articles")         # return the list of articles
        return articles
        
    except Exception as e:          # handles errors during the entire fetch operation
        print(f"❌ Scraping failed: {str(e)}")
        return []

def analyze_sentiment(text):                # defines a function to analyze the sentiment of a news headline
    """Enhanced sentiment analysis for financial news"""
    try:
        analysis = TextBlob(text)            # create a TextBlob object for the given text
        polarity = analysis.sentiment.polarity             # gets the polarity score of the text (-1 to 1)
        
        # Financial-specific thresholds
        if polarity > 0.2:
            return 'Bullish'
        elif polarity < -0.2:
            return 'Bearish'
        elif 'rise' in text.lower() or 'gain' in text.lower():
            return 'Positive'
        elif 'fall' in text.lower() or 'drop' in text.lower():
            return 'Negative'
        return 'Neutral'
    except:
        return 'Neutral'

def scrape_and_analyze():                    # main function to orchestrate the scraping and analysis process
    """Main scraping workflow"""
    news_data = fetch_news(BASE_URL)          # fetch news articles from Reuters finance section
    
    if not news_data:                    # checks if no articles were found
        print("\n🔴 Troubleshooting Guide:")
        print("1. Open debug_reuters.html in browser")
        print("2. Right-click → Inspect to verify current HTML structure")
        print("3. Check if you're being blocked (CAPTCHA)")
        print("4. Try changing User-Agent or using Selenium")
        return
    
    # Analyze sentiment
    for article in news_data:             # loops through each article to analyze its sentiment
        article['sentiment'] = analyze_sentiment(article['headline'])              # adds a sentiment field to the article data
    
    # Save results
    df = pd.DataFrame(news_data)               # converts the list of articles into a pandas DataFrame
    try:
        df.to_csv('reuters_finance_news.csv', index=False)
        print(f"\n💾 Saved {len(df)} articles to reuters_finance_news.csv")
        print("Sample headlines:")
        for i, row in df.head().iterrows():
            print(f"{i+1}. {row['headline']} ({row['sentiment']})")
    except Exception as e:
        print(f"❌ Failed to save CSV: {str(e)}")

if __name__ == "__main__":
    scrape_and_analyze()