# This file is going to include methods that will parse
# the specific data that we need from each one of the deals
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BookingReport:
    def __init__(self, boxes_section_element:WebDriver):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR, 'div[data-testid="property-card"]'
        )

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            #pulling the hotel name
            hotel_name = deal_box.find_element(
                By.CSS_SELECTOR, 'div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()
            #pulling the price
            hotel_price = deal_box.find_element(
                By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]'
            ).get_attribute('innerHTML').strip()


            collection.append(
                [hotel_name, hotel_price]
            )
        return collection