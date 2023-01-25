from selenium import webdriver
import cv2
from os import remove, getenv


class Parser:
    def get_screenshot(self, url: str, use_default_profile: bool = False):
        options = webdriver.ChromeOptions()

        if use_default_profile:
            options.add_argument(rf"user-data-dir=C:\Users\{getenv('username')}\AppData\Local\Google\Chrome\User Data\Default")
            
        driver = webdriver.Chrome(chrome_options=options)
        driver.get(url)
        driver.maximize_window()
        current = 0
        height = driver.execute_script('return document.body.clientHeight')
        step = driver.execute_script("return screen.height") - 160  # Magic number

        images = []
        while current <= height:
            img_name = f"{str(current)}.png"
            driver.save_screenshot(img_name)
            images.append(cv2.imread(img_name))
            remove(img_name)
            driver.execute_script(f"window.scrollBy(0, {step})")
            current += step
        driver.quit()
        im_v = cv2.vconcat(images)
        cv2.imwrite('out.png', im_v)
