#! /usr/bin/env python3
# coding: UTF-8
# python3.3 

''' 
@version: "2015-12-31"
@var: communication with usb device
@author: lidatong
'''
import usb.core
import usb.util

TEST = False

class UsbDevice:
    '''the function of usb'''
    def __init__(self, _vend, _prod):
        '''init device'''
        self._dev = usb.core.find(idVendor=_vend, idProduct=_prod)
        #self._dev.reset()
        self.printAttr()  
        self.device = self.getDevice(_vend, _prod)
      
        if self.device == None:
            print("not find dev")
        else:
            self.handle = self.openDevice(self.device)


    def getDevice(self, _vend, _prod):
        '''get device'''
        busses = usb.busses()

        for bus in busses:
            devices = bus.devices
            for device in devices:
                if device.idVendor == _vend and device.idProduct == _prod:
                    return device
        return None

   
    def printAttr(self):
            for cfg in self._dev:
                for intf in cfg:
                    self._dev.set_configuration()
                    #print('intf bInterfaceNumber = %s, bAlternateSetting = %s' %(str(intf.bInterfaceNumber),str(intf.bAlternateSetting)))
                    #for ep in intf:
                        #print('ep bEndpointAddress = %s' %(str(ep.bEndpointAddress)))
       

    def openDevice(self, device):
        '''open device'''
        
        self.handle = device.open()
        #self._dev.set_configuration(1)
        #self.handle.detach_kernel_driver(0)
        '''
        if self._dev.is_kernel_driver_active(0):
            try:
                self.handle.detach_kernel_driver(0)
            except:
                print("detachKernelDriver")
        '''
        try:
            self.handle.claimInterface(0)
        except:
            print("claimInterface")
            raise
        #self._dev.reset()
        #print(self.handle)
        return self.handle

    
    

    def write_data(self, sendlist):
        '''write a list to ep'''
        #self._dev.set_configuration(1)
        ep   = self._dev[0][(0,0)][1].bEndpointAddress
        size = self._dev[0][(0,0)][0].wMaxPacketSize
        #print('write part : ep = %s,size = %s' % (ep,size))
        if TEST:
            ep = 0x01
        try:
            self.handle.interruptWrite(ep, sendlist, 5000)
        except:
            raise


    def read_data(self):
        '''read data from ep and return a list'''
        #self._dev.set_configuration(1)
        ep   = self._dev[0][(0,0)][0].bEndpointAddress
        size = self._dev[0][(0,0)][0].wMaxPacketSize
        #print('read part : ep = %s,size = %s' % (ep,size))
        if TEST:
            ep = 0x82
        my_data_list = []
        try:
            data = self.handle.interruptRead(ep, size, 5000)
                
            #print('after interruptRead')
            #print(data)
            return data
        except:
            raise
        
    def close(self):   
        """ Release device interface """

        self.handle.reset()
        self.handle.releaseInterface()

        self.handle, self.device = None, None        
        
    def release_interface(self):
        '''release the claim interface'''
        self.handle.releaseInterface()


if __name__ == '__main__':
    ''''''
    VID_CAPAC = 0x0483
    PID_CAPAC = 0x5750

    sendlist = [67, 79, 77,83, 67, 76 , 20,  16,  11,  14, 21, 11, 1]
    
    device = UsbDevice(VID_CAPAC, PID_CAPAC)
 
    device.write_data(sendlist)
    print('write scuess')
    my_data_list = device.read_data()
    print('after read')
    print(my_data_list)
    device.close()
    print("read scuess")
    #device.release_interface()

