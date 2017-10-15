import os
import sys
fileList=[]
#print os.name
#print os.environ
#print os.path.dirname('E:/')

#get temprary dir
dirs=os.getcwd()
print dirs
#print os.path.split(dirs)
'''
#get filelist
fileList=os.listdir(dirs)
print fileList
'''

#testDir=os.mkdir(dirs+'/test')
newdir='test'
path=dirs+'/'+newdir
print path
os.mkdir(path)
fileName=os.path.join(path,'test.txt')
print fileName
file=open(fileName,'w+')
file.write('i am created by python program,test ok')
file.close()

