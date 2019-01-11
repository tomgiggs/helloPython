#endocing=utf8

import json
import execjs

jsfile = r'd:\data\test.js'
jsin = open(jsfile,'r')
ctx = execjs.compile(jsin)
print(ctx.call())


