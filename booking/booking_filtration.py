#This file will include a class with instance methods.
#They will be responsible to interact with our website
#after we have generated results, and would like to filter through them.
from _ast import Continue

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver


    def star_rating(self, *star_values):
        star_box = self.driver.find_element(
            By.XPATH, "//*[contains(@id, 'filter_group_class_')]"
        )
        star_box_children = star_box.find_elements(
            By.CSS_SELECTOR, '*'
        )

        for star_value in star_values:
            for star_child in star_box_children:
                if str(star_child.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_child.click()

    def amenities(self, amenity_1, amenity_2):
        amenities_box = self.driver.find_element(
            By.XPATH, "//*[contains(@id, 'filter_group_hotelfacility_')]"
        )
        amenities_children = amenities_box.find_elements(
            By.CSS_SELECTOR, '*'
        )

        for amen_child in amenities_children:
            if str(amen_child.get_attribute('innerHTML')).strip() == f'{amenity_1}':
                amen_child.click()
            if str(amen_child.get_attribute('innerHTML')).strip() == f'{amenity_2}':
                amen_child.click()


    def trip_budget(self, budget_amount):
        try:
            WebDriverWait(self.driver, timeout=20).until(
                EC.presence_of_element_located(
                    (By.ID, 'filter_group_pri_:Rcq:')
                )
            )
        except StaleElementReferenceException:
            Continue


        budget_box = self.driver.find_element(
            By.ID, 'filter_group_pri_:Rcq:'
        )
        budget_prices = budget_box.find_elements(
            By.CSS_SELECTOR, '*'
        )

        for price in budget_prices:
            if str(price.get_attribute('innerHTML')).strip() == f'{budget_amount}':
                price.click()
