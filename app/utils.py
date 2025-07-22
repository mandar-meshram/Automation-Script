import time
import logging
import os
from contextlib import contextmanager

BASE_URL = 'https://www.reuters.com/business/finance/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/'
}

DELAY = 2

logger = logging.getLogger("reuters_scraper")
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def save_debug_html(request, filename="debug_reuters.html"):
    os.makedirs("debug_pages", exist_ok=True)
    path = os.path.join("debug_pages", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(request.text)
    logger.debug(f"Saved page HTML to {path}")

@contextmanager
def timed(name="Operation"):
    start = time.time()
    yield
    end = time.time()
    logger.info(f"{name} took {end - start:.2f}s")