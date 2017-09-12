def hello():
    good=['this is a list','this is list 2']
    yield 'this is 3'
    yield 'this is 4'
    yield  'this is 5'
    yield good
    yield 'this is 6'

'''
print hello().next()
print hello().next()
print hello().next()
output='
this is 3
this is 3
this is 3'
'''
'''
ok=hello()
print ok.next()
print ok.next()
print ok.next()
print ok.next()
print ok.next()
#output='this is 3 this is 4 this is 5'
'''

def helloyield():
    good=[]
    for x in range(2):
        yield x
    #print loop().next()
    #print loop().next()
    yield hello()

isgood=helloyield()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
print isgood.next()
''''''
def loop():
    yield '1'
    print helloyield().next()
    print helloyield().next()
    print helloyield().next()

'''
test=helloyield()

print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
print test.next()
'''