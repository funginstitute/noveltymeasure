import pandas as pd

def trim(txt):
  if '.0' in txt:
    return txt[:txt.rfind('.0')]
  return txt

matrix = pd.read_csv('matrix',header=None)
dates = pd.read_csv('appdates.csv',header=None)

patent = 7692844

daterow = dates[dates[0] == patent]
date = int(daterow[2])
index = int(daterow.index)

rows = matrix[matrix[0] == index]
# number of unique words in the focal patent
focaluniquewords = len(rows)

words = matrix[matrix[1].isin(rows[1])]

before = dates[((date - dates[2]) < 50000) & ((date - dates[2]) > 0)]
after = dates[((dates[2] - date) < 50000) & ((dates[2] - date) > 0)]

pat_before = words[words[0].isin(before.index)].groupby(0).count()[1]
pat_after = words[words[0].isin(after.index)].groupby(0).count()[1]

after['count'] = pat_after
before['count'] = pat_before

after = after.fillna(0)
before = before.fillna(0)

after[0] = after[0].astype(str).apply(trim)
after[2] = after[2].astype(str).apply(trim)
before[2] = before[2].astype(str).apply(trim)

del after[2]
del before[2]

after.to_csv('after.csv',index=False)
before.to_csv('before.csv',index=False)
