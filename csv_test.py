import numpy
a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
numpy.savetxt("foo.csv", a, delimiter=",")

import pickle

mylist = [1, 'foo', 'bar', {1, 2, 3}, [ [1,4,2,6], [3,6,0,10]]]
with open('mylist', 'wb') as f:
    pickle.dump(mylist, f) 


with open('mylist', 'rb') as f:
    mylist = pickle.load(f)
print(mylist)


