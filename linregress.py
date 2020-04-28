from scipy import stats
import numpy as np
import pylab

x = np.array([2500050000,
            2500225000,
            2500400000,
            2500575000,
            2500750000,
            2500925000,
            2501100000,
            2501275000,
            2501450000])
y = np.array([1.32409698149857,
            1.28799676639904,
            1.25234143571827,
            1.21621137548904,
            1.1810833087663,
            1.14619627200914,
            1.11128096091859,
            1.0768641158539,
            1.04237449056064])

slope, intercept, r_value, p_value, slope_std_error = stats.linregress(x,y)

predict_y = intercept + slope * x
pred_error = y - predict_y
degrees_of_freedom = len(x)-2
residual_std_error = np.sqrt(np.sum(pred_error**2)/degrees_of_freedom)

# Plotting
print(slope)
print(intercept)
pylab.plot(x,y,'o')
pylab.plot(x,predict_y,"k-")
pylab.show()