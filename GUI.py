import tkinter as tk
import tkinter.ttk as ttk
import threading
import datetime
from DeliverLogic import deliverPackages, getUIState

def control(btn,thread1,thread2):
    if btn["text"] == "Start" or btn["text"] == "Resume":
        if btn["text"] == "Start":
            disableTimeSearch()
            thread1.start()
            thread2.start()
        elif btn["text"] == "Resume":
            # Disable our time searching functions and reset the statuses if needed
            disableTimeSearch()
            if truckTopLF.cget("text") != "Trucks":
                resetStatusView()
        btn["text"] = "Pause"
    elif btn["text"] == "Pause":
        # Enable our time searching functions
        enableTimeSearch()
        btn["text"] = "Resume"
    elif btn["text"] == "Exit":
        root.destroy()

def enableTimeSearch():
    # Change focus
    controlBtn.focus()

    # Enable function to enter in a time to see package statuses
    timeViewBtn.config(state="normal")
    timeViewEntry.delete(0,tk.END)
    timeViewEntry.insert(0,"Enter time (H:M AM/PM)")
    timeViewEntry.config(state="normal")
    timeViewInfoLabel.grid_forget()

def disableTimeSearch():
    # change focus
    controlBtn.focus()

    # Disable our time searching functions
    timeViewBtn.config(state="disabled")
    timeViewEntry.delete(0,tk.END)
    timeViewEntry.insert(0,"Enter time (H:M AM/PM)")
    timeViewEntry.config(state="readonly")
    timeViewInfoLabel.config(text="Unable to search while \nprogram is running.")
    timeViewInfoLabel.grid(column=0,row=2)
    resetStatusViewBtn.grid_forget()

def clearEntry(event):
    if event.widget.get():
        event.widget.delete(0,tk.END)

def checkPackageStatus():
    # change focus to button widget
    timeViewBtn.focus()

    timeToSearch = timeViewEntry.get().casefold() # User inputted time
    uiState = getUIState(timeToSearch) # Key and dictionary of logged time (or closest entry)
    
    # Update UI
    truckTopLF.config(text=f"Viewing Package Statuses From {timeToSearch}",background="light yellow")
    truckWidgets = truckTopLF.winfo_children()
    for truckW in truckWidgets:
        for childW in truckW.winfo_children():
            if childW.winfo_name() in uiState.keys():
                childW.configure(text=f"{uiState[childW.winfo_name()]}") # type: ignore
    # Show and enable reset button
    resetStatusViewBtn.grid(column=0,row=2,sticky="ew",padx=3,pady=3)

def resetStatusView():
    currentState = getUIState(timeVal["text"].casefold()) # get current program time's most recent UI log

    # Restore UI
    truckTopLF.config(text="Trucks",background="light gray")
    truckWidgets = truckTopLF.winfo_children()
    for truckW in truckWidgets:
        for childW in truckW.winfo_children():
            if childW.winfo_name() in currentState.keys():
                childW.configure(text=f"{currentState[childW.winfo_name()]}") # type: ignore

    resetStatusViewBtn.grid_forget() 

def handleTimeViewBtn():
    # Switch focus to button widget
    timeViewBtn.focus()

    # Clear any previous search/highlights
    updatesArea.tag_remove("highlight","0.0",tk.END)
    
    # Store user's input
    timeInput = timeViewEntry.get().casefold()

    # Validate user input by attempting to format the entry as a datetime
    try:
        # This block will execute if the input is a valid time value
        validTimeInput = datetime.datetime.strptime(timeInput,"%H:%M %p")
        # Create highlight tag which will be applied to all occurences
        updatesArea.tag_config("highlight",background="yellow", foreground="black")
        
        # Search for packages with matching time
        numLines = int(updatesArea.index(tk.END).split(".")[0]) # E.g output of .index() can be "4.5" so splitting at the decimal gives us [4,5] 
                                                                # where 0th index is our number of lines 
        startIdx = updatesArea.search(timeInput,"0.0",tk.END,exact=False,nocase=True)
        for i in range(numLines-1):
            foundIdx = updatesArea.search(timeInput,f"{startIdx}+{i}l",f"{startIdx}+{i}l+{len(timeInput)+1}c",exact=False,nocase=True)

            # Apply highlight
            if foundIdx != "":
                updatesArea.tag_add("highlight",f"{foundIdx}-{1}c",f"{foundIdx}+{len(timeInput)+1}c")
        
        updatesArea.see(startIdx)
        timeViewInfoLabel.grid_forget()
    except Exception as e:
        # This block will execute if the input is not valid i.e not entering in a time
        timeViewInfoLabel.config(text="No packages delivered at that time.")
        timeViewInfoLabel.grid(column=0,row=2)

def handleEnterKey(event):
    checkPackageStatus()

def startGUI(truckList):
    """ This method builds and starts the GUI portion of the program.
    
    Args:
        truckList (list[Truck]): A list structure containing Truck objects.
    """
    # Populate Truck Frame with info
    for index, truck in enumerate(truckList):
        truckLF = tk.LabelFrame(master=truckTopLF, name=f"t{index+1}Label", text=f"Truck {index+1}",labelanchor="n",font=("Arial",12),bd=3,relief=tk.RAISED)
        truckLF.grid(column=index,row=0,padx=50,pady=10,sticky="N")
        
        # Truck Info
        truckStatusLabel = tk.Label(master=truckLF,name=f"t{index+1}StatusLabel",text="Status: At Hub")
        truckStatusLabel.grid(column=0,row=0)
        
        mileageLabel = tk.Label(master=truckLF,name=f"t{index+1}MileageLabel",text="Mileage: 0.0 miles")
        mileageLabel.grid(column=2,row=0)

        sep = ttk.Separator(master=truckLF,orient="horizontal")
        sep.grid(column=0,row=1,columnspan=3,sticky="ew")

        # Package info titles
        packageHeader = tk.Label(master=truckLF,text="Package",font=("bold"),anchor="center")
        packageHeader.grid(column=0,row=2)

        packageHeaderSepVert = ttk.Separator(master=truckLF,orient="vertical")
        packageHeaderSepVert.grid(column=1,row=2,rowspan=len(truck.packages)+2,sticky="ns")

        packageHeaderSepHor = ttk.Separator(master=truckLF,orient="horizontal")
        packageHeaderSepHor.grid(column=0,row=3,columnspan=3, sticky="ew")

        packageStatusHeader = tk.Label(master=truckLF,text="Package Status",font=("bold"),anchor="center")
        packageStatusHeader.grid(column=2,row=2)
        
        # Populate the Truck's container with its Packages and their info
        for idx, p in enumerate(truck.packages):
            global pkgStatusLabelNames
            pkgStatusLabelNames = {}
            
            packageLabel = tk.Label(master=truckLF,name=f"p{p.getID()}Label",text=f"Package {p.getID()}")
            packageLabel.grid(column=0,row=idx+4)

            packageStatusLabel = tk.Label(master=truckLF,name=f"p{p.getID()}StatusLabel",text=f"{p.getStatus()}")
            packageStatusLabel.grid(column=2,row=idx+4)
            
            pkgStatusLabelNames.update({packageStatusLabel.winfo_name(): packageStatusLabel})
            
    
    # Threads to start deliveries
    thread1 = threading.Thread(target=deliverPackages,args=(root,truckList,truckList[0],"08:00 AM"))
    thread2 = threading.Thread(target=deliverPackages,args=(root,truckList,truckList[1],"08:00 AM"))

    # Update Button command
    controlBtn.config(command=lambda: control(controlBtn,thread1,thread2))

    disableTimeSearch()
    timeViewInfoLabel.config(text="Unable to search.\nProgram never started.")
    
    root.mainloop()

# Root
root = tk.Tk()
root.title("WGUPS Delivery Program")
root.geometry("1014x900")
root.configure(bg="dark gray")
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)

# Notebook widget to hold different views
rootNB = ttk.Notebook(master=root)
mainPage = tk.Frame(master=rootNB,name="mainPage")
timeLookupView = tk.Frame(master=rootNB,name="timeLookupView")
rootNB.add(mainPage,text="Home")
rootNB.add(timeLookupView,text="Time Lookup")
rootNB.grid(column=0,row=0,sticky="nsew")
mainPage.columnconfigure(0,weight=1)
mainPage.rowconfigure(0,weight=1)
timeLookupView.columnconfigure(0,weight=1)
timeLookupView.rowconfigure(0,weight=1)

# Create frame to hold Truck Information
truckTopLF = tk.LabelFrame(master=mainPage,
                           text="Trucks",
                           name="truckTopLF",
                           labelanchor="n",
                           font=("Times New Roman", 14),
                           background="light gray",
                           bd=3,
                           relief=tk.RAISED)
truckTopLF.grid(column=0,row=0,columnspan=5)

# Delivery Updates text area
scrollbar = tk.Scrollbar(master=mainPage)
updatesArea = tk.Text(master=mainPage,name="updatesArea",wrap="word",bg="light green",height=18,yscrollcommand=scrollbar.set)
updatesArea.grid(column=0,row=3,columnspan=3)
scrollbar.grid(column=3,row=3,sticky="nsw")
scrollbar.config(command=updatesArea.yview)

# Frame to contain time/distance info
infoFrame = tk.Frame(master=mainPage,name="infoFrame")
infoFrame.grid(column=0,row=2)

# Interactive button to Start/Stop/Resume program
controlBtn = tk.Button(master=infoFrame,
                        name="controlBtn",
                        text="Start",
                        default="normal",
                        width=10,
                        relief=tk.RAISED)
controlBtn.grid(column=0,row=0)

# Time Widgets
timeLF = tk.LabelFrame(master=infoFrame,name="timeLF",text="Program Time",background="light gray",relief=tk.RAISED)
timeLF.grid(column=1,row=0)

timeVal = tk.Label(master=timeLF,text="08:00 AM",name="timeVal",justify="center",background="light gray")
timeVal.grid(column=0,row=0)

# Total Distance Widgets
totalDistLF = tk.LabelFrame(master=infoFrame,text="Total Distance",name="totalDistLF",background="light gray",relief=tk.RAISED)
totalDistLF.grid(column=2,row=0)

totalDistVal = tk.Label(master=totalDistLF,text="0.0 Miles",name="totalDistVal",justify="center",background="light gray")
totalDistVal.grid(column=0,row=0)

# Time Selector Widget
timeViewLF = tk.LabelFrame(master=timeLookupView,text="View package statuses \nat a specific time",name="timeViewLF",background="light gray",relief=tk.RAISED,labelanchor="n")
timeViewLF.grid(column=4,row=2,pady=10)

timeViewEntry = tk.Entry(master=timeViewLF,name="timeViewEntry",justify="center",relief=tk.SUNKEN)
timeViewEntry.bind("<FocusIn>",clearEntry) # Clears entry contents upon gaining focus
timeViewEntry.bind("<Return>",handleEnterKey)
timeViewEntry.grid(column=0,row=0,sticky="ew",padx=3)

# Button widget to submit time entry
timeViewBtn = tk.Button(master=timeViewLF,name="timeViewBtn",text="View Packages",relief=tk.RAISED,command=lambda: checkPackageStatus())
timeViewBtn.grid(column=0,row=1,sticky="ew",padx=3,pady=3)

# Button widget to reset time search
resetStatusViewBtn = tk.Button(master=timeViewLF,name="resetStatusViewBtn",text="Restore\nStatuses",relief=tk.RAISED,command=lambda: resetStatusView())
resetStatusViewBtn.grid(column=0,row=2,sticky="ew",padx=3,pady=3)

# Label widget to inform user about time lookup
timeViewInfoLabel = tk.Label(master=timeViewLF,
                             name="timeViewInfoLabel",
                             text="Unable to search.\nProgram not started.",
                             justify="center",
                             font=("italicized", 10),bg="light gray",fg="red")
timeViewInfoLabel.grid(column=0,row=3)


