::
:: This batch file runs the ALCES to DSS conversion program.
::
:: Command Format: [Path to HEC-DSSVue exe] [Path to .py script]
::      [Path to ALCES output .csv] [Path to ALCES output .dss] [Path to log .txt]
::
:: The ALCES output .dss file and the log .txt file will be created or overwritten.
::
:: Critical: in Python, "\a" is a special character sequence. If the script encounters
:: "\a" in a path then it will fail. So don't call the ALCES csv file anything that
:: starts with 'a' otherwise you'll end up with a path containing "\a" and the program
:: will fail.
::      Good: _alces.csv <-- the path is C:\whatever\_alces.csv
::       Bad:  alces.csv <-- the path is C:\whatever\alces.csv (see the "\a"?)
::

:: Assumes that the script, input, output, and log should all be read/written from
:: the same directory.
set "CommonPath=E:\Code\import_alces_to_dss\"

"C:\Program Files (x86)\HEC\HEC-DSSVue\HEC-DSSVue.exe" ^
    "%CommonPath%import_alces_to_dss.py" ^
        "%CommonPath%_alces.csv" ^
        "%CommonPath%_alces.dss" ^
        "%CommonPath%log.txt"
        