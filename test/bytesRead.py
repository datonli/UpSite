# -*- coding: utf-8 -*-
 
def how_many_byte(a):
    """
        判断这个字符是由几个字节组成的        
        向右移2位，如果移位后的数字的各位都是1那么这个字符由6个字节组成
        向右移3位，如果移位后的数字的各位都是1那么这个字符由5个字节组成
        以此类推
    """
    bits = 8
    move_bits = 2
    while move_bits < bits:
        temp = (a >> move_bits)
        all_1 = 0
        for i in range(bits-move_bits):
            all_1 += 2**i
        if temp == all_1: return bits - move_bits
        move_bits += 1       
    return 1
 
     
with open('QQQ6.TXT','rb') as file_t:
    #读取3个字节跳过BOM
    file_t.read(3)
    while True:
        #读取一个字节
        a = file_t.read(1)
        if not a:
            print('read to end of the file')
            break
        else:        
            bytes_count = how_many_byte(ord(a))
            #print(bytes_count)
            if bytes_count > 1:
                aleft = file_t.read(bytes_count-1)
                a = a+aleft
            print('%s length is %i'%(a,len(a)))
