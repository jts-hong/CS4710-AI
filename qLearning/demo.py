import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data_10000.csv')
df.plot(y=["A_Price","B_Price","A_PI","B_PI"])
df.plot(y=["A_PI","B_PI"])
df.plot(y=["A_Price","B_Price","A_PI","B_PI",'CONS_1','CONS_2'])
plt.show()