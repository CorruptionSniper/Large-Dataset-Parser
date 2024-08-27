from lsd.dataset import LargeDataSet
from lsd.plotter import Plot
from lsd.sheets import *
from lsd.columns import *
import numpy as np
from statistics import stdev
import matplotlib.pyplot as plt

#sheets = [CAMBORNE_2015]
#x = MAX_GUST_CARDINAL_DIRECTION
#print(*[data for data in LargeDataSet(sheets, columns=x)[*sheets]])
Plot(CAMBORNE_2015).hist(MAX_GUST_CARDINAL_DIRECTION)
#Plot(JACKSONVILLE_1987, JACKSONVILLE_2015).scatter(DATE, MEAN_TEMPERATURE, lineOfBestFit=True, deg=3)