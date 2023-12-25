import scrapy
from selenium import webdriver
from time import sleep
from parsel import Selector
from selenium.webdriver.chrome.options import Options
import pandas as pd


def store_in_database(data):
    df = pd.DataFrame(data=data, columns={"url"})
    df.to_csv("database.csv")


class Nevadaepro2Spider(scrapy.Spider):
    name = 'nevadaepro_2'

    def start_requests(self):
        shared_space = []
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(
            "chromedriver.exe",
            options=chrome_options
        )
        # C:\\Users\\shubhan.patange\\Desktop\\chromedriver_win32\\chromedriver_win32\\

        driver.get("https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true")
        sleep(5)
        sel = Selector(text=driver.page_source)
        disable = sel.xpath("//span[@class='ui-paginator-next ui-state-default ui-corner-all ui-state-disabled']").get()
        data = []
        loop = 0
        while loop < 2:
            common = sel.xpath("//div[@class='ui-datatable-tablewrapper']//tbody//tr[@role='row']")
            for i in common:
                Bid_Solitication_number = i.xpath(".//td[1]/a/text()").get()
                Bid_Solitication_url = "https://nevadaepro.com" + i.xpath(".//td[1]/a/@href").get()
                Bid_Buyer = i.xpath(".//td[6]/text()").get()
                Bid_Description = i.xpath(".//td[7]/text()").get()
                Bid_Opening_Date = i.xpath(".//td[8]/text()").get()
                data.append({
                    "Bid Solicitation #": Bid_Solitication_number,
                    "Bid Solicitation url": Bid_Solitication_url,
                    "Buyer": Bid_Buyer,
                    "Description": Bid_Description,
                    "Bid Opening Date": Bid_Opening_Date,
                })
            next_page = driver.find_element_by_xpath("//span[contains(@class,'ui-paginator-next')]")
            next_page.click()
            sleep(5)
            sel = Selector(text=driver.page_source)
            disable = sel.xpath("//span[@class='ui-paginator-next ui-state-default ui-corner-all ui-state-disabled']").get()
            if disable is not None:
                loop = loop +1
        print(len(data))
        for i in data:
            shared_space.append(i['Bid Solicitation url'])
            yield scrapy.Request(
                url=i['Bid Solicitation url'],
                callback= self.parse,
                meta=i
            )
        print("shared_space" + str(shared_space))
        store_in_database(shared_space)


    def parse(self, response):
        Bid_number = response.xpath(
            "//td[contains(text(),'Bid Number:')]/following-sibling::td[1]/text()").get().strip()
        Purchaser = response.xpath("//td[contains(text(),'Purchaser:')]/following-sibling::td[1]/text()").get().strip()
        Department = response.xpath(
            "//td[contains(text(),'Department:')]/following-sibling::td[1]/text()").get().strip()
        fiscal_year = response.xpath(
            "//td[contains(text(),'Fiscal Year:')]/following-sibling::td[1]/text()").get().strip()
        alternate_id = response.xpath(
            "//td[contains(text(),'Alternate Id:')]/following-sibling::td[1]/text()").get().strip()
        info_contact = response.xpath(
            "//td[contains(text(),'Info Contact:')]/following-sibling::td[1]/text()").get().strip()
        Purchase_Method = response.xpath(
            "//td[contains(text(),'Purchase Method:')]/following-sibling::td[1]/text()").get().strip()
        Description = response.xpath(
            "//td[contains(text(),'Description:')]/following-sibling::td[1]/text()").get().strip()
        Organization = response.xpath(
            "//td[contains(text(),'Organization:')]/following-sibling::td[1]/text()").get().strip()
        Location = response.xpath(
            "//td[contains(text(),'Location:')]/following-sibling::td[1]/text()").get().strip()
        Type_Code = response.xpath(
            "//td[contains(text(),'Type Code:')]/following-sibling::td[1]/text()").get().strip()
        Required_Date = response.xpath(
            "//td[contains(text(),'Required Date:')]/following-sibling::td[1]/text()").get().strip()
        Bid_Type = response.xpath(
            "//td[contains(text(),'Bid Type:')]/following-sibling::td[1]/text()").get().strip()
        opening_date = response.xpath(
            "//td[contains(text(),'Bid Opening Date:')]/following-sibling::td[1]/text()").get().strip()
        Allow_Electronic_Quote = response.xpath(
            "//td[contains(text(),'Allow Electronic Quote:')]/following-sibling::td[1]/text()").get().strip()
        Available_Date = response.xpath(
            "//td[contains(text(),'Available Date')]/following-sibling::td[1]/text()").get().strip()
        Informal_Bid_Flag = response.xpath(
            "//td[contains(text(),'Informal Bid Flag:')]/following-sibling::td[1]/text()").get().strip()
        Pre_Bid_Conference = response.xpath(
            "//td[contains(text(),'Pre Bid Conference:')]/following-sibling::td[1]/text()").get().strip()
        Bulletin_Desc = response.xpath(
            "//td[contains(text(),'Bulletin Desc:')]/following-sibling::td[1]/text()").get().strip()
        Ship_to = ""
        Bill_to = ""
        for i in response.xpath("//td[contains(text(),'Ship-to Address:')]/following-sibling::td[1]/text()").extract():
            Ship_to = Ship_to + "" + i.strip()
        for i in response.xpath("//td[contains(text(),'Bill-to Address:')]/following-sibling::td[1]/text()").extract():
            Bill_to = Bill_to + " " + i.strip()

        Bid_Solitication_number = response.meta['Bid Solicitation #']
        Bid_Buyer = response.meta['Buyer']
        Bid_Description = response.meta['Description']
        Bid_Opening_Date = response.meta['Bid Opening Date']
        yield {
            "header_information": {
                "Bid Number": Bid_number,
                "Purchaser": Purchaser,
                "Department": Department,
                "fiscal_year": fiscal_year,
                "Alternate Id:": alternate_id,
                "info_conctact": info_contact,
                "Purchase Method": Purchase_Method,
                "Description:": Description,
                "Organization": Organization,
                "Location": Location,
                "Type Code": Type_Code,
                "Required Date": Required_Date,
                "Bid Type": Bid_Type,
                "Bid Opening Date": opening_date,
                "Allow Electronic Quote": Allow_Electronic_Quote,
                "Available Date": Available_Date,
                "Informal Bid Flag": Informal_Bid_Flag,
                "Pre Bid Conference": Pre_Bid_Conference,
                "Bulletin Desc": Bulletin_Desc,
                "Ship-to Address": Ship_to,
                "Bill-to Address": Bill_to,

            },
            "Bid Solicitation #": Bid_Solitication_number,
            "Buyer": Bid_Buyer,
            "Description": Bid_Description,
            "Bid Opening Date": Bid_Opening_Date,
        }
