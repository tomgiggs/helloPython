#encoding=utf8

import numpy as np
from PIL import Image
from pylab import *
from scipy import misc
import cv2
from PIL import Image


# #img = np.load(r'D:\data\tf\mnist_train\1\mnist_train_3.png') #OSError: Failed to interpret file 'D:\\data\\tf\\mnist_train\\1\\mnist_train_3.png' as a pickle
# #image to numpy array
# img = Image.open(r'D:\data\tf\mnist_train\1\mnist_train_3.png')
# img_array = Image.fromarray(uint8(img)) #<PIL.Image.Image image mode=L size=28x28 at 0xBD4ECF8>
# img_np = np.array(img_array) # ok
#
# #numpy array to image
# #img_out = misc.toimage(img_np)
# img = Image.fromarray(img_np)
# img.save('./array_to_img.jpg')
# # img_out.save('./numpy_out.jpg') # save image as a file
# #img_out.show()

video = cv2.VideoCapture('./data/VID_20170922_193234.mp4')
np.set_printoptions(threshold=np.inf)
while video.isOpened():
  # Capture frame-by-frame
  ret, frame = video.read()
  if ret is True:
    cv2.putText(frame, "好好学习，天天吃土", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (1,125))
    arrays = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    print(arrays.shape)
    arrays = cv2.resize(arrays, (480, 270))
    #cv2.rotate(arrays,rotateCode=0)
    arrays = np.transpose(arrays)
    print(arrays)

    print(arrays.shape)
    cv2.imshow('Frame', arrays)
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  else:
    break

video.release()
cv2.destroyAllWindows()


