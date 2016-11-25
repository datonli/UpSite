# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace\UpSite\ParaSetting.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

# Translate 璐熻矗ASCII鐮侊紙Unicode锛夊拰HEX锛�16杩涘埗锛変箣闂寸殑杞崲
# 涓嶅垽鏂寚浠ょ殑鎰忎箟锛屼笉娑夊強鎸囦护鏄粈涔堟寚浠わ紝鍥犱负瀵规瘡涓寚浠ら兘瑕佽繘琛岀炕璇�
# 杩樿涓€涓噸瑕佺殑鑱岃矗鏄細淇濊瘉浼犺緭鐨勬暟鎹畬鏁存€у拰姝ｇ‘鎬�
# 

import time
from .Para import Para

class Translate(object):
    def __init__(self):
        pass

    def dataList2Str(self, dataList):
        if len(dataList) > 64:
            #print('Error in str2dataList')
            return
        s = ''
        for i in range(len(dataList)):
            if i < 6:
                s += chr(dataList[i])
            else:
                tmpS = str(dataList[i])
                if len(tmpS) == 1:
                    tmpS = '0'  + tmpS
                s += tmpS
        return s	

    def str2dataList(self, s):
        cnt = len(s)
        if cnt > 122:
            #print('Error in str2dataList')
            return
        elif cnt < 122:
            for i in range(122 - cnt):
                s += '0'

        dataList = []
        for c in s[0:6]:
            dataList.append(ord(c))
        for d in range(6, len(s), 2):
            dataList.append(int(s[d:d+2]))
        return dataList

    ''' "20110312193355" to "2011/03/12 19:33:55" '''
    def str2ClockStr(self,s):
        year = s[0:4]
        month = s[4:6]
        day = s[6:8]
        hour = s[8:10]
        minute = s[10:12]
        second = s[12:14]
        return "{YY}/{MM}/{DD} {HH}:{mm}:{ss}".format(YY = year,MM = month,DD = day,HH = hour,mm = minute,ss = second)

    ''' "2011/03/12 19:33:55" to "20110312193355" '''
    def clockStr2Str(self,s):
        dateTime = s.split(' ')
        date = dateTime[0].split('/')
        year = date[0]
        month = date[1]
        day = date[2]

        time = dateTime[1].split(':')
        hour = time[0]
        minute = time[1]
        second = time[2]

        return "{YY}{MM}{DD}{HH}{mm}{ss}".format(YY = year,MM = month,DD = day,HH = hour,mm = minute,ss = second)

    def _getRealTimeStatusFromDataList(self,dataList):
        status = {}
        h_co2 = str(dataList[0])
        if 1 == len(h_co2):
            h_co2 = '0' + h_co2
        l_co2 = str(dataList[1])
        if 1 == len(l_co2):
            l_co2 = '0' + l_co2
        co2 = h_co2 + l_co2
        status['co2concentration'] = co2
        status['temperature'] = ''
        if 'N' == chr(dataList[2]):
            status['temperature'] = '-'
        status['temperature'] += str(dataList[3]) + '.' + str(dataList[4])
        status['temperature_f'] = str(round((float(status['temperature'])*1.8 + 32),1))
        status['humidity'] = str(dataList[5]) + '.' + str(dataList[6])
        
        '''
        Apr. 3,add this code for adding status bar about recording time when record,
        it's ugly because QinShou use real time datalist 7-10 bytes as record count  
        '''
        if len(dataList) > 7:
            recordCnt = dataList[7]*1000000 + dataList[8]*1000 + dataList[9]*100 + dataList[10]
            return status,recordCnt
        else:
            return status

    def getRealTimeStatusFromDataList(self,dataList):
        status = {}
        status['humidity'] = str((dataList[0]+(dataList[1]&0xC0)*4)/10)
        status['co2concentration'] = str((dataList[1]&0x3F)*256+dataList[2])
        status['temperature'] = ''
        if 1 == dataList[3]&0x80:
            status['temperature'] = '-'
        status['temperature'] += str(dataList[3]&0x7F) + '.' + str(dataList[4])
        status['temperature_f'] = str(round((float(status['temperature'])*1.8 + 32),1))
        status['pressure'] = dataList[5]+4*(dataList[6]&0xC0)+124
        status['battery'] = (dataList[6]&0x3F)*0.025+5
        
        if len(dataList) > 7:
            recordCnt = dataList[7]*1000000 + dataList[8]*1000 + dataList[9]*100 + dataList[10]
            return status,recordCnt
        else:
            return status

    def dirsInfoTranslate(self, dataList):
        fileInfo = dict()
        fileName = str()
        fileSize = str()
        fileUpdateTime = str()
        for d in dataList[10:22]:
            c = chr(d)
            if c != '#':
                fileName += c 
        fileSize = str(dataList[22]*1000000 + dataList[23]*10000 + dataList[24]*100 + dataList[25])
        fileUpdateTime = str(dataList[26]*100+dataList[27]) + '/' + str(dataList[28]) + '/' + str(dataList[29]) + ' ' + \
        str(dataList[30]) + ':' + str(dataList[31]) + ':' + str(dataList[32])
        fileInfo['fileName'] = fileName
        fileInfo['fileSize'] = fileSize
        fileInfo['fileUpdateTime'] = fileUpdateTime
        return fileInfo

    def fileInfoTranslate(self, dataList):
        fileInfo = dict()
        fileName = str()
        fileSize = str()
        fileCreateTime = str()
        fileUpdateTime = str()
        for d in dataList[0:12]:
            c = chr(d)
            if c != '#':
                fileName += c 
        #print(fileName)
        fileSize = str(dataList[12]*1000000 + dataList[13]*10000 + dataList[14]*100 + dataList[15])
        fileCreateTime = str(dataList[16]*100+dataList[17]) + '/' + str(dataList[18]) + '/' + str(dataList[19]) + ' ' + \
        str(dataList[20]) + ':' + str(dataList[21]) + ':' + str(dataList[22])
        fileUpdateTime = str(dataList[23]*100+dataList[24]) + '/' + str(dataList[25]) + '/' + str(dataList[26]) + ' ' + \
        str(dataList[27]) + ':' + str(dataList[28]) + ':' + str(dataList[29])
        fileInfo['fileName'] = fileName
        fileInfo['fileSize'] = fileSize
        fileInfo['fileCreateTime'] = fileCreateTime
        fileInfo['fileUpdateTime'] = fileUpdateTime
        return fileInfo

    def fileTranslate(self, bytesList):
        '''
        fileInfo block : bytesList[0]
        data block : bytesList[1:]
        translate to:
        fileName\tfileSize\tfileCreateTime\tfileUpdateTime\tnum\tname\trecordTime\tsampleInterval\talarmValue\talarm\thand\n
        dateTime\tco2concentration\ttemperature\thumidity\n
                                .
                                .
                                .
        dateTime\tco2concentration\ttemperature\thumidity\n
        '''
        '''
        #print('header is',bytesList[:64])
        bytesList[20] = 20
        bytesList[21] = 11
        bytesList[23] = 11
        '''
        
        content = str()
        #get file info
        fileInfo = self.fileInfoTranslate(bytesList[4:34])
        para = Para()
        if False == para.getParaFromDataList(bytesList[34:60]):
            return False
        paraDict = para.paraDict()
        content += "{fileName}\t{fileSize}\t{fileCreateTime}\t{fileUpdateTime}\t{num}\t{name}\t{recordTime}\t{sampleInterval}\t{alarmValue}\t{alarm}\t{hand}\n" \
        .format(fileName = fileInfo['fileName'],fileSize = fileInfo['fileSize'],fileCreateTime = fileInfo['fileCreateTime'],\
        fileUpdateTime = fileInfo['fileUpdateTime'],num = paraDict['num'],name = paraDict['name'],recordTime = paraDict['recordTime'],\
        sampleInterval = paraDict['sampleInterval'],alarmValue = paraDict['alarmValue'],alarm = paraDict['alarm'],hand = paraDict['hand'])
        
        fileCreateTime = fileInfo['fileCreateTime']
        sampleInterval = paraDict['sampleInterval']
        timeInterval = self.sampleInterval2TimeInterval(sampleInterval)
        timeStamp = self.fmtDateTime2TimeStamp(fileCreateTime)
        #get value
        #for block in bytesList[1:]:
        #block = bytesList[1:]
        cnt = 0
        
        for i in range(1,int(len(bytesList)/64)):
            block = bytesList[i*64:(i+1)*64]
            #print('%d bytes is %s' %(i,block))
            '''
            0:7
            7:14
            '''
            for j in range(int(len(block)/7) -1):
                timeStamp += timeInterval
                status = self.getRealTimeStatusFromDataList(block[7*j:7*(j+1)])
                cnt += 1
                if cnt <= int(paraDict['recordTime']):
                    content += "{dateTime}\t{co2concentration}\t{temperature}\t{humidity}\t{pressure}\t{battery}\n".format(dateTime = self.timeStamp2FmtDateTime(timeStamp), \
                    co2concentration = status['co2concentration'],temperature = status['temperature'],humidity =  status['humidity'],pressure =  status['pressure'],battery =  status['battery'])
        return content

    def sampleInterval2TimeInterval(self,sampleInterval):
        timeInterval = -1
        num = int(sampleInterval[:-1])
        unit = sampleInterval[-1]
        if 'S' == unit:
            timeInterval = num 
        elif 'M' == unit:
            timeInterval = num*60
        elif 'H' == unit:
            timeInterval = num*3600
        return timeInterval

    def fmtDateTime2TimeStamp(self,fmtDateTime):
        timeArray = time.strptime(fmtDateTime, "%Y/%m/%d %H:%M:%S")
        #print(timeArray)
        return int(time.mktime(timeArray))

    def timeStamp2FmtDateTime(self,timeStamp):
        timeArray = time.localtime(timeStamp)
        return time.strftime("%Y/%m/%d %H:%M:%S",timeArray)
        

    def _hexByte2Str(self, hexByte):
        return str(hexByte//16)+str(hexByte%16)

if __name__ == '__main__':
    tran = Translate()
    s = '20160114201855'
    clock = tran.str2ClockStr(s)
    print(clock)
    print(tran.clockStr2Str(clock))
    dataList = [30,0,78,30,60]
    print(tran.getRealTimeStatusFromDataList(dataList))