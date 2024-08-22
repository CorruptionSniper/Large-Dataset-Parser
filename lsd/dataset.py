from .sheets import *
from .columns import *
import pandas as pd
import numpy as np
from statistics import stdev

def quartiles(arr):
    sArr = sorted(arr)
    lq, med, uq = sArr[len(sArr)//4], sArr[len(sArr)//2], sArr[len(sArr)*3//4]
    iqr = uq - lq
    lb, ub = [sArr[max(np.searchsorted(sArr, loc) - 1, 0)] for loc in [lq - 1.5*iqr, uq + 1.5*iqr]]
    return [lb, lq, med, uq, ub]

def mode(arr):
    valCount = {}
    for val in arr:
        if val not in valCount:
            valCount[val] = 1
        else:
            valCount[val] += 1
    maxCount, modeVals = 0, [None]
    for val, count in valCount.items():
        if count > maxCount:
            maxCount, modeVals = count, [val]
        elif count == maxCount:
            modeVals.append(val)
    return modeVals if len(modeVals) > 1 else modeVals[0]

class LargeDataSet():
    OVERSEAS_COLUMN_VARS = [DATE, MEAN_TEMPERATURE, RAINFALL, MEAN_PRESSURE, MEAN_WIND_SPEED, MEAN_WIND_SPEED_BC]
    OVERSEAS_COLUMN_INDEX_DICT = {var:i for i, var in enumerate(OVERSEAS_COLUMN_VARS)}

    def __init__(self, sheets=None, columns=None):
        if sheets is None:
            sheets = [x for x in range(1,17)]
        elif isinstance(sheets, (tuple, list)):
            sheets = [x + 1 for x in sorted(sheets)]
        elif isinstance(sheets, int):
            sheets = [sheets + 1]
        if isinstance(columns, int):
            columns = [columns]
        i = 0
        for i, sheet in enumerate(sheets):
            if sheet >= BEIJING_1987:
                break
        ukSheets, overseasSheets = sheets[:i], sheets[i:]
        converters = {2 if columns is None else len([x for x in columns[:3] if x in [0,1]]):
                      lambda x:x if x != "tr" else 0.025} if columns is None or 2 in columns else None
        overseasColumns = [self.OVERSEAS_COLUMN_INDEX_DICT[column] 
                           for column in columns 
                           if column in self.OVERSEAS_COLUMN_INDEX_DICT
                           ] if columns is not None else list(self.OVERSEAS_COLUMN_INDEX_DICT.values())
        ukData = pd.read_excel("lsd/LDS.xlsx", 
                            sheet_name=ukSheets, usecols=columns, 
                            header=0, skiprows=6, skipfooter=4, 
                            converters=converters) if ukSheets else None
        overseasData = pd.read_excel("lsd/LDS.xlsx", 
                            sheet_name=overseasSheets, usecols=overseasColumns, 
                            header=0, skiprows=6, skipfooter=4,
                            converters=converters) if overseasSheets else None
        self.sheets = [None]*len(SHEET_NAMES)
        overseasColumns = [self.OVERSEAS_COLUMN_VARS[i] for i in overseasColumns]
        for sheetI, dataFrame in ukData.items() if ukData else []:
            sheetI -= 1
            self.sheets[sheetI] = Sheet(dataFrame, SHEET_NAMES[sheetI], columns)
        for sheetI, dataFrame in overseasData.items() if overseasData else []:
            sheetI -= 1
            self.sheets[sheetI] = Sheet(dataFrame, SHEET_NAMES[sheetI], overseasColumns)

    def __len__(self):
        return len([s for s in self.sheets if s is not None])

    def statistics(self, *sheets):
        if not len(sheets):
            sheets = (i for i, sheet in enumerate(self.sheets) if sheet is not None)
        return {self.sheets[i].getName():self.sheets[i].statistics() for i in sheets}

    def __getitem__(self, *args):
        while not (len(args) != 1 or isinstance(args[0], int)): 
            args = args[0]
        return self.sheets[args[0]] if len(args) == 1 else [self.sheets[arg] for arg in args if self.sheets[arg] is not None]

    def __str__(self):
        return str(self.sheets)

    def __iter__(self):
        return (sheet for sheet in self.sheets if sheet is not None)

class Sheet():
    def __init__(self, dataFrame, name=None, columns=None, columnNames=COLUMN_NAMES):
        dataFrame.rename({oldName:columnNames[i] for i, oldName in zip(columns or list(range(len(dataFrame.columns))), dataFrame.columns)}, axis='columns', inplace=True, errors='raise')
        self.data = {i:dataFrame.loc[:,name].to_numpy(copy=False) for i, name in enumerate(columnNames) if name in dataFrame.columns}
        self.name = name
        self.columnNames = columnNames

    def __getitem__(self, *args):
        if isinstance(s := args[0], slice):
            args = [[i for i in 
                        range(*[arg for arg in 
                            [*[s.start or 0, len(self.columnNames) if s.stop is None else s.stop][::-1 if s.step and s.step < 0 else 1], 
                             1 if s.step is None else s.step]])
                        if i in self.data]]
        if isinstance(l := args[0], (tuple, list)):
            vals = [self.data[arg] if arg in self.data else None for arg in l]
            return vals[0] if len(args[0]) == 1 else vals
        return self.data[args[0]] if args[0] in self.data else None

    def getName(self):
        return self.name
    
    def statistics(self, *columns):
        if not len(columns):
            columns = sorted(self.data.keys())
        return {COLUMN_NAMES[i]:(({"mean":np.mean(columnData), "standard deviation":stdev(columnData),
                                } | {var:val for var, val in zip(
                                    ["lower bound", "lower quartile", "median", "upper quartile", "upper bound"], 
                                    quartiles(columnData))}) 
                                    if "datetime" not in str(columnData.dtype) else 
                                    {"lower bound":str(columnData.min()), "upper bound":str(columnData.max())})
                                    if "object" not in str(columnData.dtype) else 
                                    {"mode":mode(columnData)}
                            for i, columnData
                            in ((column, self.data[column]) for column in columns)}

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.data)
    
    def __iter__(self):
        return (column for column in self.data.values())