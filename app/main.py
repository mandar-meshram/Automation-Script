from fastapi import FastAPI, Request, Form 
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates 
from fastapi.staticfiles import StaticFiles 

import pandas as pd

from .scraper import fetch_news
from .sentiment import analyze_sentiment
from .utils import logger

app =FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get('/', response_class=HTMLResponse)
def load_form(request: Request):
    return templates.TemplateResponse("index.html",{'request' : request})

@app.post('/scrape', response_class=HTMLResponse)
def scrape_from_url(request: Request, url: str = Form(...)):
    logger.info(f'[User Submitted] Scraping: {url}')
    articles = fetch_news(url)

    if not articles:
        return templates.TemplateResponse("results.html",{
            'request': request,
            'error': 'No articles found for the provided URL.'
        })
    
    for article in articles:
        article['sentiment'] = analyze_sentiment(article['headline'])

    return templates.TemplateResponse("results.html",{
        'request': request,
        'articles': articles,
        'message': f'Successfully scraped {len(articles)} headlines.'
    })

@app.get('/health')
def health_check():
    return {'status':'ok'}
