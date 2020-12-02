import obspy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

data = obspy.read('data.mseed')
#print(data)
tr = data[-1]
print(tr.stats)
print(tr.data)
plt.plot(tr.times(), tr.data)
plt.show()
