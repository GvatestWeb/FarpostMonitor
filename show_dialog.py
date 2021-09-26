from PyQt5.QtWidgets import QMessageBox, QApplication
import sys
import os


def show_dialog(text):
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Внимание")
    msg.setInformativeText(text)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    retval = msg.exec_()
    if retval == 1024:
        return True
    return False
