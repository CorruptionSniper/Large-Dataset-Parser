import matplotlib.pyplot as plt
import matplotlib.patches as mpat
import numpy as np
from numpy.polynomial.polynomial import Polynomial, polyval
from math import sqrt, ceil, floor

class Plot():
    def __init__(self, xLabel=None, yLabel=None, title=None, **kwargs):
        self.figure = plt.figure(**kwargs)
        if title:
            plt.suptitle(title)
        if xLabel:
            plt.xlabel(xLabel)
        if yLabel:
            plt.ylabel(yLabel)
        self.xLabel = xLabel
        self.yLabel = yLabel
        self.legendArgs = []


    def scatter(self, *graphs, lineOfBestFit=False, deg=1, normaliseDates=False):
        graphs = list(graphs)
        if normaliseDates and "datetime" in str(graphs[0][1].dtype):
                for i, lxy in enumerate(graphs):
                    graphs[i][1] = self.__normaliseDateArray(lxy[1])
        for label, x, y in graphs:
            x, y = self.__removeNaNValues(x, y)
            g = plt.plot(x, y, '.')
            self.__addToLegend(g, label)
            if lineOfBestFit:
                if "datetime" in str(y.dtype):
                    raise Exception("INVALID OPERATION: Cannot plot line of best fit using datetime object as y variable, only valid for x variable.")
                normalisedX = x if "datetime" not in str(x.dtype) else x.astype(np.float64)
                coeffs = Polynomial.fit(normalisedX, y, deg=deg).convert().coef
                lOBF = plt.plot(x, polyval(normalisedX, coeffs))
                self.__addToLegend(lOBF, f"{label} LOBF")
        self.__showLegent()
        plt.show()

    def lineGraph(self, *graphs, normaliseDates=False):
        graphs = list(graphs)
        if normaliseDates and "datetime" in str(graphs[0][1].dtype):
                for i, xy in enumerate(graphs):
                    graphs[i][1] = self.__normaliseDateArray(xy[1])
        for label, x, y in graphs:
            g = plt.plot(x, y)
            self.__addToLegend(g, label)
        self.__showLegent()
        plt.show()

    def hist(self, *vals, subPlotTitles=[], measure="density", bins=None, binMode="balanced", order=None):
        vals = list(vals)
        subPlotTitles = subPlotTitles[::-1]
        binFunc = None
        xTicks = None
        if measure not in ["density", "den", "d", "frequency", "freq", "f"]:
            raise Exception("Uknown measure: measure can either be 'frequency' or 'density' - Check documentation for details.")
        if str(vals[0].dtype) != 'object':
            if binMode in ['balanced', 'bal', 'b']:
                binFunc = lambda v:(len(v)//(bins or 10)) or 1
            elif binMode in ['interval', 'int', 'i']:
                binFunc = lambda v:round((max(v) - min(v))/(bins or 1)) or 1
            elif binMode not in ['number', 'num', 'n']:
                raise Exception("Uknown binMode: binMode can be either 'balanced', 'interval' or 'number' - Check documentation for details.")
        else:
            if order is None:
                raise Exception("Missing argument: order must be provided for histograms of non-numerical data.")
            toIDict = {val:i for i, val in enumerate(order)}
            binFunc = lambda v:np.arange(len(order) + 1) - 0.5
            xTicks = np.arange(0, len(order)), [str(val) for val in order]
            for i, arr in enumerate(vals):
                vals[i] = np.asarray([toIDict[val] for val in arr if val in toIDict], dtype=int)

        for axis in self.figure.get_axes():
            axis.set_visible(False)
        self.yLabel = "Frequency" + " Density"*(measure in "density")
        self.figure.text(0.05, 0.5, self.yLabel, va='center', rotation='vertical')
        self.figure.text(0.5, 0.05, self.xLabel, ha='center')
        rows = floor(sqrt(len(vals))) or 1
        columns = ceil(len(vals)/rows)
        subAxs = self.figure.subplots(rows, columns, sharey=True, squeeze=False)
        for i in range(rows):
            for j in range(columns):
                cVals = vals[j*rows + i]
                weights = [1/len(cVals) if measure == "density" else 1]*len(cVals)
                subAxs[i][j].hist(cVals, weights=weights, bins=(binFunc(cVals) if binFunc is not None else 20))
                subAxs[i][j].set_title(subPlotTitles.pop() if subPlotTitles else "")
                if xTicks:
                    subAxs[i][j].set_xticks(*xTicks)
        plt.show()

    def boxPlot(self, *varsArr, tickInterval=None, tickOffset=0):
        varsArr = list(varsArr)[::-1]
        for i, var in enumerate(varsArr):
            if str(var[1].dtype) in ['datetime64[ns]', 'object']:
                raise Exception(f"INVALID DATA TYPE: {str(var[1].dtype)} - Cannot boxplot an array of non-numeric data types.")
            varsArr[i][1] = self.__removeNaNValues(var[1])
        plt.boxplot([vals for label, vals in varsArr], vert=False)
        if tickInterval:
            l, h = min([min(vals) for label, vals in varsArr]), max([max(vals) for label, vals in varsArr])
            mid, span = (l + h)/2, h - l
            lb, ub = mid - span, mid + span
            n = (lb - tickOffset)//tickInterval
            lb = n*tickInterval + tickOffset
            plt.xticks(np.arange(lb, ub + 1, tickInterval))
        plt.yticks(np.arange(1, len(varsArr) + 1), [label for label, vals in varsArr])
        plt.grid()
        plt.tight_layout()
        plt.show()

    def __normaliseDateArray(self, dateArray):
        return np.asarray([np.datetime64('0001' + str(date)[4:10]) for date in dateArray], dtype=np.datetime64)

    def __addToLegend(self, plot, label):
        self.legendArgs.append(mpat.Patch(color=plot[0].get_color(), label=label))
        
    def __showLegent(self):
        plt.gca().legend(handles=self.legendArgs, loc="best", draggable=True)

    def __removeNaNValues(self, *args):
        if not args:
            return []
        nanRemovalArray = np.isnan(args[0])
        for var in args[1:]:
            nanRemovalArray |= np.isnan(var)
        nanRemovalArray = ~nanRemovalArray
        return args[0][nanRemovalArray] if len(args) == 1 else [var[nanRemovalArray] for var in args]