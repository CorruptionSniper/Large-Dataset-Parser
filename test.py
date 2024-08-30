from lsd.dataset import LargeDataSet
from lsd.plotter import Plot
from lsd.sheets import *
from lsd.columns import *
import numpy as np
from statistics import stdev
import matplotlib.pyplot as plt

removalCondition = lambda x:x <= 0.025
Plot(CAMBORNE_1987, CAMBORNE_2015, HEATHROW_1987, HEATHROW_2015, HURN_1987, HURN_2015, LEEMING_1987, LEEMING_2015, LEUCHARS_1987, LEUCHARS_2015).boxPlot(RAINFALL, removalCondition=removalCondition)
#Plot(JACKSONVILLE_1987, JACKSONVILLE_2015).scatter(DATE, MEAN_TEMPERATURE, lineOfBestFit=True, deg=3)