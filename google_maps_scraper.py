# Author: Saksham Solanki
# Timestamp: 2024-08-01 5:00 PM
# Format - Page: Parameter: Description: Type: To Be Stored
# 1. Main: Keyword: Main keyword to search for: InputBox: No
# 2. Main: zip codes: User can give a file containing zip codes where each line is a zip code: FilePicker: No
# 3. Main: country: we will ask for the country to be included so that maps doesn't get confused with the number: InputBox: No
# 4. Main: output file name: the name of the file where the data will be stored: InputBox: Yes
# 5. Settings: output file format: json or csv: Slider: Yes
# 6. Settings: No. of Pages: number of pages to scrape, if user wants they can put a limit, by default it will be None: InputBox: Yes
# 7. Settings: Chrome Instances: number of chrome instances to run: InputBox: Yes
# 8. Settings: Strict matching: don't scrape entry until it matches the keyword, for ex, if keyword->Cafe, don't scrape restaurent, only cafe: Checkbox: Yes
# 9. Main: Variables: Link, Image, name, Rating, Expensiveness, No of Reviews, Type, Address, Close Timing, Menu Link, website, Location Plus Code, Phone No, reservation Link: Chip: Yes
# 10. Settings: Timeout: Timeout for each page: InputBox: Yes
# 11. Settings: Headless: Run in headless mode: Checkbox: Yes

from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import multiprocessing
import flet
import os
import json


def check_settings_file() -> None:
    # We will check ifthe file exists of not with default values, if it doesn't then we will save all 
    # those in a file so that user settings can also be saved for future use
    if os.path.exists("settings.json"):
        pass
    else:
        settings = {
            "output_filename": "output",
            "output_file_format": "csv",
            "no_of_pages": None,
            "chrome_instances": 1,
            "strict_matching": False,
            "timeout": 15,
            "headless": True,
            "Variables": {
                "Link": True,
                "Image": True,
                "Name": True,
                "Rating": True,
                "Expensiveness": True,
                "No of Reviews": True,
                "Type": True,
                "Address": True,
                "Close Timing": True,
                "Menu Link": True,
                "Website": True,
                "Location Plus Code": True,
                "Phone No": True,
                "Reservation Link": True
            }
        }
    with open("settings.json", "w") as f:
        json.dump(settings, f)



def create_browser_session():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    return page


def scrape_all_details() -> None:
    pass


if __name__ == "__main__":
    check_settings_file()
    browser = create_browser_session()
