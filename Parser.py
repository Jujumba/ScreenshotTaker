from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
from os import remove, getenv


class Parser:
    def __init__(self):
        self.driver = None
        self.options = None
        self.__deleted_header__ = False

    def get_screenshot(self, url: str, use_default_profile: bool = False, pop_ups: list[str] = None, by: By = By.XPATH):
        self.options = webdriver.ChromeOptions()

        if use_default_profile:
            self.options.add_argument(rf"user-data-dir=C:\Users\{getenv('username')}\AppData\Local\Google\Chrome\User Data\Default")
            
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.get(url)
        self.driver.maximize_window()

        self.accept_pop_ups(pop_ups, by)

        self.scroll_and_save()

    def accept_pop_ups(self, pop_ups, by):
        if pop_ups is None:
            return
        for pop_up in pop_ups:
            self.driver.find_element(by, pop_up).click()

    def scroll_and_save(self):
        current = 0
        height = self.driver.execute_script('return document.body.clientHeight')
        step = self.driver.execute_script("return screen.height") - 160  # Magic number
        images = []
        while current <= height:
            img_name = f"{str(current)}.png"
            self.driver.save_screenshot(img_name)
            images.append(cv2.imread(img_name))

            remove(img_name)
            self.driver.execute_script(f"window.scrollBy(0, {step})")

            if not self.__deleted_header__:  # Removing header
                self.__delete_header__()

            current += step
        self.driver.quit()
        im_v = cv2.vconcat(images)
        cv2.imwrite('python.org.png', im_v)

    def __delete_header__(self):
        self.driver.execute_script("const header = document.getElementsByTagName(\"header\")[0]; header.remove()")
        self.__deleted_header__ = True