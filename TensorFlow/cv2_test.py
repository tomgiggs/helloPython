import numpy as np
import scipy
import cv2
from PIL import Image

src_img = cv2.imread('./data/mnist_train/1/mnist_train_3.png',1)
cv2.resize(src_img,(80,80),interpolation=cv2.INTER_AREA)
print(src_img)
print('waiting')


