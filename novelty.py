import pandas as pd
import sys

def trim(txt):
  if '.0' in txt:
    return txt[:txt.rfind('.0')]
  return txt

# 0: patent idx 1: word idx 2: word count
matrix = pd.read_csv('full_matrix',header=None)
# 0: patent 1: date 2: sortable date
dates = pd.read_csv('appdates.csv',header=None)
wordcounts = pd.DataFrame()
wordcounts[0] = matrix.groupby(0).count()[1].astype('float32')

# patent is a patent number, e.g. '4130416', NOT a row index
#patent = sys.argv[1]
for patent in sys.argv[1:]:
# get the date for that patent
  daterow = dates[dates[0] == patent]
  date = int(daterow[2])

  # get all words + word counts for that patent
  rows = matrix[matrix[0] == int(daterow.index)]
  # number of unique words in this patent
  unique_count_focal = len(rows)

  # get all patents that share at least 1 word
  overlap_patents = matrix[matrix[1].isin(rows[1])]

  # get the patent numbers for patents before/after the date of our focal patent
  before = dates[((date - dates[2]) < 50000) & ((date - dates[2]) > 0)]
  after = dates[((dates[2] - date) < 50000) & ((dates[2] - date) > 0)]

  pat_before = overlap_patents[overlap_patents[0].isin(before.index)]
  pat_after = overlap_patents[overlap_patents[0].isin(after.index)]


  pat_before_count = pat_before.groupby(0).count()[1].astype('float32')
  pat_after_count = pat_after.groupby(0).count()[1].astype('float32')

  #import IPython
  #IPython.embed(user_ns=locals())

  try:
    after['overlap'] = pat_after_count
    t1 = list((unique_count_focal - pat_after_count).values)
    t2 = list(wordcounts[wordcounts.index.isin(pat_after[0])].values)
    print len(t1),len(t2), len(after)
    after['union'] = [a+b for a,b in zip(t1,t2)]
    after['union'] = after['union'].astype(int)
    after['jaccard'] = after['overlap'] / after['union']
    after = after.sort('jaccard', ascending=False)

    before['overlap'] = pat_before_count
    t1 = list((unique_count_focal - pat_before_count).values)
    t2 = list(wordcounts[wordcounts.index.isin(pat_before[0])].values)
    print len(t1),len(t2),len(before)
    before['union'] = [a+b for a,b in zip(t1,t2)]
    before['union'] = before['union'].astype(int)
    before['jaccard'] = before['overlap'] / before['union']
    before = before.sort('jaccard', ascending=False)
  except Exception as e:
    import IPython
    IPython.embed(user_ns=locals())
    print 'ERROR',patent,e

  after = after.fillna(0)
  before = before.fillna(0)
  print after.columns

  # 0: patent num, 1: date, 2: sortabledate, overlap: # overlapping words, union: # unique words

  after[0] = after[0].astype(str).apply(trim)
  before[0] = before[0].astype(str).apply(trim)

  del after[2]
  del before[2]

  after.to_csv('{0}_after.csv'.format(patent),index=False)
  before.to_csv('{0}_before.csv'.format(patent),index=False)
