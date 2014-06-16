import pandas as pd

print "Loading matrix..."
matrix = pd.read_csv('matrix',header=None)
print "Loading dictionary..."
worddict = pd.read_csv('dict',header=None)
print "Loading dates..."
dates = pd.read_csv('appdates.csv',header=None)

out = []

print "Iterating through words"
for row in worddict.iterrows():
  wordindex = row[1][0]
  exists = matrix[matrix[1] == wordindex]
  patent = dates.iloc[exists[0]][2].idxmin()
  #patent = dates[dates[0].isin(exists[0])][2].idxmin()
  print dates.loc[patent][0], dates.loc[patent][1], row[1][1]
  out.append([dates.loc[patent][0], dates.loc[patent][1], row[1][1]])

pd.DataFrame.from_records(out).to_csv('firstseen.csv',index=False)

