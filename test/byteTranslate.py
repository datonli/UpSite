# -*- coding: utf-8 -*-

class ByteTranslate(object):
    def readFile(self):
        #with open('QQQ6.TXT','rb') as f:
        with open('bt.txt','r') as f:
            lines = f.read()
            return lines
            
    def writeFile(self):
        with open('wf.txt','wb') as f:
            f.write(b'hello world')
            
    def printLines(self):
        lines = self.readFile()
        print(lines)
        #print(lines.decode('gbk'))
        
if __name__ == '__main__':
    bt = ByteTranslate()
    bt.printLines()
    bt.writeFile()