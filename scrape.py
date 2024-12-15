from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler("scrape_website.log")
stream_handler = logging.StreamHandler()

# Create a formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def scrape_website(website):
    try:
        logger.info("Launching Chrome Browser...")
        AUTH = "brd-customer-hl_de461e3e-zone-ai_scraper:y9dtuug15kzt"
        SBR_WEBDRIVER = f"https://{AUTH}@brd.superproxy.io:9515"
        logger.info("Connecting to Scraping Browser...")
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
        options = ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        with Remote(sbr_connection, options=options) as driver:
            logger.info("Connected! Navigating...")
            driver.get(website)
            logger.info("Taking page screenshot to file page.png")
            driver.get_screenshot_as_file("./page.png")
            logger.info("Navigated! Scraping page content...")
            html = driver.page_source
            return html
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None


def extract_body_content(html_content):
    try:
        logger.info("Extracting body content...")
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        if body_content:
            return str(body_content)
        return ""
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return ""


def clean_body_content(body_content):
    try:
        logger.info("Cleaning body content...")
        soup = BeautifulSoup(body_content, "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )
        return cleaned_content
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return ""


def split_dom_content(dom_content, max_length=6000):
    try:
        logger.info("Splitting DOM content...")
        return [
            dom_content[i : i + max_length]
            for i in range(0, len(dom_content), max_length)
        ]
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []
