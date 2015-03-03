# samples of various deviation tables

from .models import Curve

def create_curve_from_sample(sample):
    curve = Curve.objects.create()
    for ships_head, deviation in sample.items():
        curve.reading_set.create(ships_head=ships_head, deviation=deviation)
    return curve

rya_training_almanac = {
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
