# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ParaSetting.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys
sys.path.append('.')
sys.path.append('.\\commu\\CommuMain')
sys.path.append('.\\ui\\')


from PyQt4 import QtCore, QtGui
from commu.CommuMain import Commu

#from commu.Translate import Translate

import numpy as np
import pyqtgraph as pg


#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as figureCanvas
#from matplotlib.figure import Figure
#$import matplotlib.pyplot as plt

import threading
import time


en_version = 1
if 1 == en_version:
    from ui.Ui_UpSite_en import Ui_CTH
    from ui.Ui_about_en import Ui_AboutDialog
    from ui.Ui_help_en import Ui_HelpDialog
    from ui.Ui_timer_en import Ui_calibrationClockDialog
    from ui.Ui_ReturnInfo_en import Ui_returnInfoDialog
else:
    from ui.Ui_UpSite import Ui_CTH
    from ui.Ui_about import Ui_AboutDialog
    from ui.Ui_help import Ui_HelpDialog
    from ui.Ui_timer import Ui_calibrationClockDialog
    from ui.Ui_ReturnInfo import Ui_returnInfoDialog

#from ui.Ui_ReceiveFile import Ui_ReceiveFileDialog

import warnings
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
        
        
class Ctrl_Ui_CTH(Ui_CTH):
    
    def __init__(self, VID_CAPAC, PID_CAPAC):
        super().__init__()
        self.str = list()
        self.para = dict()
        #define usb API 
        self.commu = Commu(VID_CAPAC, PID_CAPAC)
        self.updateThread = None
        self.CTH = None
        self.index1Flag = False
        self.index2Flag = False
        self.reDrawCurveFlag = False
        self.dt = list()
        self.co2 = list()
        self.temp = list()
        self.humi = list()
        self.pres = list()
        self.batt = list()
        self.filePath = '.\\data\\example.csv'
        self.logoPath = 'image/logo.ico'
        self.selectFileModelIndex = None
        self.connectFlag = False

        self.recordCnt = 0
    
    def setupUi(self, CTH, realTimeStatus, para):
        super().setupUi(CTH)
        #super().retranslateUi(CTH)
        self.CTH = CTH
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/logo.ico"),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.CTH.setWindowIcon(icon)
        
        '''
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        '''
        
        self.num.setValidator(QtGui.QIntValidator(1, 99999999))
        #self.name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[1-9][0-9]{1,9}")))
        self.recordTime.setValidator(QtGui.QIntValidator(1, 99999999))
        self.sampleInterval.setValidator(QtGui.QIntValidator(1, 999999))
        self.alarmValue.setValidator(QtGui.QIntValidator(1, 5000))
        #self.alarm.setValidator(QtGui.QIntValidator(1, 2))
        #self.hand.setValidator(QtGui.QIntValidator(1, 2))
        self.name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("\\w{1,8}")))
        
        status,p,err = self.getInitStatus()
        #print('realTimeStatus : ',status)
        #print('para : ',p)
        if err == True:
            realTimeStatus = status
            if 0 != int(p['num']):
                para = p
        else:
            pass
            #print('get init status failed')
        self.num.setText(para["num"])
        self.name.setText(para["name"])
        self.recordTime.setText(para["recordTime"])
        self.sampleInterval.setText(para["sampleInterval"][0:-1])
        self.sampleInvBox.setCurrentIndex(self.sampleIntervalUnit2Index(para["sampleInterval"][-1]))
        self.alarmValue.setText(para["alarmValue"])
        #self.alarm.setText(para["alarm"])
        #hand value : 1 or 2,and handComboBox starts from ZERO
        self.handComboBox.setCurrentIndex(int(para["hand"])-1)
        
        self.co2concentration.display(realTimeStatus["co2concentration"])
        self.temperature_c.display(realTimeStatus["temperature"])
        self.temperature_f.display(realTimeStatus["temperature_f"])
        self.humidity.display(realTimeStatus["humidity"])
        self.pressure.display(realTimeStatus["pressure"])
       
        # set the dir tree related parameter 
        self.dirModel = QtGui.QDirModel(self.fileOperBox)
        #self.dirModel = QtGui.QFileSystemModel(self.fileOperBox)
        self.dirTreeView.setModel(self.dirModel)
        self.dirTreeView.setRootIndex(self.dirModel.index(".\\data"))
        self.fileOperBox.show()
        

        #set default para in recordrangeBox
        self.beginDateEdit.setDate(QtCore.QDate.currentDate())
        self.afterDateEdit.setDate(QtCore.QDate.currentDate())
        
        qPicCo2 = QtGui.QPixmap('image/co2Line.PNG')
        self.co2Line.setPixmap(qPicCo2)
        qPicTemp = QtGui.QPixmap('image/tempLine.PNG')
        self.tempLine.setPixmap(qPicTemp)
        qPicHum = QtGui.QPixmap('image/humLine.PNG')
        self.humLine.setPixmap(qPicHum)
        qPicAtmo = QtGui.QPixmap('image/atmoLine.PNG')
        self.atmoLine.setPixmap(qPicAtmo)
        qPicBatt = QtGui.QPixmap('image/battLine.PNG')
        self.battLine.setPixmap(qPicBatt)

    def closeAll(self):
        self.tabWidget.setCurrentIndex(1)
        #time.sleep(1)
        self.CTH.close()
        

    def controllorUi(self):
        QtCore.QObject.connect(self.exitAct, QtCore.SIGNAL(_fromUtf8("triggered()")), self.closeAll)
        QtCore.QObject.connect(self.CTH, QtCore.SIGNAL(_fromUtf8("destroyed()")), self.closeAll)

        self.updateTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.updateTimer, QtCore.SIGNAL(_fromUtf8("timeout()")), self.updateStatus)
        self.updateTimer.start(2000)
        
        #set dir path button 
        #delete the button now  Jun 2
        #QtCore.QObject.connect(self.setDirPath, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openDirPath)
        
        #transfer original file 
        QtCore.QObject.connect(self.tranferFileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.tranOrigFile)
        
        #set refresh clock button 
        QtCore.QObject.connect(self.calibrationClockButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.showCalibrationClock)
        QtCore.QObject.connect(self.updatePara, QtCore.SIGNAL(_fromUtf8("clicked()")), self.updateParaFunc)
        
        #co2CheckBox change 
        QtCore.QObject.connect(self.co2CheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), self.reDrawCurve)
        QtCore.QObject.connect(self.tempCheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), self.reDrawCurve)
        QtCore.QObject.connect(self.humiCheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), self.reDrawCurve)
        QtCore.QObject.connect(self.atmospheriCheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), self.reDrawCurve)
        QtCore.QObject.connect(self.batteryCheckBox, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), self.reDrawCurve)
        
        #load into file
        QtCore.QObject.connect(self.loadinFileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openFile)
        QtCore.QObject.connect(self.dirTreeView, QtCore.SIGNAL(_fromUtf8("pressed(QModelIndex)")), self.pressPrint)
        #QtCore.QMetaObject.connectSlotsByName(CTH)
        
        QtCore.QObject.connect(self.aboutAct, QtCore.SIGNAL(_fromUtf8("triggered()")), self.openAboutDialog)
        QtCore.QObject.connect(self.helpAct, QtCore.SIGNAL(_fromUtf8("triggered()")), self.openHelpDialog)
        
        #get dir's info
        QtCore.QObject.connect(self.refreshFiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getDirsInfo)
        
        QtCore.QObject.connect(self.receiveFiles, QtCore.SIGNAL(_fromUtf8("clicked()")), self.getFiles)
        QtCore.QObject.connect(self.deleteFileButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.deleteFiles)

        # stop record
        QtCore.QObject.connect(self.stopRecord, QtCore.SIGNAL(_fromUtf8("clicked()")), self.stopRecordFunc)

        QtCore.QObject.connect(self.queryButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.queryRecord)

    '''
    def receiveFile(self):
        self.receiveFileDialog = QtGui.QDialog()
        self.ui_receiveFileDialog = Ui_ReceiveFileDialog()
        self.ui_receiveFileDialog.setupUi(self.receiveFileDialog)
        self.ui_receiveFileDialog.receiveFileProgressBar.setProperty("value", 0)
        QtCore.QObject.connect(self.ui_receiveFileDialog.receiveFileProgressBar, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.valueC)
        sys.exit(self.receiveFileDialog.exec_())

    def valueC(self,v):
        #self.ui_receiveFileDialog.receiveFileProgressBar.setValue(v)
        print('ba')
    '''
    
    def getFiles(self):
        '''
        one = QtGui.QTableWidgetItem()
        one.setText('Jan')
        one.setCheckState(QtCore.Qt.Checked)
        
        howto use it in signal: 
        first , travel the QTableWidget and find QTableWidgetItem, takeItem()
        QTableWidgetItem.checkState() will return the checked state of the table item
        QtCore.Qt.Unchecked
        QtCore.Qt.Checked
        '''
        rowCnt = self.fileOperTableWidget.rowCount()
        getFilesName = list()
        for i in range(rowCnt):
            fileNameItem = self.fileOperTableWidget.takeItem(i,0)
            if QtCore.Qt.Checked == fileNameItem.checkState():
                getFilesName.append(fileNameItem.text())
        #getFilesFlag = False
        #filesName = list()
        getFilesFlag,filesName = self.commu.getFiles(getFilesName)
        if 1 == en_version:
            if True == getFilesFlag:
                if 0 == len(filesName):
                    info = 'Disconnect downSite board\n'
                else:
                    info = 'Completed get files:\n' + '\n'.join(filesName)
                self.returnInfoDisplay(info)
            else:
                info = 'failed to get files below:\n' + '\n'.join(filesName)
                self.returnInfoDisplay(info)
        else:
            if True == getFilesFlag:
                if 0 == len(filesName):
                    info = '无法连接到下位机!\n'
                else:
                    info = '已经获取了如下文件:\n' + '\n'.join(filesName)
                self.returnInfoDisplay(info)
            else:
                info = '未能成功获取以下文件:\n' + '\n'.join(filesName)
                self.returnInfoDisplay(info)
        self.getDirsInfo()
        # set false will cause re-paint the dir tree content
        self.index2Flag = False
        
    def deleteFiles(self):
        rowCnt = self.fileOperTableWidget.rowCount()
        getFilesName = list()
        for i in range(rowCnt):
            fileNameItem = self.fileOperTableWidget.takeItem(i,0)
            if QtCore.Qt.Checked == fileNameItem.checkState():
                getFilesName.append(fileNameItem.text())
        if 1 == en_version:
            if True == self.commu.deleteFiles(getFilesName):
                if 0 == len(getFilesName):
                    self.returnInfoDisplay("Disconnect downSite board\n")
                else:
                    self.returnInfoDisplay("Delete files Success！")
            else:
                self.returnInfoDisplay("Delete some files failed！Please refresh dir and re-delete them")
        else:
            if True == self.commu.deleteFiles(getFilesName):
                if 0 == len(getFilesName):
                    self.returnInfoDisplay("无法连接到下位机!\n")
                else:
                    self.returnInfoDisplay("删除文件成功！")
            else:
                self.returnInfoDisplay("部分文件删除失败！请刷新目录之后重新选择仍未删除的文件进行删除")
            
        self.getDirsInfo()
        
    def getDirsInfo(self):
        dirsInfo = self.commu.getDirs()
        self.fileOperTableWidget.clearContents()
        rowCnt = self.fileOperTableWidget.rowCount()
        for i in range(len(dirsInfo)):
            if 'SYS.TXT' == dirsInfo[i]['fileName']:
                dirsInfo.pop(i)
                break
        for i in range(len(dirsInfo)):
            if i < rowCnt :
                pass
            else:
                self.fileOperTableWidget.insertRow(i)
            fileName = QtGui.QTableWidgetItem()
            fileName.setText(dirsInfo[i]['fileName'])
            fileName.setCheckState(QtCore.Qt.Unchecked)
            self.fileOperTableWidget.setItem(i,0,fileName)
            self.fileOperTableWidget.setItem(i,1,QtGui.QTableWidgetItem(dirsInfo[i]['fileSize']))
            self.fileOperTableWidget.setItem(i,2,QtGui.QTableWidgetItem(dirsInfo[i]['fileUpdateTime']))
        while len(dirsInfo) < rowCnt:
            self.fileOperTableWidget.removeRow(rowCnt-1)
            rowCnt = self.fileOperTableWidget.rowCount()
        self.fileOperTableWidget.show()
        
    '''
    def openHelpDialogThread(self):
        helpDialogThread = threading.Thread(target = self.openHelpDialog)
        helpDialogThread.start()
    '''
    def openHelpDialog(self):
        HelpDialog = QtGui.QDialog()
        ui = Ui_HelpDialog()
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.logoPath),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        HelpDialog.setWindowIcon(icon)
        '''
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        '''
        ui.setupUi(HelpDialog)
        HelpDialog.show()
        HelpDialog.exec_()

    def openAboutDialog(self):
        AboutDialog = QtGui.QDialog()
        ui_aboutDialog = Ui_AboutDialog()
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.logoPath),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        '''
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        '''
        ui_aboutDialog.setupUi(AboutDialog)
        AboutDialog.exec_()
    
    def pressPrint(self,modelIndex):
        self.selectFileModelIndex = modelIndex
        
    def openFile(self):
        self.filePath = self.dirModel.filePath(self.selectFileModelIndex)
        self.index2Flag = False
        
    def getInitStatus(self):
        '''including para and real time status'''
        if self.commu.connectStatus():
            self.statusBar.showMessage('USB CONNECTED')
            realTimeStatus,self.recordCnt = self.commu.getRealTimeStatus()
            para = self.commu.getPara()
            self.connectFlag = True
            return realTimeStatus,para,True
        else:
            self.statusBar.showMessage('USB DISCONNECTED,RECONNECTING ...')
            return '','',False
        
    def updateStatus(self):
        if self.commu.connectStatus():
            if 0 == self.recordCnt or 1 == self.tabWidget.currentIndex() or 2 == self.tabWidget.currentIndex():
                self.statusBar.showMessage('USB CONNECTED')
            self.connectFlag = True
        else:
            #print('connecting ...')
            self.commu.reConnectDevice()
            self.statusBar.showMessage('USB DISCONNECTED,RECONNECTING ...')
            self.connectFlag = False

        if True == self.connectFlag and 0 == self.tabWidget.currentIndex():
            realTimeStatus,self.recordCnt = self.commu.getRealTimeStatus()
            #print('update realTime : ',realTimeStatus)
            
            if 1 == en_version:
                if 0 != self.recordCnt:
                    self.statusBar.showMessage('USB CONNECTED,AND RECORDING %.2f%%' %(100*self.recordCnt/int(self.para["recordTime"]),))
            else:
                if 0 != self.recordCnt:
                    self.statusBar.showMessage('USB CONNECTED,AND RECORDING %.2f%%' %(100*self.recordCnt/int(self.para["recordTime"]),))

            self.co2concentration.display(str(int(realTimeStatus['co2concentration'])))
            self.temperature_c.display(realTimeStatus['temperature'])
            self.temperature_f.display(realTimeStatus['temperature_f'])
            self.humidity.display(realTimeStatus['humidity'])
            self.pressure.display(realTimeStatus['pressure'])
            self.index2Flag = False
            
            
        elif 1 == self.tabWidget.currentIndex() and False == self.index1Flag:
            self.getDirsInfo()
            self.index1Flag = True
            
        elif 2 == self.tabWidget.currentIndex() and False == self.index2Flag: 
            #self.dirModel.index(".\\data")
            self.dirModel.refresh()
            if True == self.reDrawCurveFlag:
                self.drawCurve()
                self.reDrawCurveFlag = False
            else:
                self.readAtrFile(self.filePath)
                self.setDisplayDetailInfoTableWidget()
                self.drawCurve()
            self.index2Flag = True
        
    def showCalibrationClock(self):
        if self.connectFlag:
            self.calibrationClock = QtGui.QDialog()
            self.ui_calibrationClock = Ui_calibrationClockDialog()
            self.ui_calibrationClock.setupUi(self.calibrationClock)
            
            self.ui_calibrationClock.actualTime.setDateTime(QtCore.QDateTime.currentDateTime())
            
            downSiteClock = self.commu.getClock()

            #print(downSiteClock)
            #yyyy/M/d H:mm:ss
            self.ui_calibrationClock.downSiteTime.setDateTime(QtCore.QDateTime.fromString(downSiteClock, "yyyy/MM/dd HH:mm:ss"))
            
            #set downSite clock  time right
            QtCore.QObject.connect(self.ui_calibrationClock.setTimerButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.setClockTime)
            
            #use show() will crash(close immediately , Jan 10 by lidatong
            self.calibrationClock.exec_()
        else:
            self.returnInfoDisplay('Disconnect downSite and can\'t get clock')
    
    def setClockTime(self):
        clockTime = self.ui_calibrationClock.actualTime.dateTime().toString( "yyyy/MM/dd HH:mm:ss")
        self.commu.setClock(clockTime)
        #print("clockTime is %s" %clockTime)
        self.calibrationClock.close()

    # transfer the orignal file (which wirte as ord num) to readable file
    def tranOrigFile(self):
        filePath = QtGui.QFileDialog.getOpenFileName(self.tabWidget, "Open File",QtCore.QDir.currentPath())
        content = str()
        byteList = list()
        if '' == filePath:
            return
        with open(filePath,'rb') as f:
            byte = f.read(1)
            while byte:
                byteList.append(ord(byte))
                byte = f.read(1)
        content = self.commu.file2Content(byteList)
        if False == content:
            self.returnInfoDisplay("translate %s failed!" %(filePath,))
        fileName =  './data/' +  filePath.split('/')[-1]
        with open(fileName,'w') as f:
            f.write(content)
        self.returnInfoDisplay("translate %s success!" %(filePath,))
        # set false will cause re-paint the dir tree content
        self.index2Flag = False

    def openDirPath(self):
        dirPath = QtGui.QFileDialog.getExistingDirectory(self.fileOperBox, "Open Dir",QtCore.QDir.currentPath())
        if dirPath != "":
            self.dirTreeView.setRootIndex(self.dirModel.index(dirPath))

    def sampleIntervalUnit2Index(self,unit):
        if 'S' == unit:
            return 0
        elif 'M' == unit:
            return 1
        elif 'H' == unit:
            return 2

    def index2SampleIntervalUnit(self,index):
        if 0 == index:
            return 'S'
        elif 1 == index:
            return 'M'
        elif 2 == index:
            return 'H'
    
    def returnInfoDisplay(self,info):
        self.returnInfoDialog = QtGui.QDialog()
        self.ui_returnInfoDialog = Ui_returnInfoDialog()
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.logoPath),QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.returnInfoDialog.setWindowIcon(icon)
        '''
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        '''
        self.ui_returnInfoDialog.setupUi(self.returnInfoDialog)
        self.ui_returnInfoDialog.result.setText(info)
        self.returnInfoDialog.exec_()
    
    #get Para from the UI and set para to downSite
    def updateParaFunc(self):
        if self.connectFlag:
            self.para['num'] = self.num.text()
            self.para['name'] = self.name.text()
            self.para['recordTime'] = self.recordTime.text()
            self.para['sampleInterval'] = self.sampleInterval.text() + self.index2SampleIntervalUnit(self.sampleInvBox.currentIndex())
            self.para['alarmValue'] = self.alarmValue.text()
            self.para['alarm'] = '01'
            #self.para['hand'] = self.hand.text()
            # hand : 1 or 2
            self.para['hand'] = str(self.handComboBox.currentIndex()+1)
            #print(self.para)
            if 1 == en_version:
                if True == self.commu.setPara(self.para):
                    self.returnInfoDisplay("Parameter set success！")
                else:
                    self.returnInfoDisplay("Parameter set failed！")
            else:
                if True == self.commu.setPara(self.para):
                    self.returnInfoDisplay("参数设置成功！")
                else:
                    self.returnInfoDisplay("参数设置失败！")
            self.index1Flag = False
        else:
            self.returnInfoDisplay('Disconnect downSite and can\'t set parameters')

    def stopRecordFunc(self):
        if 1 == en_version:
            if True == self.commu.stopRecord():
                self.returnInfoDisplay("Stop record success！")
            else:
                self.returnInfoDisplay("Stop record failed！")
        else:
            if True == self.commu.stopRecord():
                self.returnInfoDisplay("停止记录成功！")
            else:
                self.returnInfoDisplay("停止记录失败！")

    def setDisplayDetailInfoTableWidget(self):
        '''
        one = QtGui.QTableWidgetItem()
        one.setText('Jan')
        one.setCheckState(QtCore.Qt.Checked)
        '''
        self.displayDetailInfoTableWidget.clearContents()
        rowCnt = self.displayDetailInfoTableWidget.rowCount()
        for i in range(len(self.co2)):
            if i < rowCnt :
                pass
            else:
                self.displayDetailInfoTableWidget.insertRow(i)
            self.displayDetailInfoTableWidget.setItem(i,0,QtGui.QTableWidgetItem(self.dt[i]))
            self.displayDetailInfoTableWidget.setItem(i,1,QtGui.QTableWidgetItem(str(int(self.co2[i]))))
            self.displayDetailInfoTableWidget.setItem(i,2,QtGui.QTableWidgetItem(self.temp[i]))
            self.displayDetailInfoTableWidget.setItem(i,3,QtGui.QTableWidgetItem(self.humi[i]))
            self.displayDetailInfoTableWidget.setItem(i,4,QtGui.QTableWidgetItem(self.pres[i]))
            self.displayDetailInfoTableWidget.setItem(i,5,QtGui.QTableWidgetItem(self.batt[i]))
        while len(self.co2) < rowCnt:
            self.displayDetailInfoTableWidget.removeRow(rowCnt-1)
            rowCnt = self.displayDetailInfoTableWidget.rowCount()
        self.displayDetailInfoTableWidget.show()

    def readAtrFile(self, filePath):
        self.dt.clear()
        self.co2.clear()
        self.temp.clear()
        self.humi.clear()
        self.pres.clear()
        self.batt.clear()
        with open(filePath,'r') as atrFile:
            lines = atrFile.readlines()
        i = 0
        for line in lines:
            i += 1
            if i == 1:
                continue
            ls = line.strip().split('\t')
            self.dt.append(ls[0])
            #self.dt.append(i)
            #timeArray = time.strptime(ls[0], "%Y/%m/%d %H:%M:%S")
            #self.dt.append(int(time.mktime(timeArray)))
            self.co2.append(ls[1])
            self.temp.append(ls[2])
            self.humi.append(ls[3])
            self.pres.append(ls[4])
            self.batt.append(ls[5])
        #print(self.dt)

    def queryRecord(self):
        self.readAtrFile(self.filePath)
        dataArray = [time.mktime(time.strptime(d, "%Y/%m/%d %H:%M:%S")) for d in self.dt]
        #print(dataArray)
        if self.alldateRadioButton.isChecked() == True:
            self.drawCurve()
        if self.beforedayRadioButton.isChecked() == True:
            #print(self.beforeDayBox.value())
            days = self.beforeDayBox.value()
            wholeTime = days*24*60*60
            if wholeTime != 0:
                for i in range(len(dataArray)-1):
                    if dataArray[-1] - dataArray[i] <= wholeTime:
                        break
                self.dt = self.dt[i:-1]
                self.co2 = self.co2[i:-1]
                self.temp = self.temp[i:-1]
                self.humi = self.humi[i:-1]
                self.pres = self.pres[i:-1]
                self.batt = self.batt[i:-1]
            else:
                pass
            self.drawCurve()
        if self.beforeMonthRadioButton.isChecked() == True:
            #print(self.beforeMonthBox.value())
            months = self.beforeMonthBox.value()
            wholeTime = months*24*60*60*30
            if wholeTime != 0:
                for i in range(len(dataArray)-1):
                    if dataArray[-1] - dataArray[i] <= wholeTime:
                        break
                self.dt = self.dt[i:-1]
                self.co2 = self.co2[i:-1]
                self.temp = self.temp[i:-1]
                self.humi = self.humi[i:-1]
                self.pres = self.pres[i:-1]
                self.batt = self.batt[i:-1]
            else:
                pass
            self.drawCurve()
        if self.radioButton.isChecked() == True:
            pass
            #print('radioButton')
        #print('query end')

    def printScreen(self):
        for s in self.str:
            pass
            #print(s + " ")
        self.str = []
        
    def reDrawCurve(self):
        self.reDrawCurveFlag = True
        self.index2Flag = False
        
    def drawCurve(self):
        while False == self.drawCurveLayout.isEmpty():
             it = self.drawCurveLayout.itemAt(0)
             self.drawCurveLayout.removeItem(it)
        axis = DateAxis(orientation='bottom')
        vb = CustomViewBox()
        pw = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=False, title="plot figure")
        #pw = pg.PlotWidget(enableMenu=False, axisItems={'bottom': axis}, title="plot figure")
        dataArray = [time.mktime(time.strptime(d, "%Y/%m/%d %H:%M:%S")) for d in self.dt]
        dates = np.array(dataArray,dtype=np.int32)
        '''
        Symbol to use for drawing points OR list of symbols, one per point. Default is no symbol. Options are o, s, t, d, +, or any QPainterPath
        '''
        if QtCore.Qt.Checked == self.co2CheckBox.checkState():
            pw.plot(x=dates, y=np.array(self.co2,dtype=np.int16), pen=(255,0,0), symbol='t')  #red
        if QtCore.Qt.Checked == self.tempCheckBox.checkState():
            pw.plot(x=dates, y=np.array(self.temp,dtype=np.float16), pen=(0,255,0), symbol='+')  #blue
        if QtCore.Qt.Checked == self.humiCheckBox.checkState():
            pw.plot(x=dates, y=np.array(self.humi,dtype=np.float16), pen=(0,0,255), symbol='d') #green
        if QtCore.Qt.Checked == self.atmospheriCheckBox.checkState():
            pw.plot(x=dates, y=np.array(self.pres,dtype=np.float16), pen=(255,0,255), symbol='s')
        if QtCore.Qt.Checked == self.batteryCheckBox.checkState():
            pw.plot(x=dates, y=np.array(self.batt,dtype=np.float16), pen=(255,255,0), symbol='o')
        self.drawCurveLayout.addWidget(pw)

class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        strns = []
        '''
        rng = max(values)-min(values)
        #if rng < 120:
        #    return pg.AxisItem.tickStrings(self, values, scale, spacing)
        if rng < 3600*24:
            string = '%H:%M:%S'
            label1 = '%b %d -'
            label2 = ' %b %d, %Y'
        elif rng >= 3600*24 and rng < 3600*24*30:
            string = '%d'
            label1 = '%b - '
            label2 = '%b, %Y'
        elif rng >= 3600*24*30 and rng < 3600*24*30*24:
            string = '%b'
            label1 = '%Y -'
            label2 = ' %Y'
        elif rng >=3600*24*30*24:
            string = '%Y'
            label1 = ''
            label2 = ''
        '''
        for x in values:
            try:
                #strns.append(time.strftime(string,time.localtime(x)))
                #print(x)
                #print(time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(x)))
                strns.append(time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
        '''
        try:
            label = time.strftime(label1, time.localtime(min(values)))+time.strftime(label2, time.localtime(max(values)))
        except ValueError:
            label = ''
        '''
        #self.setLabel(text=label)
        return strns

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.setMouseMode(self.RectMode)
        
    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            self.autoRange()
            
    def mouseDragEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton:
            ev.ignore()
        else:
            pg.ViewBox.mouseDragEvent(self, ev)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CTH = QtGui.QMainWindow()
    
    VID_CAPAC = 0x0483
    PID_CAPAC = 0x5750
    ui = Ctrl_Ui_CTH(VID_CAPAC, PID_CAPAC)
    para = {"num":"999999","name":"CTHXXX", "recordTime":"999", "sampleInterval":"99S", "alarmValue":"9999","alarm":"3", "hand":"1" }
    status = {"co2concentration":"999","temperature":"-99","temperature_f":"9999","humidity":"99","pressure":"100"}
    ui.setupUi(CTH, status, para)
    ui.controllorUi()
    #ui.setDisplayDetailInfoTableWidget()
    #ui.drawCurve()
    CTH.show()
    sys.exit(app.exec_())
    #sys.exit(0)
