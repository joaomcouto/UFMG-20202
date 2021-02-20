import struct
import os
# def utf8len(s):
#     return len(s.encode('utf-8'))

# #print(utf8len(b'12'))
# txt = "pythõn lala"
# x = txt.encode()
# print(x)

# txt = "My name is Ståle"
# x = txt.encode()
# print(x)



# msg = bytearray(2)
# msg[1] = 1 
# print(msg, '\n')
# print(int.from_bytes(msg, 'big'))



#sendMsg = b''
#sendMsg += struct.pack('')



# sendMsg = bytearray(2)
# sendMsg[1] = 2
# sendMsg.extend(bytearray(4))
# sendMsg[2:5] = bytearray([5556])

#sendMsg = (5556).to_bytes(5,'big')
#print(sendMsg)




# for c in string:
#     print(ord(c).to_bytes(1,'big'))

# print([(ord(c)).to_bytes(1,'big') for c in string])






# print(len('arquivodoc'.split('.')))


# fileNameInts = [int(ord(c)) for c in string]

# for c in fileNameInts:
#     print(type(3))
#     print((3).to_bytes(1,'big'))




# string = 'arquivo.doc'

# msg = (3).to_bytes(2, 'big')

# msg += (0).to_bytes(0, 'big')

# for c in string:
#     msg += (ord(c)).to_bytes(1,'big')

# #msg= [(ord(c)).to_bytes(1,'big') for c in string]
# print(msg[-4])


# print(msg)

fileName = 'arquivo.doc'
print(os.path.getsize(fileName))
