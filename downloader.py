import logging
from selenium import webdriver
import time
import os
import requests
from bs4 import BeautifulSoup
import json
import datetime
from send_email import send
import zipfile
from show_dialog import show_dialog
from enum_hendler import enum_handler
import win32gui


def download():
    # try:
        with open('settings.json') as f:
            data = json.load(f)
            path_to_program = data['path_to_program']
        os.system('taskkill /IM chromedriver_old.exe /F')
        os.remove('chromedriver_old.exe')
        resp = requests.get('https://chromedriver.chromium.org/downloads')
        soup = BeautifulSoup(resp.text, 'html.parser')
        versions = soup.find_all("a", {"class": "XqQF9c"})
        driver_version = versions[1].text.split()[1]
        os.rename('chromedriver.exe', 'chromedriver_old.exe')
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": path_to_program}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path='chromedriver_old.exe', options=chrome_options)
        driver.get("https://chromedriver.chromium.org/downloads")
        driver.set_window_size(1500, 1000)
        win32gui.EnumWindows(enum_handler, None)
        time.sleep(3)
        versions = driver.find_elements_by_class_name('TYR86d.wXCUfe.zfr3Q')
        path_to_download = versions[1].find_element_by_class_name('aw5Odc').find_element_by_tag_name('a').get_attribute('href')
        driver.get(path_to_download)
        time.sleep(3)
        packs = driver.find_elements_by_tag_name('tr')
        for pack in packs[3:]:
            link = pack.find_elements_by_tag_name('td')[1].find_element_by_tag_name('a')
            link_text = link.text
            if 'win32' in link_text:
                link.click()
                break
        while True:
            if os.path.exists('chromedriver_win32.zip'):
                driver.close()
                os.system('taskkill /IM chromedriver_old.exe /F')
                with zipfile.ZipFile('chromedriver_win32.zip', 'r') as zip_ref:
                    zip_ref.extract('chromedriver.exe')
                os.remove('chromedriver_win32.zip')
                break
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            settings['driver_version'] = driver_version
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    # except Exception:
    #     try:
    #         driver.close()
    #     except UnboundLocalError:
    #         logging.fatal('Cant rename chromedriver.exe to chromedriver_old.exe' + ' ' + str(datetime.datetime.now()))
    #     logging.fatal('Unexpected error at download function' + ' ' + str(datetime.datetime.now()))
    #     send('!!!FATAL!!! Unexpected error at download function'.capitalize())
    #     show_dialog('Не удалось скачать драйвер')


def compare_versions_of_driver():
    with open('settings.json') as f:
        settings = json.load(f)

    resp = requests.get('https://chromedriver.chromium.org/downloads')
    soup = BeautifulSoup(resp.text, 'html.parser')
    versions = soup.find_all("a", {"class": "XqQF9c"})
    driver_version = versions[1].text.split()[1]
    if driver_version != settings['driver_version']:
        response = show_dialog('Обновить драйвер до последней версии?')
        if response:
            download()