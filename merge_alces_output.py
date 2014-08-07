import os
import sys
import operator
import glob

# Initialize a log file.
log = ""
logFilePath = os.path.normpath(sys.argv[3])

# Declare input/output paths.
inputDir = os.path.normpath(sys.argv[1])
outFilePath = os.path.normpath(sys.argv[2])

# Abort if the input cannot be located.
if os.path.isdir(inputDir) == False:
    print("\tCould not locate " + inputDir)
    sys.exit(-1)
    
# Find all .csv files in the input directory (but ignore an output .csv if one
# has already been created by a previous execution of this script.
os.chdir(inputDir)
fNames = [os.path.join(inputDir, f) for f in glob.glob("*[0-9][0-9][0-9][0-9].csv")]
fNames = [f for f in fNames if os.path.isfile(f) and f != outFilePath]
# Create a sorted list of (year, file name) pairings.
pairings = [(fName.split('.')[0][-4:], fName) for fName in fNames]
pairings.sort(key=operator.itemgetter(0))

# Check if any years are missing from the input.
start = int(pairings[0][0])
expected = list(range(start, start + len(pairings)))
observed = [int(year) for (year, fName) in pairings]
diff = list(set(expected) - set(observed))
if(len(diff) > 0):
    print("\tYears are missing from the input: " + str(diff))
    sys.exit(-1)

# Merge all the files into a single collection
merged = []
log += "Merging\n"
for year, fName in pairings:
    log += "\t" + year + " - " + fName + "\n"
    # Extract all lines from the output file.
    lines = [line.strip() for line in open(fName, 'r') if len(line.strip()) > 0]
    header = lines[0]
    if(len(merged) == 0):
        merged.append(header)
    merged.extend(lines[1:])
# Write the merged content to a file.
with open(outFilePath, 'w') as outF:
    outF.write("\n".join(merged))
log += "Writing merged series to " + outFilePath + "\n"
# Write a log.
with open(logFilePath, 'w') as logF:
    logF.write(log)