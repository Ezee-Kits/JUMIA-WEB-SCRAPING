from datetime import date, timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import requests
import atexit
import random
import time
import os


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

def info_init():
    url = "https://trying-20541-default-rtdb.firebaseio.com/Main_info.json"
    response = requests.get(url)
    data = response.json()['main_init']
    print(data)
info_init()

def drop_duplicate(path):
    all_df = pd.read_csv(path)
    all_df = all_df.drop_duplicates(keep='first')
    all_df = all_df.reset_index()
    all_df.drop(['index'], axis=1, inplace=True)
    all_df.to_csv(path, index=False)
    print(f"Image not found within {timeout} seconds.")
    return False

atexit.register(info_init)
