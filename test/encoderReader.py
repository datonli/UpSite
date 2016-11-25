
with open("UUU.CSV", "rb") as f:
    byte = f.read(1)
    byteList = list()
    while byte:
        ob = ord(byte)
        byteList.append(ob)
        byte = f.read(1)
    #print(byteList)
    #print(len(byteList)/64)
for i in range(int(len(byteList)/64)):
    l = byteList[i*64:(i+1)*64]
    print('%d bytes is %s' %(i,l))

