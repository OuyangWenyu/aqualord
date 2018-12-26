"""The conditional merging process.
(a) The rainfall field is observed at discrete points by rain gauges.
(b) The rainfall field is also observed by radar on a regular, volume-integrated grid.
(c) Kriging of the rain gauge observations is used to obtain the best linear unbiased estimate of rainfall
    on the radar grid.
(d) The radar pixel values at the rain gauge locations are interpolated onto the radar grid using Kriging.
(e) At each grid point, the deviation C between the observed and interpolated radar value is computed.
(f) The field of deviations obtained from (e) is applied to the interpolated rainfall field obtained
    from Kriging the rain gauge observations.
(g) A rainfall field that follows the mean field of the rain gauge interpolation,
    while preserving the mean field deviations and the spatial structure of the radar field is obtained"""
import numpy as np
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging

import project_util
import time_unit_type

'''get discrete points by rain gauges from database'''
start_time = '2017-08-05 00:00:00'
end_time = '2017-08-10 00:00:00'
data = project_util.read_data_from_db_timesequence(15, 114, str(time_unit_type.TimeUnitType.Hour.value), 1, start_time, end_time)
# transform data to the form of np.array, need zero to fill up the array
data = np.array([[0.3, 1.2, 0.47],
                 [1.9, 0.6, 0.56],
                 [1.1, 3.2, 0.74],
                 [3.3, 4.4, 1.47],
                 [4.7, 3.8, 1.74]])
# calculate the grid number in radar graph of rain gauge by its geological coordination
# Firstly, give out a virtual position
gridx = np.arange(0.0, 5.5, 0.5)
gridy = np.arange(0.0, 5.5, 0.5)

'''get volume-integrated grid data by radar from database'''

'''krige the rain gauge observations'''
# Create the ordinary kriging object. Required inputs are the X-coordinates of
# the data points, the Y-coordinates of the data points, and the Z-values of the
# data points. If no variogram model is specified, defaults to a linear variogram
# model. If no variogram model parameters are specified, then the code automatically
# calculates the parameters by fitting the variogram model to the binned
# experimental semivariogram. The verbose kwarg controls code talk-back, and
# the enable_plotting kwarg controls the display of the semivariogram.
OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear',
                     verbose=False, enable_plotting=False)

# Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
# grid of points, on a masked rectangular grid of points, or with arbitrary points.
# (See OrdinaryKriging.__doc__ for more information.)
z, ss = OK.execute('grid', gridx, gridy)

# visualize the interpolation data


'''krige radar data at the rain gauge locations'''

'''compute the deviation between the radar-observation and kriging-radar'''

'''apply deviation to kriging-rain-gauge'''
