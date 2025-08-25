import hashlib

filepath = 'C://Users/31522/Desktop/1.png'
file = open(filepath, "rb")
md = hashlib.md5()
md.update(file.read())
res1 = md.hexdigest()
print(res1)