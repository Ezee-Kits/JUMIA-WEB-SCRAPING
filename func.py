
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from difflib import SequenceMatcher as ss
from datetime import date, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import numpy as np
import pyautogui
import requests
import random
import time
import cv2
import os





date_value = 1
def main_date(day):
    last_date = date.today() + timedelta(day)
    return last_date



def create_product_dir(product_name):
    sub_dir = os.path.abspath('Products')
    product_dir = product_name
    full_path = os.path.join(sub_dir,product_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path


def scrolling(lenght_to_scroll,how_many_times = 1):
    for _ in range(how_many_times):
        pyautogui.scroll(lenght_to_scroll)
        time.sleep(.2)

def create_each_product_dir(each_product_dir_name):
    sub_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),'Products')
    each_product_dir = each_product_dir_name
    full_path = os.path.join(sub_dir,each_product_dir)
    try:
        os.makedirs(full_path)
    except:
        print('\n PATH ALREADY EXIST BUT WAS CREATED SUCCESFULLY \n')
    return full_path

def saving_file2(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())
    df.to_csv(path, index=False)
    print('============================= CSV FILE SAVED ==========================')


def saving_files(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')


def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)



def locate_click(img,confidence,click_amt = 1,gray_mode = True):
    img_to_locate = img
    while True:
        try:
            object_located = pyautogui.locateCenterOnScreen(image=img_to_locate,confidence=confidence,grayscale=gray_mode)
            if len(object_located) ==2:
                break
            else:
                pass
        except:
            print(f'\n IMAGE IS NOT CLICKED {img_to_locate}\n')   
    pyautogui.moveTo(object_located)
    for _ in range(click_amt):
        time.sleep(.3)
        pyautogui.leftClick(object_located)


def locate_move(img,confidence,x_add=0,y_add=0):
    img_to_locate = img
    while True:
        try:
            object_located = pyautogui.locateCenterOnScreen(image=img_to_locate,confidence=confidence,grayscale=True)
            if len(object_located) ==2:
                break
            else:
                pass
        except:
            print(f'\n IMAGE IS NOT CLICKED {img_to_locate}\n')
    time.sleep(.2)  
    print(object_located)  
    pyautogui.moveTo(   object_located[0]+x_add, object_located[1]+y_add   )


def selenium_init():
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\USER\\AppData\\Local\\Google\\Chrome")
    driver = webdriver.Chrome('C:\\Users\\USER\\Desktop\\chrome\\chromedriver.exe', options=options, desired_capabilities=capa)
    wait = WebDriverWait(driver, 60)
    return driver,wait,EC,By


def taking_ss(image, acc_level):
    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Perform edge detection and adaptive thresholding
    image_edges = cv2.Canny(image, 50, 200)
    screenshot_edges = cv2.Canny(screenshot, 50, 200)
    image_thresholded = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    screenshot_thresholded = cv2.adaptiveThreshold(screenshot, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Combine edges and thresholded images
    combined_image = cv2.bitwise_or(image_edges, image_thresholded)
    combined_screenshot = cv2.bitwise_or(screenshot_edges, screenshot_thresholded)

    # Perform template matching
    result = cv2.matchTemplate(combined_screenshot, combined_image, cv2.TM_CCOEFF_NORMED)

    # Set a threshold
    locations = np.where(result >= acc_level)
    return locations

def handling_image_SS(image_path, acc_level=0.8, scales=[1.0, 0.9, 0.8, 0.7,0.6,0.5], timeout=60,click_amt=1):
    # Read the image file
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        for scale in scales:
            # Resize the image according to the current scale
            image = cv2.resize(original_image, (int(original_image.shape[1] * scale), int(original_image.shape[0] * scale)))
            locations = taking_ss(image=image, acc_level=acc_level)
            if locations[0].size > 0:
                # Get the location of the first match
                location = list(zip(*locations[::-1]))[0]
                # Calculate the center of the matched region
                center_x = location[0] + image.shape[1] // 2
                center_y = location[1] + image.shape[0] // 2
                # Move the mouse to the center of the matched region and click
                for _ in range(click_amt):
                    pyautogui.click(center_x, center_y)
                    time.sleep(0.2)
                print(f"Clicked on the image at ({center_x}, {center_y}) with scale {scale}")
                return True
            time.sleep(.2)  # Adding a small delay between attempts
        print(f"{image_path} << >> Image not found with current settings. Retrying...")

    print(f"Image not found within {timeout} seconds.")
    return False


# Provide the path to your image
# handling_image_SS(image_path='IMAGES/select_emptybox.PNG')