import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# cardinals  = np.arange(0,  361, 45)
# deviations = np.array([-2, -4, -3, -1,  2,   4,   3,   0,   -2])

# cardinals  = np.arange(0,  360, 45)
# deviations = np.array([-2, -2, -1, 0, 1, 1, 0.5, -1])

# From RYA Training Almanac
# cardinals  = np.arange(0,  361, 22.5)
# deviations = np.array([-4, -2, 0, 2, 4, 5, 6, 5, 4, 2, 0, -2, -4, -5,-6,-5,-4])

# # From http://www.americanflyers.net/aviationlibrary/instrument_flying_handbook/chapter_3.htm
# cardinals  = np.arange(0, 331, 30)
# deviations = np.array([1, 2, 2, 5, 3, 5, -4, 0, 3, 1, -4, -5])

# From http://code7700.com/direction.html
# cardinals  = np.arange(0, 346, 15)
# deviations = np.array([1, 1, 1, 1, 2, 2, 2, 2, 2, 0, -1, -1, -1, -1, -1,-1,-2, -2, -2, -2, -2, -1, 0, 1])

# From http://threesheetsnw.com/svselah/2011/06/23/that-took-an-adjustment/
# cardinals  = np.arange(0, 361, 45)
# deviations = np.array([1, 1, 0, 0, -1, -1, 0, 0, 1])

# From http://opencpn.org/ocpn/node/178
# cardinals  = np.arange(0, 331, 30)
# deviations = np.array([1, 3, 4, 4, 3, 2, -1, -3, -5, -6, -4, -2])

# From http://www.globalsecurity.org/military/library/policy/army/fm/55-501/fig6-6-2.gif
# cardinals  = np.arange(0, 361, 15)
# deviations = np.array([-4, -4, -3.5, -3.2, -3, -2.5, -2, -1.8, -1.2, -0.8,-0.5, 1.5, 2, 2.5, 3, 3.5, 4, 3.5, 3, 2, 1.5, 1, 0.5, -1, -4])

# From https://www.flickr.com/photos/seadog-images/3591881376/
# cardinals  = np.arange(0, 361, 45)
# deviations = np.array([1, 1.5, 1, 1, 1, 1.5, 1, 0, 1])


# From http://www.collectors-edition.de/FokkerTeam/Steuertabelle.JPG
cardinals  = np.arange(0, 331, 30)
deviations = np.array([3, 1, -1, 0, 3, 5, 6, 5, 4, 2, 3, 3])

# From http://code7700.com/images/compass_correction_card_afm_51-37_figure_1-15.png
# cardinals  = np.arange(0, 361, 15)
# deviations = np.array([1, 1, 1, 1, 2, 2, 2, 2, 2, 0, -1, -1, -1, -1, -1, -1,-2, -2, -2, -2, -2, -1, 0, 1, 1])



# plot the actual data points
plt.plot(cardinals, deviations, 'rs')

# function to fit a sine curve to the line
def sine_curve(t1, offset=0, scale=1):
    radians = t1 / 360. * 2. * np.pi
    return np.sin(radians+offset) * scale

# from http://opencpn.org/ocpn/node/178
def deviation_curve(t1, A, B, C, D, E):
    radians = t1 / 360. * 2. * np.pi
    return A + B * np.sin(radians) + C * np.cos(radians) + D * np.sin(2*radians) + E * np.cos(2*radians)

degrees    = np.arange(0,  361, 1)

# use curve_fit
# popt, pcov = curve_fit(sine_curve, cardinals, deviations)
# print popt
# plt.plot(degrees, sine_curve(degrees, *popt), 'r')

# use curve_fit with the better fit
popt, pcov = curve_fit(deviation_curve, cardinals, deviations)
print popt
plt.plot(degrees, deviation_curve(degrees, *popt), 'g--')


plt.grid(True)
plt.show()
