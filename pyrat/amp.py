from numpy import mean as np_mean
from numpy import abs as np_abs


def normalize(a):
    '''
    Normalize the input (numpy array).
    '''

    return (a - np_mean(a))/np_abs(a).max()
