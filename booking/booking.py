import booking.constants as const
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from _ast import Continue
from selenium.common.exceptions import StaleElementReferenceException
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"/users/armanvakili/SeleniumDrivers/chromedriver", teardown=True):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += os.pathsep + os.path.dirname(self.driver_path)
        super(Booking, self).__init__(self.driver_path)
        self.implicitly_wait(20)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)
        try:
            close_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Dismiss sign-in info."]')
            close_button.click()
        except:
            print('No element with this class name. Skipping...')

        print('Landed on the first page...')
        print('Changing Currency to Desired Currency')

    def change_currency(self, currency=None):
        currency_element = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_element.click()

        WebDriverWait(driver=self, timeout=20).until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, 'div[data-testid="selection-modal"]') , f'{currency}'
            )
        )

        desired_currency_box = self.find_element(
            By.CSS_SELECTOR, 'div[data-testid="selection-modal"]'
        )

        desired_currency_children = desired_currency_box.find_elements(
            By.CSS_SELECTOR, '*'
        )

        for desired_currency in desired_currency_children:
            try:
                if str(desired_currency.get_attribute('innerHTML')).strip() == f'{currency}':
                    desired_currency.click()
            except StaleElementReferenceException:
                Continue

        print(f'Desired currency changed to {currency}')

        print('Choosing Place to Go...')

    def select_place_to_go(self, place_to_go):
        WebDriverWait(driver=self, timeout=20).until(
            EC.element_to_be_clickable(
                (By.ID, ':Ra9:')
            )
        )

        search_field = self.find_element(By.ID, ":Ra9:")
        search_field.clear()
        search_field.send_keys(place_to_go)

        try:
            WebDriverWait(driver=self, timeout=30).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'ul[data-testid="autocomplete-results"]')
                )
            )

            location_elements = self.find_elements(
                By.CLASS_NAME, 'a40619bfbe'
            )

            for location in location_elements:
                if str(location.get_attribute('innerHTML')).strip() == f'{place_to_go}':
                    location.click()
                else:
                     Continue
        except TimeoutError as ex:
            print(f'Timed out waiting for location {place_to_go} to apear.')
            raise ex

        except StaleElementReferenceException as ex:
            raise ex


        print(f'{place_to_go} chosen as Place to Go')

        print('Selecting Dates for Trip...')



    def select_date(self, check_in_date, check_out_date):
        check_in_area = self.find_element(
            By.CSS_SELECTOR, 'button[data-testid="date-display-field-start"]'
        )
        check_in_area.click()

        check_in_element = self.find_element(
            By.CSS_SELECTOR, f'span[aria-label="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.find_element(
            By.CSS_SELECTOR, f'span[aria-label="{check_out_date}"]'
        )
        check_out_element.click()
        print(f'Check in Date is set to {check_in_date}... Check Out date is set to{check_out_date}')

        print('Travel dates have been selected')
        print('Selecting number of travelers...')

    def select_travelers(self, count=1):
        drop_down = self.find_element(
            By.CSS_SELECTOR, 'span[data-testid="searchbox-form-button-icon"]'
        )
        drop_down.click()

        while True:

            decrease_adult_count = self.find_element(
                By.CSS_SELECTOR, 'button[class="fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 cd7aa7c891"]'
            )
            decrease_adult_count.click()
            adult_count_element = self.find_element(
                By.ID, 'group_adults'
            )
            adults = adult_count_element.get_attribute('value')

            if int(adults) == 1:
                break

        increase_adult_count = self.find_element(
            By.XPATH, '//*[@id="indexsearch"]/div[2]/div/div/form/div[1]/div[3]/div/div/div/div/div[1]/div[2]/button[2]'
        )

        for _ in range(count - 1):
            increase_adult_count.click()
        print(f'Number of travelers set to {count}')

        print('Trip parameters are set... Searching...')

    def click_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR, 'button[type="submit"]'
        )
        search_button.click()

        print('Results have been generated... Applying Filters...')

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.star_rating(4, 5)

    def report_results(self):
        hotel_boxes = self.find_element(
                By.ID, 'search_results_table'
            )
        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price"]
        )
        table.add_rows(report.pull_deal_box_attributes())
        print(table)

    def close_driver(self):
        self.teardown = True
        self.__exit__(None, None, None)
