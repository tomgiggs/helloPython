#encoding=utf8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from pylab import rcParams

df = pd.read_csv("E:\data\dataset\googleplaystore.csv")
print(df.describe().T)
print(df['Category'].unique)
print(df.size)