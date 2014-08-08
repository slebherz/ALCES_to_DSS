from hec.script import *
from hec.heclib.dss import *
from hec.heclib.util import *
from hec.io import *
import java
import string
import os

"""
    This script accepts as input ALCES model output in an expected csv format (see
    below) and imports it into a HEC-DSS database.

    Command Format:
    [Path to HEC-DSSVue exe] [Path to .py script] 
        [Path to ALCES output .csv] [Path to ALCES output .dss] [Path to log .txt] [ALCES Simulation Name]

    Input File Format:
    ,<SIM_NAME>,...,<SIM_NAME>
    ,<VAR_NAME>,...,<VAR_NAME>
    <TIMESTEP_1>,<TS1_VAL1>,...,<TSN_VAL1>
    ...
    <TIMESTEP_X>,<TS1_VAL1>,...,<TSN_VAL1>
    
    Sample Input:
    ,sim1,sim1,sim1,sim1,sim1
    ,80101,80102,80103,802,803
    1,0.1,0.1,0.1,0.1,0.1
    2,0.1,0.1,0.1,0.1,0.1
    
    Sample Output:
    DSS file with series:
        /sim1/80101/ALCES//1DAY//
        /sim1/80102/ALCES//1DAY//
        /sim1/80103/ALCES//1DAY//
        /sim1/802/ALCES//1DAY//
        /sim1/803/ALCES//1DAY//
"""
# Declare input/output paths.
inFilePath = os.path.normpath(sys.argv[1])
outFilePath = os.path.normpath(sys.argv[2])

# Declare common start time and step.
start = HecTime("01Jan1950", "2400")
step = 1440 # minutes per day

# Initialize a log file.
log = ""
logFilePath = os.path.normpath(sys.argv[3])
logF = open(logFilePath, 'a')
log += "Input: " + inFilePath + "\n"

alcesSimulationName = sys.argv[4]

if(os.path.isfile(inFilePath)):
    # Extract all lines from the output file.
    lines = [line.strip().split(',') for line in open(inFilePath, 'r') if len(line.strip()) > 0]
    # Extract the header line (the [1:] is to ignore the timestep # column).
    seriesNames = [name.strip('"') for name in lines[0][1:]]
    # Initialize an empty list to store each series.
    allSeries = [[] for i in range(0,len(seriesNames))]
    # The times will be shared among all the series.
    times = []
    
    # Each line contains a value for each series at a single timestep.
    # Add each value to a list of values for each series.
    for line in lines[1:]: # [1:] ignores one header row
        for idx, value in enumerate(line[1:]): # [1:] ignores the timestep # column
            allSeries[idx].append(float(value))
        # While parsing through the input we may as well build a list of times.
        times.append(start.value())
        start.add(step)
    
    # Prepare the dss file to be written.
    outDSS = HecDss.open(outFilePath)
    log += "Output: " + outFilePath + "\n"
    
    # Add a series for each ALCES output series.
    for series_name, series in zip(seriesNames, allSeries):
        # Build and initialize the HEC-DSS object that stores the series.
        tsc = TimeSeriesContainer()
        # Full DSS Path: //[Series Name]/[Sim Name]//1DAY//
        tsc.fullName = "//" + series_name + "/" + alcesSimulationName + "//1DAY//"
        tsc.interval = step
        tsc.times = times
        tsc.values = series
        tsc.numberValues = len(series)
        tsc.units = "CMS"
        tsc.type = "PER-CUM"
        outDSS.put(tsc)
        log += "   Added " + tsc.fullName + " (" + str(len(tsc.values)) + " values)\n"
    outDSS.close()
else:
    log += "ERROR: Could not find input file\n"
logF.write(log)
logF.close()