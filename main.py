from selenium import webdriver
import cv2
from os import remove
class Parser:
    @staticmethod
    def get_screenshot(url: str):
        driver = webdriver.Chrome()
        driver.get(url)
        driver.maximize_window()

        current = 0  # driver.execute_script("return window.scrollY")
        height = driver.execute_script('return document.body.clientHeight')
        step = driver.execute_script("return screen.height") - 160  # Magic number

        images = []
        while current <= height:
            # img_name = "test\\" + str(current) + ".jpeg"
            img_name = f"{str(current)}.jpg"
            driver.save_screenshot(img_name)
            images.append(cv2.imread(img_name))
            remove(img_name)
            driver.execute_script(f"window.scrollBy(0, {step})")
            current += step
        im_v = cv2.vconcat(images)
        cv2.imwrite('out.jpg', im_v)
        driver.quit()

if __name__ == '__main__':
    Parser.get_screenshot('https://www.python.org')