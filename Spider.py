#coding=utf-8
import urllib.request

file=urllib.request.urlopen('https://github.com/devillove084/CollageDesign')

data=file.read()
print(data)