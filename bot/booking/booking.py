import time

from selenium import webdriver
import os
import booking.constants as const
from booking.BookingFiltration import BookingFiltration
from booking.booking_report import BookingReport
from prettytable import PrettyTable


class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/SeleniumDrivers", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency=None):
        currency_element = self.find_element(
            "css selector",
            "button[data-testid='header-currency-picker-trigger']")
        currency_element.click()
        selected_currency_element = self.find_element(
            "xpath",
            f"//button[@data-testid='selection-item']//div[text()='{currency}']")
        selected_currency_element.click()



    def select_place_to_go(self, place_to_go):
        search_field = self.find_element("name", "ss")
        search_field.clear()
        search_field.send_keys(place_to_go)


        first_result = self.find_element("css selector", "li[id=autocomplete-result-0]")
        first_result.click()


    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.find_element(
            "css selector",
            f"span[data-date='{check_in_date}']")
        check_in_element.click()

        check_out_element = self.find_element(
            "css selector",
            f"span[data-date='{check_out_date}']"
        )
        check_out_element.click()


    def select_adults(self, count=1):
        selection_element = self.find_element("css selector", "button[data-testid='occupancy-config']")
        selection_element.click()


        while True:
            decrease_adults_element = self.find_element(
                "class name",
                "c857f39cb2"
            )
            decrease_adults_element.click()

            adults_value_element = self.find_element("id", "group_adults")
            adults_value = adults_value_element.get_attribute('value') # Should give back the adults

            if int(adults_value) == 1:
                break

        increase_button_element = self.find_element("class name", "dc8366caa6")
        for _ in range(count - 1):
            increase_button_element.click()


    def click_search(self):
        search_button = self.find_element("css selector", "button[type=submit]")
        search_button.click()

        time.sleep(2)

    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(3,4,5)
        filtration.sort_price_lowest_first()

    def report_results(self):
        hotel_boxes = self.find_element("class name", "cca574b93c")

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        rows = report.pull_deal_box_attributes()
        table.add_rows(rows)
        # table.add_rows(report.pull_deal_box_attributes())
        print(table)
        # print(report.pull_deal_box_attributes())

