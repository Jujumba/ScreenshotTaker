from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
from os import remove, getenv


class Parser:
    def __init__(self):
        self.__driver__ = None
        self.__options__ = None
        self.__deleted_header__ = False
        self.__images__ = []

    def get_screenshot(self, url: str, use_default_profile: bool = False, pop_ups: list[str] = None, by: By = By.XPATH, delete_header: bool = False):
        self.__options__ = webdriver.ChromeOptions()

        if use_default_profile:
            self.__options__.add_argument(rf"user-data-dir=C:\Users\{getenv('username')}\AppData\Local\Google\Chrome\User Data\Default")
            
        self.__driver__ = webdriver.Chrome(chrome_options=self.__options__)
        self.__driver__.get(url)
        self.__driver__.maximize_window()

        self.accept_pop_ups(pop_ups, by)

        self.scroll_and_save(delete_header)

    def accept_pop_ups(self, pop_ups, by):
        if pop_ups is None:
            return
        for pop_up in pop_ups:
            self.__driver__.find_element(by, pop_up).click()

    def scroll_and_save(self, delete_header):
        current = 0
        height = self.__driver__.execute_script('return document.body.clientHeight')
        step = self.__driver__.execute_script("return screen.height") - 160  # Magic number
        while current <= height:
            img_name = f"{str(current)}.png"
            self.__driver__.save_screenshot(img_name)
            self.__images__.append(cv2.imread(img_name))

            remove(img_name)
            self.__driver__.execute_script(f"window.scrollBy(0, {step})")

            if not self.__deleted_header__ and delete_header:  # Removing header
                self.__delete_header__()

            current += step
        self.__driver__.quit()
        im_v = cv2.vconcat(self.__images__)
        cv2.imwrite('python.org.png', im_v)

    def __delete_header__(self):
        self.__driver__.execute_script("const header = document.getElementsByTagName(\"header\")[0]; header.remove()")
        self.__deleted_header__ = True