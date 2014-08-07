:: Name of the ALCES simulation. Assumes that a directory exists in the Common Path
:: with this name that contains the yearly ALCES output.
set "ALCESSimulationName=scenario2"


::
:: This batch file runs the ALCES to DSS conversion program. It consists of two
:: scripts. The first script merges annual ALCES output into a single .csv. The
:: second script imports the merged series into a DSS database.
::
:: Script 1, the merge step.
:: Command Format: [Path to Python .exe] [Path to .py script (merge)]
::      [Path to ALCES output directory] [Path to merged ALCES output .csv]
::
:: Script 2, the dss import step.
:: Command Format: [Path to HEC-DSSVue .exe] [Path to .py script (dss import)]
::      [Path to ALCES output .csv] [Path to ALCES output .dss] [Path to log .txt]
::
:: The ALCES output .csv file, .dss file, and the log .txt file will be created or overwritten.
::
:: Critical: in Python, "\a" is a special character sequence. If the script encounters
:: "\a" in a path then it will fail. So don't call the ALCES csv file anything that
:: starts with 'a' otherwise you'll end up with a path containing "\a" and the program
:: will fail.
::      Good: _alces.csv <-- the path is C:\whatever\_alces.csv
::       Bad:  alces.csv <-- the path is C:\whatever\alces.csv (see the "\a"?)
::

echo off
cls

::
:: Make sure the paths set below are correct:
::

:: Path to HEC-DSSVue executable
set "HECDSSVueExePath=C:\Program Files (x86)\HEC\HEC-DSSVue\HEC-DSSVue.exe"

:: Path to Python executable
set "PythonExePath=C:\Python33\python.exe"

:: Assumes that the script, input directory, output, and log should all be read/written from
:: the same directory.
set "CommonPath=E:\Code\import_alces_to_dss"

echo Merging ALCES yearly output into a single timeseries.

:: Perform a merge step that merges the annual ALCES output into a single timeseries.
:: Assumes Python is installed and is present in the Windows Path Environment Variable.
"%PythonExePath%" "%CommonPath%\merge_alces_output.py" ^
    "%CommonPath%\%ALCESSimulationName%" ^
    "%CommonPath%\%ALCESSimulationName%\%ALCESSimulationName%.csv" ^
    "%CommonPath%\%ALCESSimulationName%.log.txt"

:: If the merge step was unsucessful then inform the user and exit.
if %ErrorLevel% neq 0 (
    echo Could not merge ALCES output. Exiting...
    pause
)

echo Importing ALCES output into DSS.

:: Have HEC-DSSVue invoke the script that imports the merged timeseries into DSS.
"%HECDSSVueExePath%" "%CommonPath%\import_alces_to_dss.py" ^
    "%CommonPath%\%ALCESSimulationName%\%ALCESSimulationName%.csv" ^
    "%CommonPath%\_alces.dss" ^
    "%CommonPath%\%ALCESSimulationName%.log.txt" ^
    "%ALCESSimulationName%"

echo Import Complete
pause