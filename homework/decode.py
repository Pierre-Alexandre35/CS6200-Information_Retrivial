import pickle
import zlib

import os, sys
from chardet import detect
import gzip

path = 'inverted_indexes/id_1.txt'

fo = open(path, 'r+b')
fo.seek(30)
data = fo.read(80)
data = zlib.decompress(data, wbits=25).decode('ISO-8859-1')

##print(data)


'''
with gzip.open(path, "rb") as f:
    f.seek(0) 
    data = f.read(80)
    decoded = data.decode('ISO-8859-1')
    print(decoded)
    with open("samples/instead.txt", "w") as f:
        f.write(decoded)
'''    
    

'''
with gzip.open(path, "rb") as f:
	data = f.read( )
cr = data.decode('ISO-8859-1')

print(cr)
    
'''


##current_bytes = os.read(str_object1, 200)
##os.read()
##zlib.decompress(current_bytes)




##str_object2 = zlib.decompress(str_object1)
##print(str_object2)


##f = open('my_recovered_log_file_2', 'wb')
##f.write(str_object2)
##f.close()


