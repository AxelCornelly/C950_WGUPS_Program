import tkinter as tk
import threading
from DeliverLogic import deliverPackages

def startGUI(truckList):
    """ This method builds and starts the GUI portion of the program.
    
    Args:
        truckList (list[Truck]): A list structure containing Truck objects.
    """

    # Build main window
    root = tk.Tk()
    root.title("WGUPS Delivery Program")

    # Create labels for Truck info
    trucksLabel = tk.Label(root, text="Delivery Trucks:")
    truckStatusLabel = tk.Label(root, text="Truck Status")
    truckMileageLabel = tk.Label(root, text="Truck Mileage")
    truckLabel1 = tk.Label(root, text= "Truck 1")
    truck1StatusLabel = tk.Label(root, text="At Hub")
    truck1MileageLabel = tk.Label(root, text="0.0")
    truckLabel2 = tk.Label(root, text= "Truck 2")
    truck2StatusLabel = tk.Label(root, text="At Hub")
    truck2MileageLabel = tk.Label(root, text="0.0")
    truckLabel3 = tk.Label(root, text= "Truck 3")
    truck3StatusLabel = tk.Label(root, text="At Hub")
    truck3MileageLabel = tk.Label(root, text="0.0")

    trucksLabel.grid(column=0, row=0)
    truckStatusLabel.grid(column=1, row=0)
    truckMileageLabel.grid(column=2, row=0)

    truckLabel1.grid(column=0, row=1)
    truck1StatusLabel.grid(column=1, row=1)
    truck1MileageLabel.grid(column=2, row=1)

    truckLabel2.grid(column=0, row=2)
    truck2StatusLabel.grid(column=1, row=2)
    truck2MileageLabel.grid(column=2, row=2)

    truckLabel3.grid(column=0, row=3)
    truck3StatusLabel.grid(column=1, row=3)
    truck3MileageLabel.grid(column=2, row=3)

    # Label for Program Time
    timeLabel = tk.Label(root, text="08:00 AM")
    timeLabel.grid(column=0, row=5)

    
    root.mainloop()