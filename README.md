# Web-site full-scale screenshot taker

## An example from Python official web-site
![img](https://github.com/Jujumba/ScreenshotTaker/blob/master/examples/python.org.png)

## Prerequisites
1) Python 3.10+

## Build
1) __pip install -r requirements.txt__
2) python main.py

## Note
1) You can specify the XPATH of the element to be removed after certain iteration. For example `Parser().get_screenshot("https://github.com/Jujumba/ScreenshotTaker/tree/master/", elements_to_remove={
        '//*[@id="readme"]/div[1]': 1
    })` will remove "readme header" after first iteration. 
