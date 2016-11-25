# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ui\UpSite.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

# 与Translate交互，得到可解析的指令或者数据（数据头带有特殊标号），分别进行解构1�7
# 此处有一个疑问？？？＄1�7
# USB的调动在这个函数，所以从USB传过来的数据是在这里接收的，如何让数据先经过Translate再到这个Commu呢？？？
# 应该让Commu之后在经过Translate
# 或者在Commu 中包含Translate class（组合）这个是比较合理的

from .HidDevice import HidDevice
#from .UsbDevice import UsbDevice
from .Translate import Translate
from .Para import Para

class Commu(object):
    def __init__(self, VID_CAPAC, PID_CAPAC):
        self.VID_CAPAC = VID_CAPAC
        self.PID_CAPAC = PID_CAPAC
        self.device = self._connect()
        self.device.start()
        self.tran = Translate()
    
    def _connect(self):
        return HidDevice(self.VID_CAPAC, self.PID_CAPAC)
        
    def _command(self, command):
        com = list()
        for c in command:
            com.append(ord(c))
        return com
        
    def _r_command(self, comDataList):
        com = str()
        for cdl in comDataList:
            com += chr(cdl)
        return com
        
    def _receiveData(self):
        return self.device.read()

    def _sendData(self, data):
        while len(data) < 64:
            data.append(0)
        if self.device != None:
            self.device.write(data)
            return True
        else:
            return False
    
    def connectStatus(self):
        command = 'COMCON'
        sendData = self._command(command)
        try:
            if self._sendData(sendData) == True:
                receiveData = self._receiveData()
                if self._r_command(receiveData[0:6]) == command:
                    #print(receiveData)
                    return True
        except Exception as err:
            #print('re connecting in con func')
            self.reConnectDevice()
        return False
    
    def makeSureConnected(self):
        while False == self.connectStatus():
            self.closeDevice()
            self._connect()
    
    def getRealTimeStatus(self):
        command = 'COMGRS'
        sendData = self._command(command)
        if self._sendData(sendData) == True:
            receiveData = self._receiveData()
            if self._r_command(receiveData[0:6]) == command:
                return self.tran.getRealTimeStatusFromDataList(receiveData[6:-1])
        else:
            return ''
    
    def setPara(self, para):
        #self.makeSureConnected()
        command = 'COMSPR'
        self.para = Para(para['num'],para['name'],para['recordTime'],para['sampleInterval'],\
        para['alarmValue'],para['alarm'],para['hand'])
        sendData = self._command(command)
        sendData.extend(self.para.setPara2DataList())
        if self._sendData(sendData) == True:
             receiveData = self._receiveData()
             if self._r_command(receiveData[0:6]) == command:
                return True
        return False
    
    def stopRecord(self):
        command = 'COMSTP'
        sendData = self._command(command)
        if self._sendData(sendData) == True:
            receiveData = self._receiveData()
            if self._r_command(receiveData[0:6]) == command:
                return True
        return False
    
    def getPara(self):
        #self.makeSureConnected()
        command = 'COMGPR'
        self.para = Para()
        sendData = self._command(command)
        if self._sendData(sendData) == True:
            receiveData = self._receiveData()
            if self._r_command(receiveData[0:6]) == command:
                self.para.getParaFromDataList(receiveData[6:-1])
                return self.para.paraDict()
        else:
            return ''

    def getClock(self):
        #self.makeSureConnected()
        command='COMGCL'
        sendData = self._command(command)
        if self._sendData(sendData) == True:
            receiveData = self._receiveData()
            if self._r_command(receiveData[0:6]) == command:
                clockStr = self.tran.dataList2Str(receiveData)
            return self.tran.str2ClockStr(clockStr[6:-1])
        else:
            return ''

    def setClock(self, clockTime):
        #self.makeSureConnected()
        #COMSCL20110312193355
        command = 'COMSCL'
        clockStr = self.tran.clockStr2Str(clockTime)
        data = self.tran.str2dataList(command + clockStr)
        if self._sendData(data) == True:
            receiveData = self._receiveData()
            return True
        else:
            return False
        
    def getDirs(self):
        command = 'COMGDR'
        sendData = self._command(command)
        dirsInfo = list()
        '''
        while False == self.device.q.empty():
            #print('block')
            pass
        '''
        if self._sendData(sendData) == True:
            receiveData = self._receiveData()
            cnt = 0
            data = list()
            if self._r_command(receiveData[0:6]) == command:
                cnt = receiveData[6]*100 + receiveData[7]
            while cnt != 0:
                try:
                    receiveData = self.device.q.get(timeout = 120)   # 120s 超时
                except Exception as err:
                    #print('timeout')
                    return False
                if self._r_command(receiveData[0:6]) == command:
                    data.append(receiveData)
                    cnt -= 1
        for d in data:
            sd = self.tran.dirsInfoTranslate(d)
            dirsInfo.append(sd)
        return dirsInfo    

    def getFiles(self, filesName):
        info = list()
        for fileName in filesName:
            while False == self._getFile(fileName):
                #print('get',fileName,'failed,please re-get it')
                info.append(fileName)
        if 0 != len(info):
            return False,info
        else:
            return True,filesName
            
    def _getFile(self,fileName):
        command = 'COMGFL'
        FFLCommand = 'FFL'  #标志文件信息块
        DFLCommand = 'DFL'  #标志数据信息块
        getFileName = fileName
        #fileInfo = dict()
        sendData = self._command(command)
        '''
        if len(fileName) < 12:
            fileName = '#' + fileName
        '''
        fileNameDataList = list()
        for fn in fileName[:-4]:
            fileNameDataList.append(ord(fn))
        sendData.extend(fileNameDataList)
        
        while not self.device.q.empty():
            self.device.q.get()
            #pass
            #print('empty the queue ',self.device.q.get())
        
        if self._sendData(sendData) == True:
            cnt = 0
            data = list()
            while True:
                receiveData = self.device.q.get()
                if self._r_command(receiveData[61:64]) == FFLCommand:
                    cnt = receiveData[0]*1000000 + receiveData[1]*10000 + receiveData[2]*100 + receiveData[3]
                    data.extend(receiveData)
                    break
            '''
            while True:
                receiveData = self._receiveData()
                if self._r_command(receiveData[61:64]) == FFLCommand:
                    cnt = receiveData[0]*1000000 + receiveData[1]*10000 + receiveData[2]*100 + receiveData[3]
                    #fileInfo = self.tran.getFileInfoFromFFLBlock(receiveData)
                    data.extend(receiveData)
                    break
            '''
            '''
            receiveData = self._receiveData()
            #print('recv data is ',receiveData)
            if self._r_command(receiveData[61:64]) == FFLCommand:
                cnt = receiveData[0]*1000000 + receiveData[1]*10000 + receiveData[2]*100 + receiveData[3]
            '''
            count = 0
            
            flags = []
            while count < cnt:
                count += 1
                flags.append(0)
            count = 0
            while cnt != 0:
                try:
                    receiveData = self.device.q.get(timeout = 10)   # 120s 超时
                    count += 1
                    #print('%d data is %s' %(count,receiveData))
                except Exception as err:
                    break
                    return False
                if self._r_command(receiveData[61:64]) == DFLCommand:
                    data.extend(receiveData)
                    order = receiveData[-5] + receiveData[-6] * 100 + receiveData[-7] * 10000 + receiveData[-8] * 1000000
                    flags[order-1]  = 1
                    cnt -= 1
        self._verifyData(flags,data,getFileName)
        #print(data)
        content = self.file2Content(data)
        #print(content)
        self._write2Disk(getFileName,content)
        return True
        
    def deleteFiles(self, filesName):
        for fileName in filesName:
            flag = self._deleteFile(fileName)
            if False == flag:
                #print('delete ',fileName,' failed,please re-delete it')
                return False
        return True
        
    def _deleteFile(self, fileName):
        command = 'COMFDE'
        getFileName = fileName
        #fileInfo = dict()
        sendData = self._command(command)
        
        fileNameDataList = list()
        for fn in fileName[:-4]:
            fileNameDataList.append(ord(fn))
        sendData.extend(fileNameDataList)
        if self._sendData(sendData) == True:
            import time
            time.sleep(0.05)
            receiveData = self._receiveData()
            for i in range(len(sendData)):
                if sendData[i] != receiveData[i]:  
                    return False
            return True
        
    def file2Content(self,data):
        try:
            return self.tran.fileTranslate(data)
        except Exception as e:
            return False
        
    def _verifyData(self,flags,data,fileName):
        lack_order = []
        for i in range(len(flags)):
            if 0 == flags[i]:
                lack_order.append(i)
        #print('lack part order ',lack_order)
        pass
        
    def _write2Disk(self,fileName,content):
        fileName = '.\\data\\' + fileName
        with open(fileName,'w') as f:
            f.write(content)

    def getByteBlock(self, fileName, seriesNumberDataList):
        command = 'COMGSN'
        DFLCommand = 'DFL'
        sendData = self._command(command)
        fileNameDataList = list()
        for fn in fileName:
            fileNameDataList += ord(fn)
        sendData.extend(fileNameDataList)
        sendData.extend(seriesNumberDataList)
        if self._sendData(sendData) == True:
            if self._r_command(receiveData[61:64]) == DFLCommand:
                return receiveData
    
    def reConnectDevice(self):
        self.device.stop()
        self.device = self._connect()
        self.device.start()
    
    def checkDevice(self):
        if self.device == None:
            return False
        else:
            return True
    
    def closeDevice(self):
        self.device.stop()

if __name__ == '__main__':
    VID_CAPAC = 0x0483
    PID_CAPAC = 0x5750
    com = Commu(VID_CAPAC, PID_CAPAC)
    print("get clock : %s " %com.getClock())
    com.setClock("2011/03/12 19:33:55")
    print("get clock : %s " %com.getClock())
    #sendlist = [0x01, 0x05, 0x01, 0x00, 0x00, 0x04, 0x02, 0x00, 0x06, 0xff, 0x10]
    #com.sendData(sendlist)
    #print(com.receiveData())
    com.closeDevice()