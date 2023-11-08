import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from collections import deque
from html2image import Html2Image

# Function to get the base domain of a URL
def get_base_domain(url):
    try:
        return urlparse(url).netloc
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None

# Function to check if the URL is valid
def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

# Function to fetch URLs
def fetch_urls(url, depth=3):
    if depth == 0:
        return []
    try:
        response = requests.get(url, headers={'User-Agent': 'Custom Web Crawler'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [urljoin(url, tag.get('href')) for tag in soup.find_all('a', href=True)]
            return [link for link in links if is_valid_url(link)]
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    return []

# Function to crawl the website, staying within the starting domain
def crawl(url, depth):
    base_domain = get_base_domain(url)
    if not base_domain:
        return []

    visited = set()
    queue = deque([(url, depth)])
    hti = Html2Image()

    while queue:
        current_url, current_depth = queue.popleft()
        if current_url not in visited and get_base_domain(current_url) == base_domain:
            visited.add(current_url)
            print(f"Crawling: {current_url}")
            # Take a screenshot of the current URL
            try:
                hti.screenshot(url=current_url, save_as=f'{base_domain}_{len(visited)}.png')
            except Exception as e:
                print(f"Failed to take screenshot of {current_url}: {e}")
            for link in fetch_urls(current_url, current_depth):
                if current_depth > 1 and link not in visited and get_base_domain(link) == base_domain:
                    queue.append((link, current_depth - 1))

    return visited

# Main script
if __name__ == "__main__":
    starting_url = "https://docs.flipper.net"  # Replace with your starting URL
    crawl(starting_url, 3)
    print("Screenshots taken successfully.")
