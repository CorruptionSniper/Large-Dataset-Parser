from lsd.dataset import LargeDataSet
from lsd.plotter import Plot
from lsd.sheets import *
from lsd.columns import *
import numpy as np

Plot(BEIJING_1987, BEIJING_2015).boxPlot(MEAN_WIND_SPEED)