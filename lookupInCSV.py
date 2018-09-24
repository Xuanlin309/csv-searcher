import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import math
import os
from tkinter import ttk

#create root instance
root = tk.Tk()
root.title("CSV Searcher")
#root.geometry('500x250')

#initialize number of search terms
searchTermCount = 0


class SearchUtils:
    def __init__(self):
        self.entryList = []
        self.checkList = []
        self.varCheckList = []
        self.searchTermCount = 0
        self.searchList = []
        self.path = ""

    # get the folder with all the CSVs; pass in label used to display folder name
    def getFolder(self, label):
        csvFlag = False
        folder =  filedialog.askdirectory()
        #check that there are CSVs present in folder
        for f in os.listdir(folder):
            if f.endswith(".csv"):
                csvFlag = True
                break
        if not csvFlag:
            messagebox.showerror("Error", "Directory must contain at least one CSV file to search")
            return
        label.config(text="Folder Path: " + folder)
        self.path = folder

    #change number of search terms and search entry fields when new number inputted
    def updateNoSearches(self, num):
        if not self.checkSubmit(num):
            return

        num = int(num)
        #need to remove fields?
        if num < self.searchTermCount:
            #destroy entry fields not needed and delete from entryList
            for i in range(1, (self.searchTermCount-num)*2 + 1):
                self.entryList[self.searchTermCount*2-i].destroy()
                del self.entryList[self.searchTermCount*2-i]
            #destroy unneeded checkboxes and delete them from checkList and varCheckList
            for i in range(1, self.searchTermCount-num + 1):
                self.checkList[self.searchTermCount-i].destroy()
                del self.checkList[self.searchTermCount-i]
                del self.varCheckList[self.searchTermCount-i]

        #need to add fields?
        elif num > self.searchTermCount:
            #add necessary elements
            for i in range(self.searchTermCount, num):
                #entry fields
                self.entryList.append(tk.Entry(root, justify='center'))
                self.entryList.append(tk.Entry(root, justify='center'))
                #checkboxes
                var = tk.IntVar()
                self.checkList.append(tk.Checkbutton(root, variable = var))
                self.varCheckList.append(var)

            #visually place entries
            for i in range(len(self.entryList)):
                self.entryList[i].grid(row = math.floor((i+8)/2), column = i % 2, pady = 2, padx = 10)

            #visually place checkboxes
            for i in range(len(self.checkList)):
                self.checkList[i].grid(row = i + 4, column = 2, pady = 2, padx = 10)

        s.searchTermCount = num
        #update search button position
        actionButton.grid(row = s.searchTermCount + 5, column = 1, pady = 5)




    # populate searchList with lists, each containing ColumnName, SearchString, DoesNotContain
    def makeSearchList(self):
        self.searchList = []
        #populate initial two fields of each list: ColumnName and SearchString
        for i in range(0, len(self.entryList), 2):
            self.searchList.append([self.entryList[i].get(), self.entryList[i+1].get()])
        #populate state of DoesNotContain (if looking for NOT CONTAINS, this will be a 1. Else, 0)
        for i in range(0, len(self.checkList)):
            self.searchList[i].append(self.varCheckList[i].get())

    #check to make sure number of entries that customer wants is valid
    def checkSubmit(self, num):
        # check to make sure number of search criteria is a digit
        if not num.isdigit():
            messagebox.showerror("Error", "Number of entries must be a positive integer")
            return(False)
        else:
            #convert number to int, as it was confirmed to be an int above
            num = int(num)
            #check that input is within acceptable range for number of entries
            if num < 1 or num > 10:
                messagebox.showerror("Error", "Number of criteria must be greater than 0 and no greater than 10")
                return(False)
        return(True)


    #check to make sure all entries are filled, directory path specified, etc
    def checkEntries(self):
        #have you specified a directory path to search?
        if self.path == "":
            messagebox.showerror("Error", "No directory path specified")
            return(False)
        #have you created search entries?
        if len(self.entryList) == 0:
            messagebox.showerror("Error", "Must have filled entries")
            return(False)
        #have you filled all entries?
        for i in self.entryList:
            if i.get() == "":
                messagebox.showerror("Error", "Not all entries are filled")
                return(False)
        return(True)


    # run the search file in this directory that is specified
    def runSearch(self):
        #check to make sure all entries are filled.  If not, don't search
        if not self.checkEntries():
            return
        #make progress bar
        progressWindow = tk.Toplevel()
        progressBar = ttk.Progressbar(progressWindow, mode='indeterminate')
        progLabel = tk.Label(progressWindow, text="Searching CSVs", justify='center')
        progressWindow.pack_slaves()
        progLabel.pack(fill='x', side='top')
        progressBar.pack(fill='x',side='bottom')
        progressBar.start()
        progressWindow.update()

        #run search
        self.makeSearchList()
        from searchFunction import searchCSVS
        searchCSVS(self.path, self.searchList)

        #destroy progress bar
        progressWindow.destroy()

    #determines what happens if increaseButton clicked (increase number
    #of search criteria by one)
    def increaseClick(self):
        if self.searchTermCount < 10:
            #entryList
            self.entryList.append(tk.Entry(root, justify='center'))
            self.entryList.append(tk.Entry(root, justify='center'))
            #update searchTermCount
            self.searchTermCount += 1
            #checkbox
            var = tk.IntVar()
            self.checkList.append(tk.Checkbutton(root, variable = var))
            self.varCheckList.append(var)
            #place on grid visually
            self.entryList[len(self.entryList)-2].grid(row = math.floor(len(self.entryList)/2)+3, column = len(self.entryList) % 2, pady = 2, padx = 10)
            self.entryList[len(self.entryList)-1].grid(row = math.floor(len(self.entryList)/2)+3, column = (len(self.entryList)+1) % 2, pady = 2, padx = 10)
            self.checkList[self.searchTermCount-1].grid(row = self.searchTermCount-1 + 4, column = 2, pady = 2, padx = 10)
            #update number in Entry field
            stringEntry.delete(0, tk.END)
            stringEntry.insert(0, self.searchTermCount)
            #update search button position
            actionButton.grid(row = s.searchTermCount + 5, column = 1, pady = 5)

    #determines what happens if decreaseButton clicked (decrease number
    #of search criteria by one, if possible)
    def decreaseClick(self):
        if self.searchTermCount > 1:
            self.searchTermCount -= 1
            #destroy lastmost entry forms
            self.entryList[len(self.entryList)-1].destroy()
            self.entryList[len(self.entryList)-2].destroy()
            #remove lastmost entry forms from list
            del self.entryList[len(self.entryList)-1]
            del self.entryList[len(self.entryList)-1]
            #remove checkboxes
            self.checkList[len(self.checkList)-1].destroy()
            del self.checkList[len(self.checkList)-1]
            del self.varCheckList[len(self.varCheckList)-1]
            #update number in Entry field
            stringEntry.delete(0, tk.END)
            stringEntry.insert(0, self.searchTermCount)
            #update search button position
            actionButton.grid(row = s.searchTermCount + 5, column = 1, pady = 5)




#--------------------------------------------------------------------------------

s = SearchUtils()

folderName = tk.Label(root, text="Folder Path: ")
folderName.grid(row=0, column = 0, columnspan = 3)

# button requesting folder with CSVs. Refers back to getFolder function to update
getFolderButton = tk.Button(root, text="Select folder with CSVs you'd like to search", command= lambda: s.getFolder(folderName))
getFolderButton.grid(row = 1, column = 0, columnspan = 3)

# how many strings will we search for?
stringCountLabel = tk.Label(root, text="How many strings/columns would you like to search for?").grid(row = 2, column=0)
stringEntry = tk.Entry(root, justify='center')
stringEntry.grid(row = 2, column = 1)
bFrame = tk.Frame(root)
decreaseButton = tk.Button(bFrame, text="-", command=s.decreaseClick)
increaseButton = tk.Button(bFrame, text="+", command = s.increaseClick)
stringSubmit = tk.Button(bFrame, text="Submit", command= lambda: s.updateNoSearches(stringEntry.get()))

#visual layout settings for buttons that regulate number of search terms
bFrame.grid(row=2, column=2, sticky='nsew')
decreaseButton.pack(side='left')
increaseButton.pack(side='left')
stringSubmit.pack(side='left')

#create labels for search criteria entry
colNamesLabel = tk.Label(root, text="Column Names:").grid(row=3, column=0, pady=10, padx = 10)
stringToSearchLabel = tk.Label(root, text="String to Search:").grid(row=3, column=1, pady=10, padx = 10)
doesNotContainLabel = tk.Label(root, text="Does Not Contain:").grid(row=3, column=2, pady=10, padx = 10)

#defines button that calls to search CSVs (default row = 5)
actionButton = tk.Button(root, text="Search!", command=s.runSearch)
actionButton.grid(row = 5, column = 1, pady = 5)



root.mainloop()
