import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from downloader import download
from send_email import send
import json
import time
import sys
import logging
# import win32gui
# import win32con
import datetime
import schedule
from show_dialog import show_dialog

logging.basicConfig(filename='logging.log')
driver_flag = 1

with open('output.txt', 'w') as f:
    sys.stdout = f


# def enumHandler(hwnd, lParam):
#     if 'chromedriver.exe' in win32gui.GetWindowText(hwnd):
#         win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)


class IdError(Exception):
    pass


def main():
    global driver
    key_index = []
    # if working_hours[0] <= datetime.datetime.now().hour < working_hours[1] and datetime.datetime.now().day <= 30 and (datetime.datetime.now().month == 6 or datetime.datetime.now().month == 7):
    if working_hours[0] <= datetime.datetime.now().hour < working_hours[1]:
        try:
            for id in ids:
                for item in driver.find_elements_by_class_name('personal-box__item'):
                    if item.text.split('\n')[0] == 'Актуальные':
                        item.click()
                        break
                try:
                    driver.find_element_by_name(str(id)).click()
                except Exception:
                    raise IdError
                driver.find_element_by_class_name('service-card-head__link').click()
                time.sleep(1)
                titles = driver.find_elements_by_class_name('bull-item__self-link')
                time.sleep(2)
                driver.find_element_by_class_name('applier__price-input').clear()
                driver.find_element_by_class_name('applier__price-input').send_keys('200')
                time.sleep(1)
                current_place = int(driver.find_element_by_class_name(
                    'place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(
                    ' место'))
                for title in titles:
                    if 'смесь' in title.text:
                        key_index = titles.index(title) - 1
                        break
                if current_place > key_index:
                    while current_place > key_index:
                        driver.find_element_by_class_name('counter__button_up').click()
                        time.sleep(1)
                        current_place = int(driver.find_element_by_class_name(
                            'place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(
                            ' место'))
                        time.sleep(2)
                elif current_place < key_index:
                    while current_place < key_index:
                        driver.find_element_by_class_name('counter__button_down').click()
                        time.sleep(1)
                        current_place = int(driver.find_element_by_class_name(
                            'place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(
                            ' место'))
                        time.sleep(2)
                    driver.find_element_by_class_name('counter__button_up').click()
                time.sleep(1)
                driver.find_element_by_class_name('stick-form__save-button').click()
                driver.find_element_by_class_name('col_login').click()
                time.sleep(3)
                driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                    'ul').find_elements_by_tag_name('li')[0].click()
        except IndexError:
            driver.find_element_by_class_name('col_login').click()
            time.sleep(3)
            driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                'ul').find_elements_by_tag_name('li')[0].click()
            logging.warning('Index error at main function' + ' ' + str(datetime.datetime.now()))
            show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
        except IdError:
            logging.fatal('Cant find post (invalid id)' + ' ' + str(datetime.datetime.now()))
            send('Cant find post (invalid id)'.capitalize())
            show_dialog('Ошибка могла возникнуть из-за неправильно введенного id объявления, либо из-за обновления структуры сайта фарпост')
        except selenium.common.exceptions.NoSuchElementException:
            driver.find_element_by_class_name('col_login').click()
            time.sleep(3)
            driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                'ul').find_elements_by_tag_name('li')[0].click()
            logging.warning('Element not found' + ' ' + str(datetime.datetime.now()))
            show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
        except selenium.common.exceptions.UnexpectedAlertPresentException:
            driver.switch_to.alert().accept()
            logging.warning('Unexpected alert at main function' + ' ' + str(datetime.datetime.now()))
        except Exception:
            driver.close()
            logging.fatal('Unexpected error at main function' + ' ' + str(datetime.datetime.now()))
            send('!!!FATAL!!! Unexpected error at main function'.capitalize())
            show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
    else:
        try:
            driver.find_element_by_class_name('stick-form__save-button').click()
            driver.find_element_by_class_name('col_login').click()
            time.sleep(3)
            driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                'ul').find_elements_by_tag_name('li')[0].click()
            driver.close()
            logging.warning('Session ended' + ' ' + str(datetime.datetime.now()))
            while working_hours[0] > datetime.datetime.now().hour >= working_hours[1]:
                time.sleep(3)
            else:
                logging.warning('Session started' + ' ' + str(datetime.datetime.now()))
                start()
        except IndexError:
            driver.find_element_by_class_name('col_login').click()
            time.sleep(3)
            driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                'ul').find_elements_by_tag_name('li')[0].click()
            logging.warning('Index error at main function' + ' ' + str(datetime.datetime.now()))
            show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
        except IdError:
            logging.fatal('Cant find post (invalid id)' + ' ' + str(datetime.datetime.now()))
            send('Cant find post (invalid id)'.capitalize())
            show_dialog('Ошибка могла возникнуть из-за неправильно введенного id объявления, либо из-за обновления структуры сайта фарпост')
        except selenium.common.exceptions.UnexpectedAlertPresentException:
            driver.switch_to.alert().accept()
            logging.warning('Unexpected alert at main function' + ' ' + str(datetime.datetime.now()))
        except selenium.common.exceptions.NoSuchElementException:
            driver.find_element_by_class_name('col_login').click()
            time.sleep(3)
            driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                'ul').find_elements_by_tag_name('li')[0].click()
            logging.warning('Element not found' + ' ' + str(datetime.datetime.now()))
            show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
        except Exception:
            driver.close()
            logging.fatal('Unexpected error at main function' + ' ' + str(datetime.datetime.now()))
            send('!!!FATAL!!! Unexpected error at main function'.capitalize())
            show_dialog('Неизвестная ошибка, обратитесь в техподдержку')


def start():
    driver = webdriver.Chrome('/Users/vasiliyganja/Documents/projects/Farpost_keyword/chromedriver')
    driver.get("https://www.farpost.ru/")
    driver.set_window_size(1500, 1000)
    # win32gui.EnumWindows(enumHandler, None)
    time.sleep(3)
    try:
        driver.find_element_by_class_name('login').click()
        with open('profile.json') as f:
            profile_data = json.load(f)
            driver.find_element_by_name('sign').send_keys(profile_data['login'])
            driver.find_element_by_name('password').send_keys(profile_data['password'], Keys.RETURN)
            time.sleep(2)
            driver.find_element_by_class_name('personal-balance-info__balance')
    except IndexError:
        driver.close()
        logging.warning('Element not found' + ' ' + str(datetime.datetime.now()))
        send('!!!FATAL!!! Element not found'.capitalize())
        show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
    except selenium.common.exceptions.NoSuchElementException:
        driver.close()
        logging.fatal('Login Failed' + ' ' + str(datetime.datetime.now()))
        send('!!!FATAL!!! Login Failed'.capitalize())
        show_dialog('Введен неверный логин, пароль, проверте данные и попробуйте снова')
    except selenium.common.exceptions.SessionNotCreatedException:
        show_dialog('Драйвер устарел, обратитесь в техподдержку')
    except Exception:
        driver.close()
        logging.fatal('Unexpected error at start function' + ' ' + str(datetime.datetime.now()))
        send('!!!FATAL!!! Unexpected error at start function'.capitalize())
        show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
    return driver


with open('settings.json') as f:
    settings = json.load(f)
    working_hours = settings['working_hours']
    update_frequency = settings['update_frequency']
    ids = settings['post_ids']


# if working_hours[0] <= datetime.datetime.now().hour < working_hours[1] and datetime.datetime.now().day <= 30 and (datetime.datetime.now().month == 6 or datetime.datetime.now().month == 7):
if working_hours[0] <= datetime.datetime.now().hour < working_hours[1]:
    driver_flag = 0
    driver = start()
    schedule.every(update_frequency).seconds.do(main)
elif driver_flag == 0:
    download()
    driver_flag = 1

while True:
    schedule.run_pending()
    time.sleep(1)