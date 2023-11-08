import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, urljoin
from collections import deque

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

# Function to initialize the Selenium WebDriver
def init_webdriver():
    options = Options()
    options.headless = True  # Run in headless mode
    service = Service(executable_path='./geckodriver.exe')
    driver = webdriver.Firefox(options=options,service=service)
    return driver

# Function to take a full-page screenshot with Selenium
def take_screenshot(driver, url, filename):
    driver.get(url)
    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    # Scroll to the bottom of the page to ensure all lazy-loaded elements are loaded
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for any lazy-loaded content
    # Take screenshot
    driver.get_full_page_screenshot_as_file(filename)

# Function to crawl the website, staying within the starting domain
def crawl(url, depth, output_directory):
    base_domain = get_base_domain(url)
    if not base_domain:
        return []

    visited = set()
    queue = deque([(url, depth)])
    driver = init_webdriver()

    try:
        while queue:
            current_url, current_depth = queue.popleft()
            if current_url not in visited and get_base_domain(current_url) == base_domain:
                visited.add(current_url)
                print(f"Crawling: {current_url}")
                # Take a screenshot of the current URL
                screenshot_filename = f"{base_domain}_{len(visited)}.png"
                screenshot_path = os.path.join(output_directory, screenshot_filename)
                take_screenshot(driver, current_url, screenshot_path)
                print(f"Screenshot saved as {screenshot_path}")
                # Fetch new URLs
                if current_depth > 1:
                    driver.get(current_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    links = [urljoin(current_url, tag.get('href')) for tag in soup.find_all('a', href=True)]
                    for link in links:
                        if is_valid_url(link) and link not in visited and get_base_domain(link) == base_domain:
                            queue.append((link, current_depth - 1))
    finally:
        driver.quit()

    return visited

# Main script
if __name__ == "__main__":
    starting_url = "https://docs.flipper.net"  # Replace with your starting URL
    output_dir = "./output"  # Output directory
    crawl(starting_url, 3, output_dir)
    print("Screenshots taken successfully.")
