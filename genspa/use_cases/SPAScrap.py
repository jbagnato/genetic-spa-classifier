import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, \
    ElementClickInterceptedException, WebDriverException


class SPAScrap:

    def __init__(self):
        self.url = 'https://www.marieclaire.com/fashion/g1898/best-online-shopping/'

    def domain_name(self, url):
        return url.split("www.")[-1].split("//")[-1].split(".")[0]

    def scrap_urls(self):
        self.reqs = requests.get(self.url)
        self.soup = BeautifulSoup(self.reqs.text, 'html.parser')
        urls = []
        for link in self.soup.find_all('a'):
            aUrl = link.get('href')

            # avoid banners or repeated urls
            banner_words = ['booksare','anthro','cocoand','fashionphile','movitaorg','therealreal','bouqs','wayfair','urbanout','everlane','marieclaire','utm','fave','future','stories','rebecca','asos','anthr','horcho','totoka','shop','westel','freepeople','adidas']

            res = any(ele in aUrl for ele in banner_words)
            if not res and len(aUrl)>1:
                print(aUrl)
                urls.append(aUrl)

        print(f"Founded {len(urls)} urls")
        return urls

    def captureWebsiteSceen(self, webs_to_visit=[], delay=0.7, directory="./screenshots"):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")  # pass headless argument to the options
        #options.binary_location = '/Users/jbagnato/chromedriver'  # location of the Chrome Browser binary
        options.add_argument("disable-infobars")  # disabling infobars
        options.add_argument("--disable-extensions")  # disabling extensions
        #options.add_argument("--disable-gpu")  # applicable to windows os only
        options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
        options.add_argument("--no-sandbox")  # Bypass OS security model
        driver = webdriver.Chrome(executable_path='/Users/jbagnato/chromedriver', chrome_options=options)
        #driver = webdriver.Safari(quiet=True)
        width = 1024
        height = width*4
        driver.set_window_size(width, height)

        for i, web in enumerate(webs_to_visit):
            try:
                print(f"{i} Getting Screnshot from: {web}")
                """driver.add_cookie(
                    {'_y': '5dcace16-d4e9-4e00-9729-47e2bdeb843c', '_s': 'dacf316b-1b51-4668-a6ff-fd7684656e44',
                     '_shopify_y': '5dcace16-d4e9-4e00-9729-47e2bdeb843c',
                     '_shopify_s': 'dacf316b-1b51-4668-a6ff-fd7684656e44',
                     '_ju_dm': 'cookie', '_ju_dn': 1})
                """
                driver.get(web)
                #el = driver.find_element_by_tag_name('body')
                sleep(delay)
                # AVOID cookies
                self.avoid_cookies(driver)
                self.avoid_subscription(driver)

                #and twice.. because some sites have up to 3 popups!
                sleep(0.1)
                self.avoid_subscription(driver)

                driver.get_screenshot_as_file(f"{directory}/{self.domain_name(web)}.png")
            except (TimeoutException, WebDriverException):
                print("Cant do screenshot of " + web)

        driver.quit()

        print("end...")

    def avoid_cookies(self, driver):
        toclick = ['*[@id="uc-btn-accept-banner"]', 'button[class="wt-mb-xs-0"]','a[@id="AVyes"]']
        for aclick in toclick:
            try:
                #WebDriverWait(driver, 1).until(expected_conditions.visibility_of_element_located((By.XPATH, f"//{aclick}")))
                cookie_button = driver.find_element_by_xpath(f"//{aclick}")
                cookie_button.click()
                sleep(0.1)
                return
            except (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException):
                pass

        texts = ['Accept','Accept Cookies','Accept All','Accept All Cookies', 'Aceptar todo','Autoriser tous les cookies','Aceptar','Got it']
        for btn_text in texts:
            try:
                #WebDriverWait(driver, 1).until(expected_conditions.visibility_of_element_located((By.XPATH, f"//button[text()='{btn_text}']")))
                cookie_button = driver.find_element_by_xpath(f"//button[text()='{btn_text}']")
                cookie_button.click()
                sleep(0.1)
                return
            except (NoSuchElementException, ElementNotInteractableException,ElementClickInterceptedException):
                pass

    def avoid_subscription(self, driver):
        toclick = ['*[@id="ltkpopup"]', 'circle', 'li[class="us-site"]','button[text()="Update location"]',
                 'button[text()="Aceptar"]','a[text()="NO THANKS"]','input[text()="Acceder a la tienda"]',
                   "div[contains(@class, 'needsclick')]",'input[value="GET TO SHOPPING"]',
                   'input[value="Acceder a la tienda"]','input[value="COMPRA AHORA"]','button[text()="Confirm"]',
                   '*[@data-test-id="om-overlays-close"]','button[text()="CONFIRM SELECTION"]','a[text()="YOU BET!"]']
        for aclick in toclick:
            try:
                #WebDriverWait(driver, 1).until(expected_conditions.visibility_of_element_located((By.XPATH, f"//{aclick}")))
                cookie_button = driver.find_element_by_xpath(f"//{aclick}")
                cookie_button.click()
                sleep(0.1)
                return
            except (NoSuchElementException, ElementNotInteractableException,ElementClickInterceptedException):
                pass
        #area to delete
        texts = ['div[role="dialog"]', "div[contains(@class, 'needsclick')]", 'div[class="needsclick"', '*[@id="ltkpopup-overlay"]',
                 '*[@id="_hjRemoteVarsFrame"]', '*[@id="wt-modal-container"]','div[@id="tc_privacy"]','*[@id="shopify-section-geo-location"]',
                 'iframe']
        for text in texts:
            try:
                aDiv = driver.find_element_by_xpath(f"//{text}]")
                #element = driver.find_element_by_id("some_id")
                driver.execute_script("arguments[0].innerText = ''", aDiv)
                sleep(0.1)
                return
            except (NoSuchElementException, ElementNotInteractableException,ElementClickInterceptedException):
                pass
