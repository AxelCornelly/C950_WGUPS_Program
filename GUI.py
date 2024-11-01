import tkinter as tk
import threading
from DeliverLogic import deliverPackages

def control():
    if controlBtn["text"] == "Start":
        controlBtn["text"] = "Pause"
        thread1

# Main window
root = tk.Tk()
root.title("WGUPS Delivery Program")
root.geometry("1000x500")
root.columnconfigure(1,weight=1,minsize=50)
root.rowconfigure(1,weight=1,minsize=50)

# Create frame to hold Truck Information
truckFrame = tk.Frame(master=root, relief=tk.RIDGE, borderwidth=3)
truckFrame.grid(column=0, row=0, columnspan=3)

# Create Frame to hold Delivery Updates and Misc Info.
updatesFrame = tk.Frame(master=root,relief=tk.SUNKEN, borderwidth=3)
updatesFrame.grid(column=0,row=1,columnspan=3)

# Label for Program Time
timeLabel = tk.Label(master=updatesFrame, name="timeLabel", text="Program Time: 08:00 AM")
timeLabel.grid(column=0, row=0)

# Label for Total Distance Traveled
totalDistLabel = tk.Label(master=updatesFrame, name="totalDistLabel", text="Total Distance Traveled: 0.0 miles")
totalDistLabel.grid(column=0,row=1)

# Delivery Updates text area
updatesArea = tk.Text(master=updatesFrame,name="updatesArea",width=60,height=20,wrap="word",bg="light gray")
updatesArea.grid(column=1,row=0, rowspan=3,columnspan=2)

# Interactive button to Start/Stop/Resume program
controlBtn = tk.Button(master=root,name="controlBtn",text="Start",command=control)
controlBtn.grid(column=2,row=0)

def startGUI(truckList):
    """ This method builds and starts the GUI portion of the program.
    
    Args:
        truckList (list[Truck]): A list structure containing Truck objects.
    """
    # Populate Truck Frame with labels for each truck in truckList
    # Truck Labels
    for i in range(len(truckList)):
        label = tk.Label(master=truckFrame, name=f"t{i+1}Label", text=f"Truck {i+1}")
        label.grid(column=i,row=0,padx=50)
    
    # Threads to call delivery function
    thread1 = threading.Thread(target=deliverPackages, args=(root, truckList, truckList[0], "08:00 AM"))
    thread2 = threading.Thread(target=deliverPackages, args=(root, truckList, truckList[1], "08:00 AM"))
    
    root.mainloop()

