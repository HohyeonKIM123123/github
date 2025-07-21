import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("./07-pandas/books2.csv")
df = pd.read_csv("./07-pandas/books2.csv")
df = pd.read_csv("./07-pandas/books2.csv")
df = pd.read_csv("./07-pandas/books2.csv")
df = pd.read_csv("./07-pandas/books2.csv")


sns.pairplot(df, vars=['가격', '출간연도'], hue='카테고리')
plt.suptitle('가격, 출간연도 관계 Pairplot', y=0.98)
plt.savefig('pairplot.png')
plt.show() 