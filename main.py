import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QLabel, QMessageBox
from templates.main_wind import Ui_MainWindow
from subprocess import Popen
import subprocess
import sys
import logging
import datetime
from show_dialog import show_dialog


# def check_id():
#     with open('settings.json') as f:
#         data = json.load(f)
#         with open('output.txt', 'w') as output:
#             subprocess.call('wmic path win32_usbhub Where (Caption="Запоминающее устройство для USB") get DeviceID', stdout=output, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
#         with open('output.txt') as output:
#             out = output.read()
#         out = ''.join(''.join(out.split('\n\n')).split('\x00')).split('\n\n')
#         for i in out:
#             if data['device_id'] == i.strip():
#                 return
#     show_dialog('USB ночитель не обнаружен')
#     exit()
#
#
# check_id()

with open('logging.log', 'w') as f:
    f.truncate()
logging.basicConfig(filename='logging.log')


class Main_Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.labell = QLabel(self)
        self.statusbar.setStyleSheet('background: #d5d5d5;')
        if not os.path.exists('profile.json') or not os.path.exists('settings.json'):
            self.labell.setText('FILL IN NECESSARY DATA      ')
            self.statusbar.setStyleSheet('background: red;')
        self.statusbar.addWidget(self.labell)
        fs = open('settings.json')
        fp = open('profile.json')
        settings = json.load(fs)
        profile = json.load(fp)
        self.label.setText('login' + ': ' + profile['login'])
        self.label_2.setText('password' + ': ' + profile['password'])
        # self.label_5.setText('update_frequency' + ': ' + str(settings['update_frequency']))
        self.label_6.setText('working_hours' + ': ' + str(settings['working_hours'][0]) + '-' + str(settings['working_hours'][1]))
        self.label_7.setText('post_ids' + ': ' + str(settings['post_ids']))
        # self.label_9.setText('cashback_waiting' + ': ' + str(settings['cashback_waiting']))
        self.label_10.setText('mail' + ': ' + str(profile['mail']))
        self.actionProfile_Data.triggered.connect(self.change_profile_data)
        self.actionUpdate_Frequency.triggered.connect(self.change_update_frequency)
        self.actionWorking_Hours.triggered.connect(self.change_working_hours)
        self.actionPost_Ids.triggered.connect(self.change_post_id)
        self.actionKeyword.triggered.connect(self.change_keyword)
        self.pushButton_3.clicked.connect(self.process_manager)
        self.pushButton_4.clicked.connect(self.process_manager)
        self.process = ''
        fp.close()
        fs.close()

    def process_manager(self):
        if not self.process:
            self.statusbar.setStyleSheet('background: #d5d5d5;')
            self.statusbar.removeWidget(self.labell)
        with open('settings.json') as f:
            data = json.load(f)
            if self.sender() == self.pushButton_3 and not self.process and 'post_ids' in data.keys():
                self.labell = QLabel(self)
                Popen('python scheduler.py')
                self.labell.setText('Started')
                self.statusbar.addWidget(self.labell)
                logging.warning('Started' + ' ' + str(datetime.datetime.now()))
            elif self.sender() == self.pushButton_4:
                logging.warning('Stoped')
                os.system('taskkill /IM scheduler.exe /F')
                os.system('taskkill /IM chromedriver.exe /F')
                os.system('taskkill /IM main.exe /F')
                # self.process = ''
                # self.labell = QLabel(self)
                # self.labell.setText('Stoped')
                # self.statusbar.addWidget(self.labell)
            elif not self.process:
                self.statusbar.setStyleSheet('background: red;')
                self.statusbar.addWidget(self.labell)
                show_dialog('Id объявлений не найдены')
                logging.warning('Post Id error' + ' ' + str(datetime.datetime.now()))

    def change_post_id(self):
        self.statusbar.setStyleSheet('background: #d5d5d5;')
        self.statusbar.removeWidget(self.labell)
        if os.path.exists('settings.json'):
            with open('settings.json') as f:
                data = json.load(f)
                if 'post_id' in data.keys():
                    post_id, ok_pressed0 = QInputDialog.getText(self, "Enter the post ids",
                        f"{data['post_id']}, (******, ******, ******)                             ")
                    while len(post_id) == 0:
                        post_id, ok_pressed0 = QInputDialog.getText(self, "Enter the post ids",
                            f"{data['post_id']}, (******, ******, ******)                                 ")
                else:
                    post_id, ok_pressed0 = QInputDialog.getText(self, "Enter the post ids",
                        "post ids, (******, ******, ******)                                           ")
                    while len(post_id) == 0:
                        post_id, ok_pressed0 = QInputDialog.getText(self, "Enter the post ids",
                            "post ids, (******, ******, ******)                                           ")
        else:
            post_id, ok_pressed0 = QInputDialog.getText(self, "Enter the post ids",
                "post ids, (******, ******, ******)                                           ")
            while len(post_id) == 0:
                post_id, ok_pressed0 = QInputDialog.getText(self, "Enter the post ids",
                    "post ids, (******, ******, ******)                                           ")
        if os.path.exists('settings.json'):
            with open('settings.json') as f:
                settings = json.load(f)
                post_id = [int(post.strip()) for post in post_id.split(',')]
                settings['post_ids'] = post_id
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
            logging.info('Changed Post Ids' + ' ' + str(datetime.datetime.now()))
        else:
            with open('settings.json', 'w') as f:
                post_id = [int(post.strip()) for post in post_id.split(',')]
                settings = {'post_id': post_id}
                json.dump(settings, f)
            logging.info('Changed Post Ids' + ' ' + str(datetime.datetime.now()))

    def change_update_frequency(self):
        self.statusbar.setStyleSheet('background: #d5d5d5;')
        self.statusbar.removeWidget(self.labell)
        if os.path.exists('settings.json'):
            with open('settings.json') as f:
                data = json.load(f)
                if 'update_frequency' in data.keys():
                    update_frequency, ok_pressed0 = QInputDialog.getText(self, "Enter the update frequency",
                        f"{data['update_frequency']}                        ")
                    while len(update_frequency) == 0:
                        update_frequency, ok_pressed0 = QInputDialog.getText(self, "Enter the update frequency",
                            f"{data['update_frequency']}                         ")
                else:
                    update_frequency, ok_pressed0 = QInputDialog.getText(self, "Enter the update frequency",
                        "update frequency                                           ")
                    while len(update_frequency) == 0:
                        update_frequency, ok_pressed0 = QInputDialog.getText(self, "Enter the update frequency",
                            "update frequency                                           ")
        else:
            update_frequency, ok_pressed0 = QInputDialog.getText(self, "Enter the update frequency",
                "update frequency                                           ")
            while len(update_frequency) == 0:
                update_frequency, ok_pressed0 = QInputDialog.getText(self, "Enter the update frequency",
                    "update frequency                                           ")
        if os.path.exists('settings.json') and update_frequency.isdigit():
            with open('settings.json') as f:
                settings = json.load(f)
                settings['update_frequency'] = int(update_frequency)
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
                logging.info('Changed Update Frequency' + ' ' + str(datetime.datetime.now()))
        elif update_frequency.isdigit():
            with open('settings.json', 'w') as f:
                settings = {'update_frequency': int(update_frequency)}
                json.dump(settings, f)
                logging.info('Changed Update Frequency' + ' ' + str(datetime.datetime.now()))
        else:
            self.labell = QLabel(self)
            self.labell.setText('WRONG UPDATE FREQUENCY      ')
            self.statusbar.setStyleSheet('background: red;')
            self.statusbar.addWidget(self.labell)

    def change_working_hours(self):
        self.statusbar.setStyleSheet('background: #d5d5d5;')
        self.statusbar.removeWidget(self.labell)
        if os.path.exists('settings.json'):
            with open('settings.json') as f:
                data = json.load(f)
                if 'working_hours' in data.keys():
                    working_hours, ok_pressed0 = QInputDialog.getText(self, "Enter the working_hours",
                        f"{str(data['working_hours'][0]) + '-' + str(data['working_hours'][1])}                        ")
                    while len(working_hours) == 0:
                        working_hours, ok_pressed0 = QInputDialog.getText(self, "Enter the working_hours",
                            f"{str(data['working_hours'][0]) + '-' + str(data['working_hours'][1])}                         ")
                else:
                    working_hours, ok_pressed0 = QInputDialog.getText(self, "Enter the working_hours",
                        "working_hours                                           ")
                    while len(working_hours) == 0:
                        working_hours, ok_pressed0 = QInputDialog.getText(self, "Enter the working_hours",
                            "working_hours                                           ")
        else:
            working_hours, ok_pressed0 = QInputDialog.getText(self, "Enter the working_hours",
                "working_hours                                           ")
            while len(working_hours) == 0:
                working_hours, ok_pressed0 = QInputDialog.getText(self, "Enter the working_hours",
                    "working_hours                                           ")
        working_hours = working_hours.split('-')
        if os.path.exists('settings.json') and len(working_hours) == 2:
            with open('settings.json') as f:
                settings = json.load(f)
                settings['working_hours'] = [int(working_hours[0]), int(working_hours[1])]
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
                logging.info('Changed Working Hours' + ' ' + str(datetime.datetime.now()))
        elif len(working_hours) == 2:
            with open('settings.json', 'w') as f:
                settings = {'working_hours': [int(working_hours[0]), int(working_hours[1])]}
                json.dump(settings, f)
                logging.info('Changed Working Hours' + ' ' + str(datetime.datetime.now()))
        else:
            self.labell = QLabel(self)
            self.labell.setText('WRONG WORKING HOURS      ')
            self.statusbar.setStyleSheet('background: red;')
            self.statusbar.addWidget(self.labell)

    def change_profile_data(self):
        self.statusbar.setStyleSheet('background: #d5d5d5;')
        self.statusbar.removeWidget(self.labell)

        login, ok_pressed0 = QInputDialog.getText(self, "Enter your login",
            "Login:                                                                    ")
        password, ok_pressed1 = QInputDialog.getText(self, "Enter your password",
            "Password:                                                                    ")
        mail, ok_pressed1 = QInputDialog.getText(self, "Enter your mail",
            "Mail:                                                                    ")
        if ok_pressed0 and ok_pressed1:
            with open('settings.json') as f:
                settings = json.load(f)
                settings['login'] = login
                settings['password'] = password
                settings['mail'] = mail
            with open('profile.json', 'w') as f:
                json.dump(settings, f)
                logging.info('Changed Profile Data' + ' ' + str(datetime.datetime.now()))

    def change_keyword(self):
        self.statusbar.setStyleSheet('background: #d5d5d5;')
        self.statusbar.removeWidget(self.labell)

        keyword, ok_pressed0 = QInputDialog.getText(self, "Enter new keyword",
            "Keyword:                                                                    ")

        if ok_pressed0:
            profile_data = {
                'keyword': keyword
            }
            with open('settings.json', 'w') as f:
                json.dump(profile_data, f)
                logging.info('Changed keyword' + ' ' + str(datetime.datetime.now()))

    # def change_card_data(self):
    #     self.statusbar.setStyleSheet('background: #d5d5d5;')
    #     self.statusbar.removeWidget(self.labell)
    #
    #     card_number, ok_pressed0 = QInputDialog.getText(self, "Enter the card number",
    #         "Number (000 000 000 000 0000):                                           ")
    #     while len(card_number) != 16:
    #         card_number, ok_pressed0 = QInputDialog.getText(self, "Enter the card number",
    #             "Number (000 000 000 000 0000):                                           ")
    #
    #     card_month, ok_pressed1 = QInputDialog.getText(self, "Enter the month",
    #         "Month: (00):    ")
    #     while len(card_month) != 2:
    #         card_month, ok_pressed1 = QInputDialog.getText(self, "Enter the month",
    #             "Month: (00):    ")
    #
    #     card_year, ok_pressed2 = QInputDialog.getText(self, "Enter the card year",
    #         "Year (0000):    ")
    #     while len(card_year) != 4:
    #         card_year, ok_pressed2 = QInputDialog.getText(self, "Enter the card year",
    #             "Year (0000):    ")
    #
    #     card_owner, ok_pressed3 = QInputDialog.getText(self, "Enter the card owner",
    #         "Owner:                                                                    ")
    #
    #     card_cvc, ok_pressed4 = QInputDialog.getText(self, "Enter the card CVC code",
    #         "CVC (000):      ")
    #     while len(card_cvc) != 3:
    #         card_cvc, ok_pressed4 = QInputDialog.getText(self, "Enter the card CVC code",
    #             "CVC (000):      ")
    #     if ok_pressed0 and ok_pressed1 and ok_pressed2 and ok_pressed3 and ok_pressed4:
    #         card_data = {
    #             'card_number': card_number,
    #             'card_month': card_month,
    #             'card_year': card_year,
    #             'card_owner': card_owner,
    #             'card_cvc': card_cvc
    #         }
    #         with open('card.json', 'w') as f:
    #             json.dump(card_data, f)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_Window()
    ex.show()
    if app.exec_() == 0:
        logging.warning('Stoped')
        os.system('taskkill /IM chromedriver.exe /F')
        os.system('taskkill /IM scheduler.exe /F')
        os.system('taskkill /IM main.exe /F')

