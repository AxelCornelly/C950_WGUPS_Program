import tkinter as tk
import tkinter.ttk as ttk
import threading
from DeliverLogic import deliverPackages

def control(btn,txt):
    if btn["text"] == "Start" or btn["text"] == "Resume":
        btn["text"] = "Pause"
    elif btn["text"] == "Pause":
        btn["text"] = "Resume"
    
    rc = root.winfo_children()
    tlfc =


def startGUI(truckList):
    """ This method builds and starts the GUI portion of the program.
    
    Args:
        truckList (list[Truck]): A list structure containing Truck objects.
    """
    # Populate Truck Frame with info
    for index, truck in enumerate(truckList):
        # Create a separate LabelFrame for each truck
        truckLF = tk.LabelFrame(master=truckTopLF, name=f"t{index+1}Label", text=f"Truck {index+1}",labelanchor="n",font=("Arial",12),bd=3,relief=tk.RAISED)
        truckLF.grid(column=index,row=0,padx=50,pady=10,sticky="N")
        
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
        packageHeaderSepVert.grid(column=1,row=2,rowspan=len(truck.packages)+2,sticky="ns")

        packageHeaderSepHor = ttk.Separator(master=truckLF,orient="horizontal")
        packageHeaderSepHor.grid(column=0,row=3,columnspan=3, sticky="ew")

        packageStatusHeader = tk.Label(master=truckLF,text="Package Status",font=("bold"),anchor="center")
        packageStatusHeader.grid(column=2,row=2)
        
        # Populate the Truck's container with its Packages and their info
        for idx, p in enumerate(truck.packages):
            
            packageLabel = tk.Label(master=truckLF,text=f"Package {p.getID()}")
            packageLabel.grid(column=0,row=idx+4)

            packageStatusLabel = tk.Label(master=truckLF,text=f"{p.getStatus()}")
            packageStatusLabel.grid(column=2,row=idx+4)
    
    
    root.mainloop()

# Main window
root = tk.Tk()
root.title("WGUPS Delivery Program")
root.geometry("1000x800")
root.columnconfigure(1,weight=1,minsize=50)
root.rowconfigure(1,weight=1,minsize=50)
root.configure(bg="dark gray")

# Create frame to hold Truck Information
truckTopLF = tk.LabelFrame(master=root,text="Trucks",name="truckTopLF",labelanchor="n",font=("Times New Roman", 14),background="light gray",bd=3,relief=tk.RAISED)
truckTopLF.grid(column=0,row=0,columnspan=3)

# Create Frame to hold Delivery updates and Misc Info.
updatesFrame = tk.Frame(master=root,name="updatesFrame",relief=tk.SUNKEN, borderwidth=3,bg="dark gray")
updatesFrame.grid(column=1,row=1,columnspan=2, rowspan=3)

# Delivery Updates text area
updatesArea = tk.Text(master=updatesFrame,name="updatesArea",width=60,height=20,wrap="word",bg="light green")
updatesArea.grid(column=1,row=0, rowspan=3)

# Time Widgets
timeLF = tk.LabelFrame(master=updatesFrame,name="timeLF",text="Program Time",background="light gray",relief=tk.RAISED)
timeLF.grid(column=0,row=0,padx=5)

timeVal = tk.Label(master=timeLF,text="08:00 AM",name="timeVal",justify="center",background="light gray")
timeVal.grid(column=0,row=0)

# Total Distance Widgets
totalDistLF = tk.LabelFrame(master=updatesFrame,text="Total Distance",name="totalDistLF",background="light gray",relief=tk.RAISED)
totalDistLF.grid(column=0,row=1,sticky="n",padx=5)

totalDistVal = tk.Label(master=totalDistLF,text="0.0 Miles",name="totalDistVal",justify="center",background="light gray")
totalDistVal.grid(column=0,row=0,sticky="ne")

# Interactive button to Start/Stop/Resume program
controlBtn = tk.Button(master=updatesFrame,
                        name="controlBtn",
                        text="Start",
                        default="normal",
                        width=10,
                        relief=tk.RAISED,
                        command=lambda: control(controlBtn, "TEXT"))
controlBtn.grid(column=0,row=2)
