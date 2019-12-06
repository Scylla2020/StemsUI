import sys
from PyQt5 import QtCore, QtWidgets
from interface import Ui_MainWindow
import audio_metadata
from pathlib import Path
import time
import threading
import os

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Stems UI')
        self.tableWidget.setAcceptDrops(True)
        self.tableWidget.viewport().installEventFilter(self)
        types = ['text/uri-list']
        types.extend(self.tableWidget.mimeTypes())
        self.tableWidget.mimeTypes = lambda: types
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnWidth(0,280) #name
        self.tableWidget.setColumnWidth(1,70) #size
        self.tableWidget.setColumnWidth(2,60)  #duration
        self.tableWidget.setColumnWidth(3,50)  #format
        self.tableWidget.setColumnWidth(4,50)  #bitrate

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Drop and
            event.mimeData().hasUrls()):
            for url in event.mimeData().urls():
                self.addFile(url.toLocalFile())
            return True
        return super().eventFilter(source, event)

    def keyPressEvent(self,event):
        if event.key()==QtCore.Qt.Key_Delete:
            row = self.tableWidget.currentRow()
            self.tableWidget.removeRow(row)

    def addFile(self, filepath):
        #Get metadata of audio
        metadata = audio_metadata.load(filepath)
        
        name = Path(filepath).stem
        size = str(round(metadata.filesize/1000000, 2))
        duration = str(time.strftime("%M:%S",time.gmtime(metadata.streaminfo.duration)))
        format = str(metadata.streaminfo.bitrate_mode).split('Bitrate')[0]
        bitrate = str(int(metadata.streaminfo.bitrate/1000))

        data_list = [name,size,duration, format,bitrate,filepath]

        #Populate table
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        i = 0
  
        for item in data_list:
            param = QtWidgets.QTableWidgetItem(item)
            self.tableWidget.setItem(row, i, param)
            i+=1

def fetch():
    #Get current settings
    settings={}
    settings['codec'] = window.comboBox_2.currentText()
    settings['bitrate'] = window.comboBox.currentText()

    settings['offset'] = 0
    if window.lineEdit_3.text():
        settings['offset'] = int(window.lineEdit_3.text())

    settings['output_folder'] = "Output"
    if window.lineEdit.text():
        settings['output_folder'] = window.lineEdit.text()

    settings['duration'] = 600
    if window.lineEdit_2.text():
        settings['duration'] = window.lineEdit_2.text()
  
    settings['stems'] = window.comboBox_3.currentText()
    rowcount = window.tableWidget.rowCount()
   
   #Create and populate main dictionary 
    data = {}
    for row in range(0,rowcount):
        name = window.tableWidget.item(row,0).text()
        filename = window.tableWidget.item(row,5).text()
        data[name] = {}
        data[name]['filename'] = filename
    split_thread(data=data, settings=settings)
 
def splitfiles(data,settings):
    window.plainTextEdit.insertPlainText("Working...")
    import warnings
    warnings.filterwarnings('ignore')
    from spleeter.separator import Separator

    # Using embedded configuration.
    stem = settings['stems']
    separator = Separator(f'spleeter:{stem}')
    
    # List of input to process.
    audio_descriptors = [data[key]['filename'] for key in data.keys()]
 
    #Output settings
    duration = int(settings['duration'])
    bitrate = settings['bitrate']
    codec = settings['codec']
    output_folder = settings['output_folder']
    offset = settings['offset']
    total_songs = len(audio_descriptors)

    #Main process
    for song in audio_descriptors:
        output_folder = output_folder + "\\" + Path(song).stem
        separator.separate_to_file(song, output_folder, duration=duration, codec=codec, bitrate=bitrate, offset=offset, synchronous=False)
          

    # Wait for batch to finish.
    separator.join()
    window.plainTextEdit.insertPlainText("Done")

def clear():
    window.tableWidget.setRowCount(0)
     
def split_thread(data, settings):
    x = threading.Thread(target=splitfiles, args=[data,settings])
    x.start()
    x.join()

def fetch_thread():
    y = threading.Thread(target=fetch)
    y.start()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.pushButton.clicked.connect(fetch_thread)
    window.pushButton_2.clicked.connect(clear)
    bitrates = ['320k', '256k','224k','192k']
    stems = ['2stems', '4stems','5stems']
    codecs = ['mp3', 'wav']
    window.comboBox.insertItems(0,bitrates)
    window.comboBox_2.insertItems(0,codecs)
    window.comboBox_3.insertItems(0,stems)
    
    window.show()
    sys.exit(app.exec_())
