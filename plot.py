import pandas as pd
import matplotlib.pyplot as plt

before = pd.read_csv('before.csv')
after = pd.read_csv('after.csv')

# plot histograms
a = before['count'].hist(bins=50)
f = a.get_figure()
f.savefig('beforehist.png')
plt.clf()

a = after['count'].hist(bins=50)
f = a.get_figure()
f.savefig('afterhist.png')
plt.clf()

# plot timeseries

# with resample:
numbins = 1000
g = before.groupby(pd.qcut(before.index, numbins)).median() # can also use .mean()
a = plt.plot(range(numbins), g['count'])
f = a[0].get_figure()
f.savefig('beforeplot.png')
plt.clf()

g = after.groupby(pd.qcut(after.index, numbins)).median() # can also use .mean()
a = plt.plot(range(numbins), g['count'])
f = a[0].get_figure()
f.savefig('afterplot.png')
plt.clf()
