import sys
import os
def getArg():
    for x in sys.argv:
       print x
    print 'there is total %s args'%len(sys.argv)

getArg()
def getPath():
    print 'my dir is %s'%os.getcwd()
getPath()

def getFatherPath():
    dirs=[]
    path=os.getcwd()

    print path
    dirname= os.path.split(path)
    print dirname
    path1=os.path.dirname(dirname[0])
    print path1
    path2=os.path.dirname(path1)
    print path2
    path3 = os.path.dirname(path2)
    print path3

    '''
    x=0
    while x>2:
        x+=1
        dirs.append(path[0])
        path=os.path.dirname(path[0])
        print path
    print dirs
    '''

    '''
    x=os.path.split(os.getcwd())
    print x
    while x:
        x=os.path.split(x[0])
        dirs.append(x)
    print dirs
    '''

getFatherPath()
print os.path.split(os.path.realpath(sys.argv[0]))