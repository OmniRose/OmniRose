import copy

# samples of various deviation tables

from .models import Curve, CurveCalculations

def create_database_curve_from_sample(sample):
    curve = Curve.objects.create()
    for ships_head, deviation in sample.items():
        curve.reading_set.create(ships_head=ships_head, deviation=deviation)
    return curve

def create_curve_calculation_from_sample(sample):
    curve = CurveCalculations()
    curve._readings_as_dict = copy.deepcopy(sample)
    return curve

samples = {}

samples['rya_training_almanac'] = {
    0    : -4,
    22.5 : -2,
    45   :  0,
    67.5 :  2,
    90   :  4,
    112.5:  5,
    135  :  6,
    157.5:  5,
    180  :  4,
    202.5:  2,
    225  :  0,
    247.5: -2,
    270  : -4,
    292.5: -5,
    315  : -6,
    337.5: -5,
}

samples['rya_training_almanac_every_45'] = {
    0    : -4,
    45   :  0,
    90   :  4,
    135  :  6,
    180  :  4,
    225  :  0,
    270  : -4,
    315  : -6,
}

samples['rya_training_almanac_every_90'] = {
    0    : -4,
    90   :  4,
    180  :  4,
    270  : -4,
}

# Astrid 1974
samples['astrid_1974'] = {
    0  : 2,
    15 : 2,
    30 : 1,
    45 : 0,
    60 : 0,
    75 : 0,
    90 : 0,
    105: -1,
    120: -2,
    135: -3,
    150: -3,
    165: -2,
    180: -1,
    195: 0,
    210: 2,
    225: 3,
    240: 3,
    255: 2,
    270: 2,
    285: 2,
    300: 2,
    315: 4,
    330: 4,
    345: 3,
}

# From http://opencpn.org/ocpn/node/178
samples['opencpn_sample'] = {
    0:    1,
    30:   3,
    60:   4,
    90:   4,
    120:  3,
    150:  2,
    180: -1,
    210: -3,
    240: -5,
    270: -6,
    300: -4,
    330: -2,
}

# From http://www.globalsecurity.org/military/library/policy/army/fm/55-501/fig6-6-2.gif
samples['global_security'] = {
    0  : -4,
    15 : -4,
    30 : -3.5,
    45 : -3.2,
    60 : -3,
    75 : -2.5,
    90 : -2,
    105: -1.8,
    120: -1.2,
    135: -0.8,
    150: -0.5,
    165: 1.5,
    180: 2,
    195: 2.5,
    210: 3,
    225: 3.5,
    240: 4,
    255: 3.5,
    270: 3,
    285: 2,
    300: 1.5,
    315: 1,
    330: 0.5,
    345: -1,
}

# From http://www.collectors-edition.de/FokkerTeam/Steuertabelle.JPG
# cardinals  = np.arange(0, 331, 30)
# deviations = np.array([3, 1, -1, 0, 3, 5, 6, 5, 4, 2, 3, 3])
samples['fokker_team'] = {
    0:    3,
    30:   1,
    60:  -1,
    90:   0,
    120:  3,
    150:  5,
    180:  6,
    210:  5,
    240:  4,
    270:  2,
    300:  3,
    330:  3,
}

# From http://code7700.com/direction.html
samples['code7700_direction'] = {
    0  :  1,
    15 :  1,
    30 :  1,
    45 :  1,
    60 :  2,
    75 :  2,
    90 :  2,
    105:  2,
    120:  2,
    135:  0,
    150: -1,
    165: -1,
    180: -1,
    195: -1,
    210: -1,
    225: -1,
    240: -2,
    255: -2,
    270: -2,
    285: -2,
    300: -2,
    315: -1,
    330:  0,
    345:  1,
}


# # From http://www.americanflyers.net/aviationlibrary/instrument_flying_handbook/chapter_3.htm
# cardinals  = np.arange(0, 331, 30)
# deviations = np.array([1, 2, 2, 5, 3, 5, -4, 0, 3, 1, -4, -5])
samples['instrument_flying_handbook'] = {
    0:    1,
    30:   2,
    60:   2,
    90:   5,
    120:  3,
    150:  5,
    180: -4,
    210:  0,
    240:  3,
    270:  1,
    300: -4,
    330: -5,
}


# cardinals  = np.arange(0,  361, 45)
# deviations = np.array([-2, -4, -3, -1,  2,   4,   3,   0,   -2])

# cardinals  = np.arange(0,  360, 45)
# deviations = np.array([-2, -2, -1, 0, 1, 1, 0.5, -1])



# From http://threesheetsnw.com/svselah/2011/06/23/that-took-an-adjustment/
# cardinals  = np.arange(0, 361, 45)
# deviations = np.array([1, 1, 0, 0, -1, -1, 0, 0, 1])


# From https://www.flickr.com/photos/seadog-images/3591881376/
# cardinals  = np.arange(0, 361, 45)
# deviations = np.array([1, 1.5, 1, 1, 1, 1.5, 1, 0, 1])



# From http://code7700.com/images/compass_correction_card_afm_51-37_figure_1-15.png
# cardinals  = np.arange(0, 361, 15)
# deviations = np.array([1, 1, 1, 1, 2, 2, 2, 2, 2, 0, -1, -1, -1, -1, -1, -1,-2, -2, -2, -2, -2, -1, 0, 1, 1])
