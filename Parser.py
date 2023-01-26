from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
from os import remove, getenv

class Parser:
    def __init__(self, use_default_profile: bool = False):
        self.__images = []
        self.__banned_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

        self.__options = webdriver.ChromeOptions()

        if use_default_profile:
            self.__options.add_argument(rf"user-data-dir=C:\Users\{getenv('username')}\AppData\Local\Google\Chrome\User Data\Default")

        self.__driver = webdriver.Chrome(chrome_options=self.__options)
    def get_screenshot(self, url: str, pop_ups: list[str] = None, elements_to_remove: dict[str, int] = None):

        self.__driver.get(url)
        self.__driver.maximize_window()

        self.__accept_pop_ups(pop_ups)

        self.__scroll(elements_to_remove)
        self.__driver.quit()

        img_name = url
        for banned_char in self.__banned_chars:
            img_name = img_name.replace(banned_char, "-")

        self.__save(img_name)
        self.__release()

    def __accept_pop_ups(self, pop_ups):
        if pop_ups is None:
            return
        for pop_up in pop_ups:
            self.__driver.find_element(By.XPATH, pop_up).click()

    def __scroll(self, elements_to_remove: dict[str, int] = None):
        current = 0
        iteration = 0
        if elements_to_remove is not None:
            keys = list(elements_to_remove)
        else:
            keys = []
        height = self.__driver.execute_script('return document.body.clientHeight')
        step = self.__driver.execute_script("return screen.height") - 160  # Magic number
        while current <= height:
            img_name = f"{str(current)}.png"
            for key in keys:
                if elements_to_remove[key] == iteration:
                    self.__remove_element(key)

            self.__driver.save_screenshot(img_name)
            self.__images.append(cv2.imread(img_name))

            remove(img_name)
            self.__driver.execute_script(f"window.scrollBy(0, {step})")

            iteration += 1
            current += step

    def __save(self, output_name: str):
        if not output_name.endswith(".png"):
            output_name += ".png"
        im_v = cv2.vconcat(self.__images)
        cv2.imwrite(output_name, im_v)
        self.__images.clear()

    def __remove_element(self, elem: str):
        elem = elem.replace('"', '\'')
        self.__driver.execute_script(f'let e = document.evaluate(\"{elem}\", document,null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (e != null)e.remove()')

    def __release(self):
        self.__images = []