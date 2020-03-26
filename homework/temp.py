import zlib

str_object1 = open('temp.txt', 'rb').read()
str_object2 = zlib.decompress(str_object1)
f = open('my_recovered_log_file_bs.txt', 'wb')
f.write(str_object2)
f.close()


str_object1 = open('inverted_indexes/id_2.txt', 'rb').read()
str_object2 = zlib.decompress(str_object1)
f = open('my_recovered_log_file_2', 'wb')
f.write(str_object2)
f.close()

'''

dic = "hfhsjhkjdnsfsdjkfkuhflufirjefhfbjaioopaidzejhzhk;bsbdksfhliufishlbehkffekbhh"
filename = 'grades.txt'
file = open(filename, 'wb')
pickle.dump(dic, file)


fo = open("demo.txt", "w+b")
my_dic = 'hello world'
compressedText = zlib.compress(my_dic.encode('ISO-8859-1'))
fo.write(compressedText)
print(fo.tell())

my_dic_2 = 'my name is pierre'
compressedText_2 = zlib.compress(my_dic_2.encode('ISO-8859-1'))
print(fo.write(compressedText_2))


print(fo.tell())


fo.close()
fo = open("demo.txt", "r+b")

##fo.seek(4)
##data = fo.read(11)
##data = zlib.decompress(data).decode('ISO-8859-1')
##print(data)
'''