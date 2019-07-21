#encoding=utf8
from fontTools.ttLib import TTFont
import xml.etree.ElementTree as et
from fontTools.ttLib import woff2

woff_body = TTFont('base.woff')
woff_body.saveXML('base.xml')

root = et.parse('base.xml').getroot()
# 找到map那一堆标签(PyQuery)
map_ele = root.find('cmap').find('cmap_format_12').findall('map')
# print(map_ele)

map_dict = {}
# 把map那一堆数据存到字典中
for m in map_ele:
      # print(help(m))
      code = m.attrib['code'].replace('0x', '')
      map_dict[code] = m.attrib['name']
print(map_dict)
