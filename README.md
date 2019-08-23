# Roast-Report-Tool



This is a simple tool that logs into your Roastlog account, scrapes data from your roast pages, reads in data from csv files, and outputs some reports and visualizations.

You will need to have a valid Roastlog account for this to work properly.

## Converting to Executable

I was able to convert the program to an executable file using PyInstaller in my Anaconda Prompt using the following command:

```
C:\file_path> pyinstaller --onefile GUI.py --exclude-module PyQt5
```

Where file_path is the location of GUI.py and all other python files found in this repository. GUI.py is the entry point for the program, so if you tell PyInstaller where it is, and the other files are placed appropriately, it will include the rest of the python files in the executable.
