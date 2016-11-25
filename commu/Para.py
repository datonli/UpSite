# -*- coding: utf-8 -*-

class Para(object):
    def __init__(self,num = '',name = '',recordTime = '',sampleInterval = '',alarmValue = '',alarm = '',hand = ''):
        self.num = num
        self.name = name
        self.recordTime = recordTime
        self.sampleInterval = sampleInterval
        self.alarmValue = alarmValue
        self.alarm = alarm
        self.hand = hand
        self.paraDic = {}

    # 0003345454 #CTHGROUND 00001000 300000M 3000 01 01
    def getParaFromStr(self,str):
        self.num = str[0:10]
        self.name = str[10:19]
        self.recordTime = str[19:27]
        self.sampleInterval = str[27:34]
        self.alarmValue = str[34:38]
        self.alarm = str[38:40]
        self.hand = str[40:42]
        
    def paraDict(self):
        #self.num = self.num.zfill(10)
        self.paraDic['num'] = self.num
        self.paraDic['name'] = self.name
        self.paraDic['recordTime'] = self.recordTime
        self.paraDic['sampleInterval'] = self.sampleInterval
        self.paraDic['alarmValue'] = self.alarmValue
        self.paraDic['alarm'] = self.alarm
        self.paraDic['hand'] = self.hand
        return self.paraDic
        
    def printPara(self):
        paraStr = "num = {0},name = {1},recordTime = {2},sampleInterval = {3},alarmValue = {4},alarm = {5},hand = {6}"\
        .format(self.num,self.name,self.recordTime,self.sampleInterval,self.alarmValue,self.alarm,self.hand)
        #print(paraStr)
        
    def getChrFromBytes(self,bytes):
        s = ''
        for b in bytes: 
            bs = chr(b)
            if '#' != bs:
                s += bs
        return s
        
    def getStrFromBytes(self,bytes):
        s = ''
        for b in bytes:
            bs = str(b)
            if len(bs) == 1:
                bs = '0' + bs
            s += bs
        while '0' == s[0]:
            s = s[1:]
        return s
        
    def getParaFromDataList(self,dataList):
        try:
            self.num = self.getStrFromBytes(dataList[0:5])
            #self.num = self.num.zfill(10)
            
            self.name = self.getChrFromBytes(dataList[5:14])
            self.recordTime = self.getStrFromBytes(dataList[14:18])
            self.sampleInterval = self.getStrFromBytes(dataList[18:21]) + self.getChrFromBytes(dataList[21:22])
            self.alarmValue = self.getStrFromBytes(dataList[22:24])
            self.alarm = self.getStrFromBytes(dataList[24:25])
            self.hand = self.getStrFromBytes(dataList[25:26])
            return True
        except Exception as e:
            return False
        
    def getOrdFromStr(self,dataStr,cnt):
        dataList = []
        while cnt > len(dataStr):
            dataStr = '#' + dataStr
        for s in dataStr:
            dataList.append(ord(s))
        return dataList  
    
    def getIntFromStr(self,dataStr,cnt):
        dataList = []
        dataStr = dataStr.zfill(cnt)
        for i in range(cnt//2):
            dataList.append(int(dataStr[2*i:2*i+2]))
        return dataList
        
    def setPara2DataList(self):
        dataList = []
        dataList.extend(self.getIntFromStr(self.num,10))
        dataList.extend(self.getOrdFromStr(self.name,9))
        dataList.extend(self.getIntFromStr(self.recordTime,8))
        dataList.extend(self.getIntFromStr(self.sampleInterval[0:-1],6))
        dataList.extend(self.getOrdFromStr(self.sampleInterval[-1],1))
        dataList.extend(self.getIntFromStr(self.alarmValue,4))
        dataList.extend(self.getIntFromStr(self.alarm,2))
        dataList.extend(self.getIntFromStr(self.hand,2))
        return dataList
        
if __name__ == "__main__":
    para = Para()
    para.getParaFromStr("0300345454CTHGROUND00001000300000M30000101")
    para.printPara()
    dataList = para.setPara2DataList()
    print(dataList)
    para.getParaFromDataList(dataList)
    para.printPara()
    para.setPara2DataList()
    print(dataList)
    print(para.paraDict())