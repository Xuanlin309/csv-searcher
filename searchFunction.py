import os
from pandas import DataFrame, read_csv, Series
import time
import datetime

# search all CSVs in given directory, returning CSV matching criteria from
# given searchList
def searchCSVS(dirpath, searchList):

    # variable to check if header already written to CSV file
    headerWritten = False

    #create directory for outputs, if one doesn't already exist.
    currPath = os.getcwd()
    if not os.path.exists(os.path.join(currPath, "Outputs")):
        os.mkdir(os.path.join(currPath, "Outputs"))

    # Start time for checking runtime
    start = time.time()

    #set encoding for CSV files based on OS
    if os.name == 'posix':
        enc = 'latin-1'
    else:
        enc = 'utf-8-sig'

    #gets currrent date and time to be used in naming output file
    dater = datetime.datetime.now()
    outName = dater.strftime("%m%d%Y %H%M %S") + "output.csv"

    #open output dataframe
    output = DataFrame()

    #for each CSV file in directory
    for f in os.listdir(dirpath):
        filePath = os.path.join(dirpath, f)
        if f.endswith('.csv') and os.stat(filePath).st_size != 0:
            #open for reading
            fileDataframe = read_csv(f, index_col=None)

            tempdf = DataFrame()

            # for row in file:
            for row in fileDataframe.itertuples(index=False):
                for i in searchList:
                    for j in range(len(fileDataframe.columns)):
                        if i[0] == list(fileDataframe)[j]:
                            col = j
                            if i[2] == 0 and str(i[1]) == str(row[col]) \
                            or i[2] == 1 and str(i[1]) != str(row[col]):
                                tempdf = tempdf.append(Series(list(row)), ignore_index=True)

            output = output.append(tempdf)

    #rename headers to match input headers if header hasn't already been updated
    #and data exists.  Drop duplicates if data exists
    if len(output) > 0:
        if not headerWritten:
            output.columns = list(fileDataframe.columns.values)
            headerWritten = True
        output.drop_duplicates(subset=None, inplace=True)
    output.to_csv(outName, index=False)

    #rename path for file
    os.rename(os.path.join(currPath, outName), os.path.join(currPath, "Outputs", outName))

    #Print runtime
    end = time.time()
    print("Time Elapsed: " + str(end-start) + " seconds")

    print("Search Complete")
