import plotter as pt
from .dataset import *
from .sheets import SHEET_NAMES
from .columns import *

class Plot():
    def __init__(self, *sheets):
        self.sheets = sheets
        self.TITLE_FUNC = lambda title: title or " vs. ".join([SHEET_NAMES[sheet][-4:]  
                                                                            if prevSheet is not None and SHEET_NAMES[sheet][:-5] == SHEET_NAMES[prevSheet][:-5] 
                                                                            else SHEET_NAMES[sheet]
                                                                            for sheet, prevSheet
                                                                            in zip(self.sheets, [None] + list(self.sheets[:-1]))])

    def scatter(self, x, y, title=None, lineOfBestFit=False, deg=1):
        p = pt.Plot(COLUMN_NAMES[x], COLUMN_NAMES[y], self.TITLE_FUNC(title))
        p.scatter(*[[SHEET_NAMES[sheetI], *sheet[x, y]] 
                      for sheetI, sheet 
                      in zip(self.sheets, LargeDataSet(self.sheets, columns=[x,y]))], lineOfBestFit=lineOfBestFit, deg=deg, normaliseDates=(len(self.sheets) > 1))

    def lineGraph(self, x, y, title=None):
        p = pt.Plot(COLUMN_NAMES[x], COLUMN_NAMES[y], title=title or self.TITLE_FUNC(title))
        p.lineGraph(*[[SHEET_NAMES[sheetI], *sheet[x, y]] 
                      for sheetI, sheet 
                      in zip(self.sheets, LargeDataSet(self.sheets, columns=[x,y]))], normaliseDates=(len(self.sheets) > 1))

    def hist(self, x, title=None, measure="density", binMode="balanced", bins=None):
        ds = LargeDataSet(self.sheets, columns=x)
        p = pt.Plot(COLUMN_NAMES[x], title=self.TITLE_FUNC(title) or SHEET_NAMES[self.sheets[0]])
        p.hist(*[ds[sheet][x] for sheet in self.sheets], 
               subPlotTitles=[SHEET_NAMES[sheet] for sheet in self.sheets],
               order=(BEAUFORT_SCALE if x == MEAN_WIND_SPEED_BC
            else (CARDINAL_DIRECTIONS if MEAN_WIND_CARDINAL_DIRECTION or MAX_GUST_CARDINAL_DIRECTION 
            else None)), measure=measure, binMode=binMode, bins=bins)

    def boxPlot(self, x, tickInterval=None, tickOffset=0, title=None, removalCondition=None):
        ds = LargeDataSet(self.sheets, columns=x)
        p = pt.Plot(COLUMN_NAMES[x], "Location", title or "")
        p.boxPlot(*[[sheet.getName(), sheet[x]] for sheet in (ds[sheet] for sheet in self.sheets)], tickInterval=tickInterval, tickOffset=tickOffset, removalCondition=removalCondition)