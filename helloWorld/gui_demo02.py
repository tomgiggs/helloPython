import _tkinter
# encoding=utf8

# import Tkinter
import time
from tkinter import *# python3.2之前使用这个来导入：from TKinter import *

root = Tk()
root.title("gui样例002")
root.geometry('150x40')
# root.config(bg='#535353')

def start(*args, **kwargs):
    textBody = t.get(1.0, 999.0)
    filename = output_file_name.get()
    print(textBody, filename)
    # t2.insert(1.0, '转换完成')
    # t2.replace(1.0,2.0, '转换完成')

    for i in range(0, 101):
        percent.set(str(i)+'%')
        hour = int(i / 3600)
        minute = int(i / 60) - hour * 60
        second = i % 60
        canvas.coords(fill_line, (0, 0, i*2, 30))
        canvas.itemconfig(canvas_text, text='%02d:%02d:%02d' % (hour, minute, second))
        root.update()
        time.sleep(0.1)  # 控制进度条流动的速度
    # clear_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
    # time.sleep(3)
    # for i in range(0, 500, 5):
    #     canvas.coords(clear_line, (0, 0, i, 60))
    #     root.update()
    #     time.sleep(0.001)  # 控制进度条流动的速度


Label(root, text="待转换文字：").grid(row=0, sticky=W)
t = Text(root, height=20, width=100, setgrid=True)
t.grid(row=0, column=2)

Label(root, text="输出文件名称：").grid(row=1, sticky=W)
output_file_name = StringVar()
Entry(root, textvariable=output_file_name).grid(row=1, column=2, sticky=W)

Label(root, text="进度：").grid(row=3, sticky=W)
t2 = Text(root, height=1, width=10, setgrid=True)
t2.grid(row=3, column=2, sticky=W)

Label(root, text='下载进度:', ).grid(row=4, sticky=W)#sticky参数会让空间靠边对齐
canvas = Canvas(root, width=300, height=30,)

# canvas.place(x=110, y=60)

canvas_text = canvas.create_text(250, 10, anchor=NW)#文字会被覆盖掉。。。网上找的一段代码却不会被覆盖，没搞明白
canvas.itemconfig(canvas_text, text='00:00:00',fill='red')
# canvas.create_text((30, 8), text="文字", font=("微软雅黑", 6))#为什么不显示呢？？因为参数位置比画布还大
fill_line = canvas.create_rectangle(0, 0, 0, 30, fill="green")  # 创建一个矩形外边框（距离左边，距离顶部，矩形宽度，矩形高度），线型宽度，颜色

percent = StringVar()
Entry(root, textvariable=percent).grid(row=4, column=3, sticky=W)

button = Button(root, text="开始", bg="green", command=start,)
# button.config(state="disable") # 禁用按钮
button.grid(row=5, column=2)
# canvas.place(relx=0.45, rely=0.4, anchor=CENTER)
canvas.grid(row=4, column=2, sticky=W)# 这一步要在最后做，不然一旦绘制后就不会再往上加东西了

root.mainloop()
