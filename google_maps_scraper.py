# Author: Saksham Solanki
# Timestamp: 2024-08-01 5:00 PM
# Format - Page: Parameter: Description: Type
# 1. Main: Keyword: Main keyword to search for : InputBox
# 2. Main: zip codes: User can give a file containing zip codes where each line is a zip code: FilePicker
# 3. Main: country: we will ask for the country to be included so that maps doesn't get confused with the number: InputBox
# 4. Main: output file name: the name of the file where the data will be stored: InputBox
# 5. Settings: output file format: json or csv: Slider
# 6. Settings: No. of Pages: number of pages to scrape, if user wants they can put a limit, by default it will be None: InputBox
# 7. Settings: Chrome Instances: number of chrome instances to run: InputBox
# 8. Settings: Strict matching: don't scrape entry until it matches the keyword, for ex, if keyword->Cafe, don't scrape restaurent, only cafe: Checkbox
# 9. Main: Variables: Image, name, Rating, Expensiveness, No of Reviews, Type, Address, Close Timing, Menu Link, website, Location Plus Code, Phone No, reservation Link: Chip
# 10. Settings: Timeout: Timeout for each page: InputBox
# 11. Settings: Headless: Run in headless mode: Checkbox

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import multiprocessing
import flet


def create_browser_session():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    return page


def scrape_all_details() -> None:
    pass


if __name__ == "__main__":
    create_browser_session()
    scrape_all_details()