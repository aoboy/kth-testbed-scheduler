#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

N = 5
menMeans = (20, 35, 30, 35, 27)
menStd =   (2, 3, 4, 1, 2)

ind = np.arange(N)  # the x locations for the groups
width = 0.5       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)

womenMeans = (25, 32, 34, 20, 25)
womenStd =   (3, 5, 2, 3, 3)
rects2 = ax.bar(ind+width, womenMeans, width, color='y', yerr=womenStd)

# add some
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('G1', 'G2', 'G3', 'G4', 'G5') )

ax.legend( (rects1[0], rects2[0]), ('Men', 'Women') )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

plt.show()


#!/usr/bin/env python
# make a horizontal bar chart

#from pylab import *
#val = 3+10*rand(5)    # the bar lengths
#pos = arange(5)+.5    # the bar centers on the y axis
#
#figure(1)
#barh(pos,val, align='center')
#yticks(pos, ('Tom', 'Dick', 'Harry', 'Slim', 'Jim'))
#xlabel('Performance')
#title('How fast do you want to go today?')
#grid(True)
#
#figure(2)
#barh(pos,val, xerr=rand(5), ecolor='r', align='center')
#yticks(pos, ('Tom', 'Dick', 'Harry', 'Slim', 'Jim'))
#xlabel('Performance')
#
#show()