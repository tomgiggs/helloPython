#encoding=utf8
import PIL
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from pytesseract import image_to_string
import pytesseract

def test():
    pytesseract.pytesseract.tesseract_cmd = r'D:\program\Tesseract-OCR\tesseract.exe'
    img = Image.open(r'd:\data\photoes\tess___9CRr.PNG','r') #200,70
    img = img.convert('P')
    print(img.size)


    #img.show()
    ret = image_to_string(img, config="-psm 6 -c tessedit_char_whitelist='ABCEFGHJKLMNPRTUXY'")
    # Linux服务器上结果为AGRBHA，windows 上结果为ACOARoHA，服务器上结果是正确的，但是Windows上结果是错误的
    print(ret)

test()

# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))

# # 随机颜色1:
# def rndColor():
#     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def draw_img():
    width = 160
    height = 60
    image = Image.new('RGB', (width, height), (255, 255, 255))
    # # 创建Font对象:
    font = ImageFont.truetype(r'C:\Windows\Fonts\simsunb.ttf', size=100)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # # 填充每个像素:
    # for x in range(width):
    #     for y in range(height):
    #         draw.point((x, y), fill=rndColor())
    # 输出文字:
    for t in range(4):
        draw.text((40 * t+20, 30), rndChar(), fill=rndColor2())
    # 模糊:
    # image = image.filter(ImageFilter.BLUR)
    image.show()
    #image.save('code.jpg', 'jpeg');
