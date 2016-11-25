# -*- coding: utf-8 -*-

import pywinusb.hid as hid
from queue import Queue


class HidDevice(object):
    
    def __init__(self, vid, pid):
        self.alive = False
        self.device = None
        self.report = None
        self.vid = vid
        self.pid = pid
        self.recv_data = list()
        self.fileData = list()
        self.flag = False
        self.q = Queue()

    def start(self):
        _filter = hid.HidDeviceFilter(vendor_id = self.vid, product_id = self.pid)
        hid_device = _filter.get_devices()
        if len(hid_device) > 0:
            self.device = hid_device[0]
            self.device.open()
            self.device.set_raw_data_handler(self._read)
            self.report = self.device.find_output_reports()
            self.inputReport = self.device.find_input_reports()
            self.alive = True

    def setRead(self):
        self.device.set_raw_data_handler(self._read)
        
    def setReadFile(self):
        self.device.set_raw_data_handler(self._readFile)

    def stop(self):
        self.alive = False
        if self.device:
            self.device.close()
            
    def _read(self, data):
        self.recv_data = data[1:]
        self.q.put(data[1:])
            
    def _readFile(self, data):
        self.recv_data = data[1:]
        self.fileData.append(data[1:])
        self.flag = True
        
    def write(self, send_list):
        target_usage = 0
        if self.device:
            if self.report:
                sendData = [target_usage,]
                sendData.extend(send_list)
                self.report[target_usage].set_raw_data(sendData)
                bytes_num = self.report[target_usage].send()
                #import time
                #time.sleep(0.2)
                return bytes_num

    def read(self):
        import time
        time.sleep(0.2)
        return self.recv_data


def checkFlag(myhid):
    print('check')
    
    FLAG = False
    cnt = 1
    while FLAG == False:
        print('the %dth time' %cnt)
        cnt += 1
        import time
        time.sleep(1)
        if myhid.flag == False:
            FLAG = True
        else:
            myhid.flag = False
    for d in myhid.fileData:
        print(d)
    print('check end')
    myhid.stop()

if __name__ == '__main__':
    myhid = HidDevice(0x0483, 0x5750)
    target_usage = hid.get_full_usage_id(0x0483, 0x5750)
    myhid.start()
    if myhid.alive:
        #receiveData = myhid.setcallback()
        #send_list = [0x43, 0x4F, 0x4D, 0x43, 0x4F, 0x4E, 0x0D, 0x0A]
        #send_list = [67, 79, 77,83, 67, 76 , 20,  16,  11,  14, 21, 11, 1]
        #send_list = [67, 79, 77, 67, 79, 78]
        #send_list = [67, 79, 77, 71, 68, 82]
        send_list = [67, 79, 77, 71, 70, 76, 88, 88, 79, 79]
        while 64 != len(send_list):
            send_list.append(0x00)
        #send_list = [0x00 for i in range(65)]
        #myhid.send_values(send_list)
        myhid.write(send_list)
        #import threading
        #t = threading.Timer(0.5, checkFlag , (myhid,))
        #t.start()
        import time
        time.sleep(0.1)

        i = 0
        while not myhid.q.empty():
            i += 1
            print('the %dth time data is: %s' %(i,myhid.q.get()))
        '''
        import time
        time.sleep(5)
        for d in HidDevice.fileData:
            print(d)
        '''
        #myhid.stop()