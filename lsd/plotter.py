import plotter as pt
from .dataset import *
from .sheets import SHEET_NAMES
from .columns import *

class Plot():
    def __init__(self, *sheets):
        self.sheets = sheets
        self.SCATTER_LINE_TITLE_FUNC = lambda title: title or " vs. ".join([SHEET_NAMES[sheet][-4:]  
                                                                            if prevSheet is not None and SHEET_NAMES[sheet][:-5] == SHEET_NAMES[prevSheet][:-5] 
                                                                            else SHEET_NAMES[sheet]
                                                                            for sheet, prevSheet
                                                                            in zip(self.sheets, [None] + list(self.sheets[:-1]))])

    def scatter(self, x, y, title=None, lineOfBestFit=False, deg=1):
        p = pt.Plot(COLUMN_NAMES[x], COLUMN_NAMES[y], self.SCATTER_LINE_TITLE_FUNC(title))
        p.scatter(*[[SHEET_NAMES[sheetI], *sheet[x, y]] 
                      for sheetI, sheet 
                      in zip(self.sheets, LargeDataSet(self.sheets, columns=[x,y]))], lineOfBestFit=lineOfBestFit, deg=deg, normaliseDates=(len(self.sheets) > 1))

    def lineGraph(self, x, y, title=None):
        p = pt.Plot(COLUMN_NAMES[x], COLUMN_NAMES[y], title=title or self.SCATTER_LINE_TITLE_FUNC(title))
        p.lineGraph(*[[SHEET_NAMES[sheetI], *sheet[x, y]] 
                      for sheetI, sheet 
                      in zip(self.sheets, LargeDataSet(self.sheets, columns=[x,y]))], normaliseDates=(len(self.sheets) > 1))

    def hist(self, x, title=None):
        p = pt.Plot(COLUMN_NAMES[x], title=title or SHEET_NAMES[self.sheets[0]])
        p.hist(LargeDataSet(self.sheets, columns=x)[self.sheets][x], order=BEAUFORT_SCALE if x == MEAN_WIND_SPEED_BC 
                                                                        else CARDINAL_DIRECTIONS if MEAN_WIND_CARDINAL_DIRECTION or MAX_GUST_CARDINAL_DIRECTION 
                                                                        else None)

    def boxPlot(self, x, tickInterval=None, tickOffset=0, title=None):
        p = pt.Plot(COLUMN_NAMES[x], "Location", title or "")
        p.boxPlot(*[[sheet.getName(), sheet[x]] for sheet in LargeDataSet(self.sheets, columns=x)], tickInterval=tickInterval, tickOffset=tickOffset)