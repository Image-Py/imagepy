import pandas as pd
import numpy as np

import itertools
import six

df = pd.DataFrame(np.arange(12).reshape(3,4),columns=['0', '1', '2', '3'])

x = df.drop(['2'], axis=1)
print('df {}'.format(df))
# print('x {}'.format(x))
print('index {}'.format(x.index))

dfList = df.T.values.tolist()

print('dfList {}'.format(dfList))
print('dfList 0 {}'.format(len(dfList)))


for index in range(len(x.columns.values.tolist())):
    print(index)
    print(x.columns[index])

    print('data {} {}'.format(index, x.iloc[:,index].values.tolist()))

print('data 2 {}'.format(df.iloc[:,2]))
# print('data -1 {}'.format(df.iloc[:,-1]))

y = df.drop(columns=['B','C'])
print('y {}'.format(y))
print('df {}'.format(df))


x = [[1,2,3], [4,5,6, 6.1, 6.2, 6.3], [7,8,9]]
newLine = map(list,map(None,*x))
newLine =  [list(row) for row in six.moves.zip_longest(*x, fillvalue=0.0)]

print('x {}'.format(x))
print('newLine {}'.format(newLine))