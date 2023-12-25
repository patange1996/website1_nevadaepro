import scrapy
from selenium import webdriver
from time import sleep
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import os


def retrieve_from_database():
    df = pd.read_csv("database.csv")
    start_urls = []
    for i in df['url']:
        start_urls.append(i)
    return start_urls

class NevadaeproDownloadFilesSpider(scrapy.Spider):
    name = 'nevadaepro_download_files'

    def start_requests(self):
        start_url = retrieve_from_database()
        download_directory = os.getcwd() + "\\downloaded_files"
        for url in start_url:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_experimental_option('prefs', {
                'download.default_directory': download_directory,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': False
            })
            driver = webdriver.Chrome(
                os.getcwd() + "\\chromedriver.exe",
                options=chrome_options,
                chrome_options=chrome_options,
            )
            # C:\\Users\\shubhan.patange\\Desktop\\chromedriver_win32\\chromedriver_win32\\

            driver.get(url)
            sleep(3)
            try:
                loop = len(driver.find_element_by_xpath(
                    "//td[contains(text(),'File Attachments')]/following-sibling::td").text.strip().split("\n"))
                #click and download
                for i in range(1, loop + 1):
                    button = driver.find_element_by_xpath(
                        f'//td[contains(text(),"File Attachments")]/following-sibling::td[1]/a[{i}]')
                    action = ActionChains(driver)
                    action.move_to_element(button) \
                        .click() \
                        .perform()
                    sleep(3)
                print(driver.current_url + " has " + str(loop) + " attachments")
                driver.close()
            except Exception:
                print(driver.current_url + "has no attachments")
                driver.close()
        driver.quit()


    def parse(self, response):
        pass
