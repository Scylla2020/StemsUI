#Credits - https://github.com/deezer/spleeter/wiki/4.-API-Reference

import os
import os
import sys
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import *
import logo_rc
import threading

#Avoid displaying Tensorflow verbose warnings
import warnings
warnings.filterwarnings('ignore')

# from spleeter.separator import Separator

#Initialise Separator instance
def initialise(num):
    # Using embedded configuration.
    separator = Separator(f'spleeter:{num}stems')

    # Using custom configuration file.
    # separator = Separator('/path/to/config.json')


if __name__ == "__main__":
    cur_dir = os.getcwd()
    app=QtWidgets.QApplication(sys.argv)

    cur_dir = os.path.normpath(cur_dir)
    ui_path = os.path.join(cur_dir, "ui_files","interface.ui")
    window = uic.loadUi(ui_path)
    model = QFileSystemModel()
    # model.setRootPath(ui_path)
    # model.setRootPath(QDir.currentPath())
    tree = window.tableView
    tree.setModel(model)
 
    window.show()
    sys.exit(app.exec_())


