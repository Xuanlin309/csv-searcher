# csv-searcher
Automatically search all CSVs in a directory for a set of search criteria, compiling results into an output CSV.

Important Notes:

    You must download Python 3 and the pandas library to run this software
  
    When inputting multiple search criteria, keep in mind that the software searches for criteria as OR statements, meaning that a search for name XYZ and NOT age 123 will return all results with EITHER name XYZ or not age 123
  
    Currently can only handle CSVs with the same columns and number of columns--a fix is in progress
    
    When the code finishes running, an Outputs folder will be created in the directory where you downloaded the source files
    (if one does not already exist). Output files will automatically be stored here.
 
To use:

    Download the files and run lookupInCSV.py (I typically use the command line/Terminal)

Please submit any issues encountered and fixes will be worked on promptly.
