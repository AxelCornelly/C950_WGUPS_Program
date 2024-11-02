import tkinter as tk
import tkinter.ttk as ttk
import threading
from DeliverLogic import deliverPackages

def control(root: tk.Tk, thread1, thread2):
    btn = root.nametowidget("controlBtn")
    if btn["text"] == "Start":
        btn["text"] = "Pause"
        #thread1.start()
        #thread2.start()
    
    if btn["text"] == "Pause":
        btn["text"] = "Resume"
    
    if btn["text"] == "Resume":
        btn["text"] = "Pause"


def startGUI(truckList):
    """ This method builds and starts the GUI portion of the program.
    
    Args:
        truckList (list[Truck]): A list structure containing Truck objects.
    """
    # Main window
    root = tk.Tk()
    root.title("WGUPS Delivery Program")
    root.geometry("1000x800")
    root.columnconfigure(1,weight=1,minsize=50)
    root.rowconfigure(1,weight=1,minsize=50)

    # Create frame to hold Truck Information
    truckTopLF = tk.LabelFrame(master=root,text="Trucks",labelanchor="n",font=("Times New Roman", 14),background="light gray",bd=3,relief=tk.RAISED)
    truckTopLF.grid(column=0,row=0,columnspan=3)


    # Populate Truck Frame with info
    for i in range(len(truckList)):
        # Create a separate LabelFrame for each truck
        truckLF = tk.LabelFrame(master=truckTopLF, name=f"t{i+1}Label", text=f"Truck {i+1}",labelanchor="n",font=("Arial",12),bd=3,relief=tk.RAISED)
        truckLF.grid(column=i,row=0,padx=50,pady=10,sticky="N")
        
        # Truck Info
        truckStatusLabel = tk.Label(master=truckLF,text="Status: At Hub")
        truckStatusLabel.grid(column=0,row=0)
        
        mileageLabel = tk.Label(master=truckLF,text="Mileage: 0.0 miles")
        mileageLabel.grid(column=2,row=0)

        sep = ttk.Separator(master=truckLF,orient="horizontal")
        sep.grid(column=0,row=1,columnspan=3,sticky="ew")

        # Package info titles
        packageHeader = tk.Label(master=truckLF,text="Package",font=("bold"),anchor="center")
        packageHeader.grid(column=0,row=2)

        packageHeaderSepVert = ttk.Separator(master=truckLF,orient="vertical")
        packageHeaderSepVert.grid(column=1,row=2,rowspan=len(truckList[i].packages)+2,sticky="ns")

        packageHeaderSepHor = ttk.Separator(master=truckLF,orient="horizontal")
        packageHeaderSepHor.grid(column=0,row=3,columnspan=3, sticky="ew")

        packageStatusHeader = tk.Label(master=truckLF,text="Package Status",font=("bold"),anchor="center")
        packageStatusHeader.grid(column=2,row=2)
        
        # Populate the Truck's container with its Packages and their info
        for index, p in enumerate(truckList[i].packages):
            
            packageLabel = tk.Label(master=truckLF,text=f"Package {p.getID()}")
            packageLabel.grid(column=0,row=index+4)

            packageStatusLabel = tk.Label(master=truckLF,text=f"{p.getStatus()}")
            packageStatusLabel.grid(column=2,row=index+4)

    # Create Frame to hold Delivery Updates
    updatesFrame = tk.Frame(master=root,relief=tk.SUNKEN, borderwidth=3)
    updatesFrame.grid(column=1,row=1,columnspan=2, rowspan=3)

    # Delivery Updates text area
    updatesArea = tk.Text(master=updatesFrame,name="updatesArea",width=60,height=20,wrap="word",bg="light gray")
    updatesArea.grid(column=0,row=0, rowspan=3)

    # Container for Time and Distance Info
    miscLF = tk.Frame(master=root)
    miscLF.grid(column=0,row=1)

    # Time Widgets
    timeLF = tk.LabelFrame(master=miscLF,text="Program Time",pady=10)
    timeLF.grid(column=0,row=0)

    timeVal = tk.Label(master=timeLF,text="08:00 AM",justify="center")
    timeVal.grid(column=0,row=0,sticky="nsew")

    # Total Distance Widgets
    totalDistLF = tk.LabelFrame(master=miscLF,text="Total Distance",pady=10)
    totalDistLF.grid(column=0,row=1)

    totalDistVal = tk.Label(master=totalDistLF,text="0.0 Miles",justify="center")
    totalDistVal.grid(column=0,row=0,sticky="ne")
    

    # Threads to run delivery program
    thread1 = threading.Thread(target=deliverPackages, args=(root, truckList, truckList[0], "08:00 AM"))
    thread2 = threading.Thread(target=deliverPackages, args=(root, truckList, truckList[1], "08:00 AM"))

    # Interactive button to Start/Stop/Resume program
    #controlBtn = tk.Button(master=root,name="controlBtn",text="Start",default="normal",command=control(root, thread1, thread2))
    #controlBtn.grid(column=2,row=0)
    
    
    root.mainloop()

