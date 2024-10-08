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
import flet as ft
import os
import json


#the reason a class is used is because it is easier to manage the ids and classes of the elements
# these are elements which will be continuously used in the code and will tend to change a lot as google updates their website
# so it is better to keep them in a class so that they can be easily changed and also the variable naming won't interfere with the other variables
class all_ids:
    # create ids as class variables
    name = "DUwDvf lfPIob"
    wait_selector = 'h1[class="DUwDvf lfPIob"]'
    rating = "F7nice"
    review = "F7nice"
    _type = "DkEaL"
    address = "rogA2c"
    timing = "ZDu9vd"
    menu_dict = {"data-item-id": "menu"}
    website_dict = {"data-item-id": "authority"}
    location_plus_dict = {"data-tooltip": "Copy plus code"}
    location_plus_code = "rogA2c"
    phone_no_dict = {"data-tooltip": "Copy phone number"}
    phone_no_code = "rogA2c"
    reservation_dict = {"data-tooltip": "Open reservation link"}


def check_settings_file() -> None:
    # We will check if the file exists of not with default values, if it doesn't then we will save all
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
                "Reservation Link": True,
            },
        }
        with open("settings.json", "w") as f:
            json.dump(settings, f)


def create_browser_session(headless: bool) -> None:
    # Here we will create a browser session and return the page object
    # You can configure the browser settings here such as heigh and stuff
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=headless, args=["--start-maximized", "--window-size=1920,1080"]
    )
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    return page


def page_parser(link: str, image: str, html_content: str, variables: dict) -> None:
    # we will parse the page and return the data
    # Current Variables: Link, Image, name, Rating, Expensiveness, No of Reviews, Type, Address, Close Timing, Menu Link, website, Location Plus Code, Phone No, reservation Link

    # For the image, what we will do is that, we will fetch the image, and then the pre-assigned number will be used as image name
    # so it is linked with the entry as such.

    # Yeah the parsing code can be written in a better way, but for now this is fine
    soup = BeautifulSoup(html_content, "html.parser")
    data = {}
    for key, value in variables.items():
        if value:
            if key == "Link":
                if value == True:
                    data["Link"] = link
            if key == "Image":
                if value == True:
                    data["Image"] = image
            if key == "Name":
                if value == True:
                    # DUwDvf lfPIob
                    name = soup.find("h1", class_=all_ids.name).text
                    data["Name"] = name
            if key == "Rating":
                try:
                    if value == True:
                        rating = soup.find("span", class_=all_ids.rating).text
                        data["Rating"] = rating.split("(")[0]
                except:
                    data["Rating"] = ""
            if key == "Expensiveness":
                try:
                    if value == True:
                        spans = soup.find_all("span")
                        for span in spans:
                            if "aria-label" in span.attrs:
                                if "Price: " in span["aria-label"]:
                                    expensiveness = span.text
                        data["Expensiveness"] = expensiveness
                except:
                    data["Expensiveness"] = ""
            if key == "No of Reviews":
                try:
                    if value == True:
                        no_of_reviews = soup.find("div", class_=all_ids.rating).text
                        data["No of Reviews"] = (
                            no_of_reviews.split("(")[1]
                            .replace("(", "")
                            .replace(")", "")
                        )
                except:
                    data["No of Reviews"] = ""
            if key == "Type":
                try:
                    if value == True:
                        type_ = soup.find("button", class_=all_ids._type)
                        data["Type"] = type_.text
                except:
                    data["Type"] = ""
            if key == "Address":
                try:
                    if value == True:
                        address = soup.find("div", class_=all_ids.address).text
                        data["Address"] = address
                except:
                    data["Address"] = ""
            if key == "Timing":
                try:
                    if value == True:
                        timing = soup.find("span", class_=all_ids.timing)
                        data["Timing"] = timing.text
                except:
                    data["Timing"] = ""
            if key == "Menu Link":
                if value == True:
                    try:
                        menu_link = soup.find("a", all_ids.menu_dict)
                        data["Menu Link"] = menu_link["href"]
                    except:
                        data["Menu Link"] = ""
            if key == "Website":
                if value == True:
                    try:
                        website_tag = soup.find("a", all_ids.website_dict)
                        website = website_tag["href"]
                        data["Website"] = website
                    except:
                        data["Website"] = ""
            if key == "Location Plus Code":
                if value == True:
                    try:
                        location_plus_code = soup.find(
                            "button", all_ids.location_plus_dict
                        )
                        location_plus_code = location_plus_code.find("div", all_ids.location_plus_code)
                        data["Location Plus Code"] = location_plus_code.text
                    except:
                        data["Location Plus Code"] = ""
            if key == "Phone No":
                if value == True:
                    try:
                        phone_no = soup.find(
                            "button", all_ids.phone_no_dict
                        )
                        data["Phone No"] = phone_no.find("div", all_ids.phone_no_code).text
                    except:
                        data["Phone No"] = ""
            if key == "Reservation Link":
                if value == True:
                    try:
                        reservation_link = soup.find(
                            "a", all_ids.reservation_dict
                        )
                        data["Reservation Link"] = reservation_link["href"]
                    except:
                        data["Reservation Link"] = ""
    return data


# Main Function to start scraping, will connect it with the GUI later
def start_scraping(e):
    print("Scraping Started")
    check_settings_file()
    browser = create_browser_session(False)
    browser.goto(
        "https://www.google.com/maps/place/Size+Zero+Cafe/data=!4m7!3m6!1s0x395fc943e7491659:0x31673306a909fc88!8m2!3d22.3083244!4d73.1693718!16s%2Fg%2F11n0df00ky!19sChIJWRZJ50PJXzkRiPwJqQYzZzE?authuser=0&hl=en&rclk=1",
        wait_until="domcontentloaded",
    )
    browser.wait_for_selector(all_ids.wait_selector, timeout=10000)
    print(
        page_parser(
            browser.url,
            "458967",
            browser.content(),
            {
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
                "Reservation Link": True,
            },
        )
    )
    browser.close()


def split_list(l, n):
    # Basically will be used to split the zip codes into n parts which then will be passed to the processes
    k, m = divmod(len(l), n)
    return (l[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))


def gui_main(page: ft.Page):
    # GUI code (Man it takes too much time to write this)

    # Window Settings
    page.window.height = 585
    page.window.width = 905
    page.padding = 20
    page.window.max_height = 630
    page.window.max_width = 910
    page.title = "MapScraper Live"
    #page.window.maximizable = False
    #page.window.resizable = False  # window is not resizable
    page.bgcolor = "#292829"
    # Fonts
    page.fonts = {"Orbitron": "fonts/orbitron_font.ttf", "Chakra": "fonts/chakra.ttf"}
    # This is where start and stop button will be placed
    side_card = ft.Container(
        width=280,
        height=150,
        bgcolor="#292829",
        shadow=ft.BoxShadow(
            spread_radius=10,
            blur_radius=10,
            color="#000000",
            offset=(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER,
        ),
        content=ft.Column(
                spacing=0,
                controls=[
                    ft.Text("      Controller", size=32.5, color="#FFFFFF", font_family="Orbitron"),
                    ft.Divider(thickness=5),
                    ft.Divider(color="transparent"),
                    ft.Divider(color="transparent"),
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.Text(" ", size=10),
                            ft.FilledButton(
                                content= ft.Text("Start", size=30, color="#FFFFFF", font_family="Chakra"),
                                #bgcolor="#1E90FF",
                                style=ft.ButtonStyle(bgcolor="#1E90FF"),
                                width=130,
                                height=40,
                                on_click=start_scraping,
                            ),
                            ft.Text("  ", size=20),
                            ft.FilledButton(
                                content= ft.Text("Stop", size=30, color="#FFFFFF", font_family="Chakra"),
                                #bgcolor="#FF0000",
                                style=ft.ButtonStyle(bgcolor="#FF0000"),
                                width=130,
                                height=40,
                                on_click=start_scraping,
                            )
                        ]
                    )
                ]
            )
        )
    # Logo of the app (Made using ChatGPT 4)
    logo = ft.Image(src="images/logo.png", width=150, height=150)
    logo_card = ft.Container(
        width=500,
        height=240,
        bgcolor="#292829",
        padding=0,
        margin=0,
        content=ft.Container(
            ft.Row(
                spacing=0,
                vertical_alignment=ft.VerticalAlignment.START,
                controls=[
                    ft.Column(controls=[ft.Text(" ", size=3),logo]),
                    ft.Text("      ", size=10),
                    ft.Column(
                        controls=[
                            ft.Text("  ", size=3),
                            ft.Text(
                                "MapScraper\nLive",
                                size=50,
                                color="#FFFFFF",
                                font_family="Orbitron",
                            ),
                        ]
                    ),
                    ft.Text("    ", size=30),
                ],
            ),
        ),
    )
    # Controls Card, this is basically where all of the settings will be placed
    controls_card = ft.Container(
        width=810,
        height=250,
        bgcolor="#292829",
        shadow=ft.BoxShadow(
            spread_radius=10,
            blur_radius=10,
            color="#000000",
            offset=(0, 0),
            blur_style=ft.ShadowBlurStyle.OUTER
        ),
    )
    # Main Page Controls
    page.add(
        ft.Column(
            spacing=0,
            controls=[
                ft.Row(
                    controls=[
                        logo_card, 
                        ft.Text("       ", size=15),
                        side_card
                    ]
                ),
                ft.Row(controls=[ft.Text("    ", size=10), controls_card]),
            ],
        )
    )
    page.update()


# Main driver Code
if __name__ == "__main__":
    ft.app(target=gui_main, assets_dir="assets")

# Further Short Term Plans

# 1. Design MenuBar in the GUI and code it afterwards
# 2. Create A Home Page and Settings page as per the above mentioned format
# 3. Add the functionality to save the settings
# 4. Add the functionality to load the settings
# 5. Add the functionality to start the scraping
# 6. Add the functionality to stop the scraping