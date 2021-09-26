import schedule
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from send_email import send
import json
import time
import sys
import logging
import win32gui
import win32con
import datetime
from show_dialog import show_dialog
from enum_hendler import enum_handler

logging.basicConfig(filename='logging.log')

with open('output.txt', 'w') as f:
    sys.stdout = f


class IdError(Exception):
    pass


def main():
    global driver, ids, cashback, limit, freeze_flag
    # if working_hours[0] <= datetime.datetime.now().hour < working_hours[1] and datetime.datetime.now().day <= 30 and (datetime.datetime.now().month == 6 or datetime.datetime.now().month == 7):
    if working_hours[0] <= datetime.datetime.now().hour < working_hours[1]:
        try:
            for id in ids:
                time.sleep(3)
                for item in driver.find_elements_by_class_name('personal-box__item'):
                    if item.text.split('\n')[0] == 'Актуальные':
                        item.click()
                        break
                time.sleep(2)
                try:
                    driver.find_element_by_name(str(id)).click()
                except Exception:
                    logging.critical('IdError: cant find post' + ' ' + str(datetime.datetime.now()))
                    raise IdError
                time.sleep(2)
                current = int(driver.find_element_by_class_name('serviceStick').text.split('\n')[0].split()[-1].split('₽')[0])
                driver.find_element_by_class_name('service-card-head__link.serviceStick.applied').click()
                time.sleep(3)
                for_first = int(driver.find_element_by_class_name('stick-applier-steps__price-cell').text.rstrip('₽'))
                driver.find_element_by_class_name('col_login').click()
                time.sleep(5)
                balance = float(''.join(driver.find_element_by_class_name('personalNavLine__balance').text.rstrip('₽').split()))
                current_place = int(driver.find_element_by_class_name('place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(' место'))
                driver.find_element_by_class_name('js-viewdir-subject').click()
                time.sleep(2)
                if balance < for_first != current:
                    logging.critical('Not enough money' + ' ' + str(datetime.datetime.now()))
                    send('NOT ENOUGH MONEY')
                    while current_place < 21:
                        driver.find_element_by_class_name('counter__button_down').click()
                        current_place = int(driver.find_element_by_class_name(
                            'place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(
                            ' место'))
                        time.sleep(2)
                    driver.find_element_by_class_name('stick-form__save-button').click()
                    time.sleep(cashback)
                    driver.refresh()
                    driver.find_element_by_class_name('bzr-btn.bzr-btn_size_l.bzr-btn_wide').click()
                time.sleep(3)
                if current < for_first <= limit and for_first <= balance:
                    logging.warning('Upped to first' + ' ' + str(datetime.datetime.now()))
                    driver.find_element_by_class_name('stick-applier-steps__price-cell').click()
                elif current > for_first:
                    driver.find_element_by_class_name('stick-applier-steps__price-cell').click()
                elif for_first > balance != current and balance < limit:
                    send('Limit reached'.capitalize())
                    logging.critical('Limit reached' + ' ' + str(datetime.datetime.now()))
                    input = driver.find_element_by_class_name('applier__price-input')
                    input.clear()
                    input.send_keys(str(balance))
                time.sleep(2)
                if current_place == int(driver.find_element_by_class_name('place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(' место')):
                    freeze_flag += 1
                else:
                    freeze_flag = 0
                driver.find_element_by_class_name('stick-form__save-button').click()
                driver.find_element_by_class_name('col_login').click()
                time.sleep(3)
                driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[0].click()
                if freeze_flag > 20:
                    logging.critical('Post froze' + ' ' + str(datetime.datetime.now()))
                    send('Post froze'.capitalize())
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
            for id in ids:
                time.sleep(3)
                driver.find_elements_by_class_name('personal-box__item')[1].click()
                try:
                    driver.find_element_by_name(str(id)).click()
                except Exception:
                    raise IdError
                driver.find_element_by_class_name('bzr-btn.bzr-btn_size_l.bzr-btn_wide').click()
                time.sleep(5)
                while int(driver.find_element_by_class_name(
                        'place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(
                        ' место')) < place:
                    driver.find_element_by_class_name('counter__button_down').click()
                    time.sleep(2)
                driver.find_element_by_class_name('stick-form__save-button').click()
                driver.find_element_by_class_name('col_login').click()
                time.sleep(3)
                driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
                    'ul').find_elements_by_tag_name('li')[0].click()
                driver.close()
                logging.warning('Session ended')
            while working_hours[0] > datetime.datetime.now().hour >= working_hours[1]:
                time.sleep(3)
            else:
                logging.warning('Session started')
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


# def update():
#     global driver, id, place
#     if working_hours[0] <= datetime.datetime.now().hour < working_hours[1]:
#         try:
#             for id in ids:
#                 time.sleep(3)
#                 driver.find_elements_by_class_name('personal-box__item')[1].click()
#                 try:
#                     driver.find_element_by_name(str(id)).click()
#                 except Exception:
#                     raise IdError
#                 driver.find_element_by_class_name('service-card-head__link.serviceStick.applied').click()
#                 time.sleep(5)
#                 while int(driver.find_element_by_class_name('place-description__position.place-description__position_marked').text.lstrip('за ').rstrip(' место')) < place:
#                     driver.find_element_by_class_name('counter__button_down').click()
#                     time.sleep(2)
#                 driver.find_element_by_class_name('stick-form__save-button').click()
#                 driver.find_element_by_class_name('col_login').click()
#                 time.sleep(3)
#                 driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name('ul').find_elements_by_tag_name('li')[0].click()
#         except IndexError:
#             driver.find_element_by_class_name('col_login').click()
#             time.sleep(3)
#             driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
#                 'ul').find_elements_by_tag_name('li')[0].click()
#             logging.warning('Element not found')
#         except selenium.common.exceptions.NoSuchElementException:
#             driver.find_element_by_class_name('col_login').click()
#             time.sleep(3)
#             driver.find_element_by_class_name('subCol.profileCol').find_element_by_tag_name(
#                 'ul').find_elements_by_tag_name('li')[0].click()
#             logging.warning('Element not found')
#         except IdError:
#             logging.fatal('Cant find post (invalid id)')
#             send('Cant find post (invalid id)'.capitalize())

def start():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get("https://www.farpost.ru/")
    driver.set_window_size(1500, 1000)
    win32gui.EnumWindows(enum_handler, None)
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
        show_dialog('Введен неверный логин, пароль, проверте данные и попробуйте снова')
        # send('!!!FATAL!!! Login Failed'.capitalize())
    except selenium.common.exceptions.SessionNotCreatedException:
        show_dialog('Драйвер устарел, установите новый: https://chromedriver.chromium.org/downloads')
    except Exception:
        driver.close()
        logging.fatal('Unexpected error at start function' + ' ' + str(datetime.datetime.now()))
        # send('!!!FATAL!!! Unexpected error at start function'.capitalize())
        show_dialog('Неизвестная ошибка, обратитесь в техподдержку')
    return driver


with open('settings.json') as f:
    settings = json.load(f)
    working_hours = settings['working_hours']
    update_frequency = settings['update_frequency']
    replace_frequency = settings['replace_frequency']
    limit = settings['price_limit']
    ids = settings['post_ids']
    place = settings['place']
    cashback = settings['cashback_waiting']
    freeze_flag = 0

# if working_hours[0] <= datetime.datetime.now().hour < working_hours[1] and datetime.datetime.now().day <= 30 and (datetime.datetime.now().month == 6 or datetime.datetime.now().month == 7):
if working_hours[0] <= datetime.datetime.now().hour < working_hours[1]:
    driver = start()
    schedule.every(update_frequency).seconds.do(main)
    # schedule.every(replace_frequency).seconds.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)