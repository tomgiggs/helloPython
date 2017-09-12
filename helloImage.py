import re
import urllib2
import urllib
import  requests
import  socket
photoUrl=""
path="E:\photo/"

socket.setdefaulttimeout(2000)
for x in range(245,250):
        for p in range(24578,24700):
            for y in range(1,10):

                    filepath=path+str(y)+".jpg"
                    photo = photoUrl+str(x)+"/"+str(p)+"-"+str(y)+".jpg"
                    urllib.urlretrieve(photo,filepath)
                    print photo
'''
                    #
                    #page=urllib.urlopen(photo)
                    page=requests.get(photo,timeout=10)
                    file = open(filepath,"ab+")

                    file.write(page.content)
                    file.flush()
                    file.close()
'''



