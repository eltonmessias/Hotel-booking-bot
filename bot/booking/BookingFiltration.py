# This file will include a class with instance methods
# That will be responsible to interact with our website
# After we have some results, to apply quickly
import time

from selenium.common import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        # wait = WebDriverWait(self.driver, 5)
        #
        # star_filtration_box = wait.until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-filters-group]"))
        # )
        #
        # star_child_elements = star_filtration_box.find_elements(
        #     By.CSS_SELECTOR, "div[data-filters-item='class:class']"
        # )
        #
        # for star_element in star_child_elements:
        #     try:
        #         text = star_element.text.strip()
        #         if text.startswith(str(star_value)):
        #             print(f"Clicking on {text} filter")
        #             star_filtration_box.click()
        #
        #             wait.until(EC.staleness_of(star_element))
        #             return
        #     except StaleElementReferenceException:
        #         # Se o DOM recarregou durante o loop, reobtém os elementos
        #         star_child_elements = star_filtration_box.find_elements(
        #             By.CSS_SELECTOR, "div[data-filters-item='class:class']"
        #         )
        #
        #     time.sleep(5)
        star_filtration_box = self.driver.find_element("css selector", "div[data-filters-group=class]")
        star_child_elements = star_filtration_box.find_elements("css selector", "*")
        print(len(star_child_elements))


        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f"{star_value} stars":
                    star_element.click()



    def sort_price_lowest_first(self):
        expand_list = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='sorters-dropdown-trigger']")
        expand_list.click()

        select_lowest_price = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Price (lowest first)']")
        select_lowest_price.click()
        time.sleep(6)
