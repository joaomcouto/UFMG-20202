import struct
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

sendMsg = (5556).to_bytes(5,'big')

# sendMsg = bytearray(2)
# sendMsg[1] = 2
# sendMsg.extend(bytearray(4))
# sendMsg[2:5] = bytearray([5556])

print(sendMsg)