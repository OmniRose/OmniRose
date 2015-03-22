import numpy

# Curve equations - which one is used depends on the number of points available
# to plot to. There must be more points than there are variables.
def _raw_curve_equation_3(heading, A, B, C):
    return _raw_curve_equation_generic(heading, A, B, C)

def _raw_curve_equation_5(heading, A, B, C, D, E):
    return _raw_curve_equation_generic(heading, A, B, C, D, E)

def _raw_curve_equation_7(heading, A, B, C, D, E, F, G):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G)

def _raw_curve_equation_9(heading, A, B, C, D, E, F, G, H, I):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G, H, I)

def _raw_curve_equation_11(heading, A, B, C, D, E, F, G, H, I, J, K):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G, H, I, J, K)

def _raw_curve_equation_13(heading, A, B, C, D, E, F, G, H, I, J, K, L, M):
    return _raw_curve_equation_generic(heading, A, B, C, D, E, F, G, H, I, J, K, L, M)

def _raw_curve_equation_generic(heading, A, *args):
    heading_in_radians = numpy.radians(heading)

    result = A

    multiplier = 1

    while len(args):
        result = result + args[0] * numpy.sin(multiplier * heading_in_radians)
        result = result + args[1] * numpy.cos(multiplier * heading_in_radians)

        args = numpy.delete(args, [0,1])
        multiplier = multiplier + 1

    return result

all_equations = (
    {
        'slug': 'trig_13',
        'points_needed': 13,
        'name': '13 variable trig curve',
        'equation': _raw_curve_equation_13,
    },
    {
        'slug': 'trig_11',
        'points_needed': 11,
        'name': '11 variable trig curve',
        'equation': _raw_curve_equation_11,
    },
    {
        'slug': 'trig_9',
        'points_needed': 9,
        'name': '9 variable trig curve',
        'equation': _raw_curve_equation_9,
    },
    {
        'slug': 'trig_7',
        'points_needed': 7,
        'name': '7 variable trig curve',
        'equation': _raw_curve_equation_7,
    },
    {
        'slug': 'trig_5',
        'points_needed': 5,
        'name': '5 variable trig curve',
        'equation': _raw_curve_equation_5,
    },
    {
        'slug': 'trig_3',
        'points_needed': 3,
        'name': '3 variable trig curve',
        'equation': _raw_curve_equation_3,
    },
)

