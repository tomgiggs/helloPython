#encoding=utf8
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
df = pd.read_csv('../Pokemon.csv', index_col=0)
#print df.head()
#aa = sns.lmplot(x='Attack', y='Defense', data=df)
#sns.boxplot(data=df)
sns.set_style('whitegrid')
# Violin plot
sns.violinplot(x='Type 1', y='Attack', data=df)
plt.show()