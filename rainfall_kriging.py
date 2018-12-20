"""雨量站克里金插值"""
import pyKriging
from pyKriging.krige import kriging
from pyKriging.samplingplan import samplingplan

# The Kriging model starts by defining a sampling plan, we use an optimal Latin Hypercube here
sp = samplingplan(2)
X = sp.optimallhc(20)

# Next, we define the problem we would like to solve
testfun = pyKriging.testfunctions().branin
y = testfun(X)

# Now that we have our initial data, we can create an instance of a Kriging model
k = kriging(X, y, testfunction=testfun, name='simple')
k.train()

# Now, five infill points are added. Note that the model is re-trained after each point is added
numiter = 5
for i in range(numiter):
    print
    'Infill iteration {0} of {1}....'.format(i + 1, numiter)
    newpoints = k.infill(1)
    for point in newpoints:
        k.addPoint(point, testfun(point)[0])
    k.train()

# And plot the results
k.plot()
