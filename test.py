from lsd.dataset import LargeDataSet
from lsd.plotter import Plot
from lsd.sheets import *
from lsd.columns import *
import numpy as np
from statistics import stdev
import matplotlib.pyplot as plt

Plot(CAMBORNE_1987, CAMBORNE_2015).hist(MEAN_TEMPERATURE)
#Plot(JACKSONVILLE_1987, JACKSONVILLE_2015).scatter(DATE, MEAN_TEMPERATURE, lineOfBestFit=True, deg=3)