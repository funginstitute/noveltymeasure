# Novelty Measure

`novelty.py` expects two files: firstly, a document matrix following `[i,j,val]` nomenclature: `X[i,j]` 
is the number of times term `j` appears in document `i`. Secondly, `appdates.csv`, which has 3 columns:
document identifier, date of publication/filing, and transformed date. The transformed date should
look like YYYYMMDD so that it is a sortable integer.

This will create 2 files: `after.csv` and `before.csv`, which give the number of overlapping words
with each document 5 years before/after the focal document.

`plot.py` will create some helpful graphs from the above output files.
