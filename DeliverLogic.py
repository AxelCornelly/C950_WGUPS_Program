import datetime
import time
import csv
import tkinter as tk
from TruckClass import Truck
from PackageClass import Package

def getUIState(time) -> dict:
    return uiLog[time]

def logUIState(time, widget):
    # Update time variable to be a readable string without case
    ezTime = time.casefold()
    
    # First check if there is an existing entry for the given time
    if ezTime in uiLog.keys():
        uiLog[ezTime].update({ # If so, update that time's inner dictionary by adding another key-value pair 
            widget.winfo_name(): widget["text"]
        })
    else: # If not found, add entry for given time along with its inner dictionary
        uiLog[ezTime] = {widget.winfo_name(): widget["text"]}
    

def deliverPackages(gui, trucks, startTruck: Truck, startTime):
    """ Initiates the delivery of packages for a given truck.
    
    Args:
        gui (Tk()): A Tk() object which resembles the root of the GUI.
        trucks (list(Truck)): A list of all Truck objects.
        startTruck (Truck): The starting Truck object to start delivering.
        startTime (str): A string of the starting delivery time (08:00am).
    """
    timer = 0
    totalTravelDist = 0.0 # In miles
    distToNext = float('inf') # Tracks how far the Truck is from the next stop
    progress = 0.0 # Tracks Truck's travel distance in between stops
    currAddress = "HUB" # Initially set to HUB since all Trucks start there
    start_Time = datetime.datetime.strptime(startTime, "%H:%M %p").time()
    
    # Global variable to log UI states
    global uiLog
    uiLog = {}

    # GUI widgets to be updated throughout the program
    guiRoot = gui
    truckWidget = guiRoot.nametowidget("truckTopLF").nametowidget(f"t{startTruck.getTruckID()}Label")
    truckStatusWidget = truckWidget.nametowidget(f"t{startTruck.getTruckID()}StatusLabel")
    truckMileageWidget = truckWidget.nametowidget(f"t{startTruck.getTruckID()}MileageLabel")
    timeWidget = guiRoot.nametowidget("timeLF").nametowidget("timeVal")
    timeSearchEntryWidget = guiRoot.nametowidget("timeViewLF").nametowidget("timeViewEntry")
    timeSearchBtnWidget = guiRoot.nametowidget("timeViewLF").nametowidget("timeViewBtn")
    timeSearchLabel = guiRoot.nametowidget("timeViewLF").nametowidget("timeViewInfoLabel")
    totalDistWidget = guiRoot.nametowidget("totalDistLF").nametowidget("totalDistVal")
    updatesWidget = guiRoot.nametowidget("updatesArea")

    while timer < 20000:
        # Check if program is paused
        if guiRoot.nametowidget("controlBtn")["text"] == "Resume":
            while guiRoot.nametowidget("controlBtn")["text"] == "Resume":
                time.sleep(0.1)
        
        # Program speed
        timer += 1
        time.sleep(0.1)

        # Continuously update current time while program runs, incrementing minutes
        currentTime = datetime.datetime.combine(datetime.date.today(), start_Time) + datetime.timedelta(minutes=timer)
        # Update gui
        timeWidget["text"] = datetime.datetime.strftime(currentTime,"%H:%M %p")
        # Str variable to hold message time
        msgTime = datetime.datetime.strftime(currentTime,"%H:%M %p")

        # When delayed packages arrive at 09:05 am, update statuses
        if currentTime.hour == 9 and currentTime.minute == 5:
            for p in trucks[2].packages:
                if p.getStatus() == "Delayed":
                    p.updateStatus("On Truck")
                    # Update gui
                    packageWidget = guiRoot.nametowidget("truckTopLF").nametowidget("t3Label").nametowidget(f"p{p.getID()}StatusLabel")
                    packageWidget["text"] = "On Truck"
                    # Log UI state
                    logUIState(msgTime,packageWidget)
        
        # When 10:20am hits, update Package 9's address
        if currentTime.hour == 10 and currentTime.minute == 20:
            for p in trucks[2].packages:
                if p.getID() == 9:
                    p.updateStatus("On Truck")
                    packageWidget = guiRoot.nametowidget("truckTopLF").nametowidget("t3Label").nametowidget(f"p{p.getID()}StatusLabel")
                    packageWidget["text"] = "On Truck"
                    # Log UI state
                    logUIState(msgTime,packageWidget)
                    p.updateAddress("410 S State St", "Salt Lake City", "UT", "84111")
                    updatesWidget.insert(tk.END,f"\n[{msgTime}]: Package 9 address corrected to: {p.getAddress()}")
                    updatesWidget.see(tk.END)
        
        # Truck Delivery Process

        # Logic for Truck 1 and 2
        # Check if Truck is not Truck 3 and also not already done delivering
        if startTruck.getTruckID() != 3 and startTruck.getTruckStatus() != "Finished Delivering":
            if startTruck.getTruckStatus() != "Heading back to Hub":
                startTruck.setTruckStatus("Delivering")
                truckStatusWidget["text"] = startTruck.getTruckStatus()
                if len(startTruck.packages) != 0:
                    # Find next nearest address from current location
                    nextPkg = findNearestPkg(currAddress, startTruck.packages)
                    distToNext = float(distBetween(currAddress, nextPkg.getAddress()))

                    # Head to address
                    if distToNext > 0:
                        progress += (18/60) # Increment progress distance.
                        startTruck.mileage += (18/60) # Increment Truck's total mileage
                        truckMileageWidget["text"] = str(round(startTruck.mileage,2)) # Update gui
                        totalTravelDist = (trucks[0].mileage + trucks[1].mileage + trucks[2].mileage)
                        totalDistWidget["text"] = str(round(totalTravelDist,2)) # Update gui

                        # Deliver package(s) once arriving at destination
                        if progress >= distToNext:
                            # Reset progress and update current address
                            progress = 0
                            currAddress = nextPkg.getAddress()
                            
                            # Find any other packages with the same address.
                            sharedAddr = []
                            for package in startTruck.packages:
                                if package.getAddress() == currAddress:
                                    sharedAddr.append(package)
                            
                            # Deliver package(s), removing them from the Truck's package list.
                            for package in sharedAddr:
                                package.updateStatus("Delivered")
                                package.setDeliveredTime(currentTime)
                                updatesWidget.insert(tk.END,f"\n[{msgTime}]: Package {package.getID()} delivered. Deadline was {package.getDeadline()}")
                                updatesWidget.see(tk.END)
                                packageWidget = truckWidget.nametowidget(f"p{package.getID()}StatusLabel")
                                packageWidget["text"] = package.getStatus()
                                # Log UI state
                                logUIState(msgTime,packageWidget)
                                startTruck.packages.remove(package)
                            
                            # Empty the sharedAddr list
                            sharedAddr = []
                
                # If Truck package list is empty, deliveries complete, trigger return process.
                if len(startTruck.packages) == 0: 
                    progress = 0
                    startTruck.setTruckStatus("Heading back to Hub")
                    truckStatusWidget["text"] = startTruck.getTruckStatus()
            
            # Start heading back to the Hub
            if startTruck.getTruckStatus() == "Heading back to Hub":
                distToNext = float(distBetween(currAddress, "HUB"))
                if distToNext > 0:
                    progress += (18/60)
                    startTruck.mileage += (18/60)
                    truckMileageWidget["text"] = str(round(startTruck.mileage,2))
                    totalTravelDist = (trucks[0].mileage + trucks[1].mileage + trucks[2].mileage)
                    totalDistWidget["text"] = str(round(totalTravelDist,2)) # Update gui

                    # Once returned, put Truck out of commission, start Truck 3
                    if progress >= distToNext:
                        progress = 0
                        currAddress = "HUB"
                        updatesWidget.insert(tk.END,f"\n[{msgTime}]: Truck {startTruck.getTruckID()} returned to HUB.")
                        updatesWidget.see(tk.END)
                        startTruck.setTruckStatus("Finished Delivering")
                        truckStatusWidget["text"] = startTruck.getTruckStatus()
                        
                        if startTruck.getTruckID() == 2: # Ends the thread that starts with truck 2 because we know it finishes after Truck 1
                            break
                        
                        if trucks[2].getTruckStatus() == "At Hub":
                            trucks[2].setTruckStatus("Delivering")
                            startTruck = trucks[2]
                            # Update widgets
                            truckWidget = guiRoot.nametowidget("truckTopLF").nametowidget(f"t{startTruck.getTruckID()}Label")
                            truckStatusWidget = truckWidget.nametowidget(f"t{startTruck.getTruckID()}StatusLabel")
                            truckMileageWidget = truckWidget.nametowidget(f"t{startTruck.getTruckID()}MileageLabel")
                            truckStatusWidget["text"] = startTruck.getTruckStatus()
        
        # Logic for Truck 3 to start delivering. Delivers urgent packages first
        if startTruck.getTruckID() == 3 and startTruck.getTruckStatus() != "Finished Delivering":
            if startTruck.getTruckStatus() != "Heading back to Hub":
                if len(startTruck.packages) != 0:
                    # List to hold any urgent packages
                    urgentPkgs = []
                    
                    # Add any urgent packages to list
                    for package in startTruck.packages:
                        if package.getDeadline() != "EOD": # If deadline is not EOD, it is urgent.
                            urgentPkgs.append(package)
                        
                    # Deliver Urgent packages first
                    if len(urgentPkgs) != 0:
                        nearestUrgent = findNearestPkg(currAddress, urgentPkgs)
                        distToNext = float(distBetween(currAddress, nearestUrgent.getAddress()))

                        if distToNext > 0:
                            progress += (18/60)
                            startTruck.mileage += (18/60)
                            truckMileageWidget["text"] = str(round(startTruck.mileage,2))
                            totalTravelDist = (trucks[0].mileage + trucks[1].mileage + trucks[2].mileage)
                            totalDistWidget["text"] = str(round(totalTravelDist,2)) # Update gui

                            if progress >= distToNext:
                                progress = 0
                                currAddress = nearestUrgent.getAddress()
                                
                                # Deliver any packages with a shared address
                                for package in urgentPkgs:
                                    if package.getAddress() == currAddress:
                                        package.updateStatus("Delivered")
                                        package.setDeliveredTime(currentTime)
                                        packageWidget = truckWidget.nametowidget(f"p{package.getID()}StatusLabel")
                                        packageWidget["text"] = package.getStatus()
                                        # Log UI state
                                        logUIState(msgTime,packageWidget)
                                        updatesWidget.insert(tk.END,f"\n[{msgTime}]: Package {package.getID()} delivered. Deadline was {package.getDeadline()}")
                                        updatesWidget.see(tk.END)
                                        urgentPkgs.remove(package)
                                        startTruck.packages.remove(package)
                    
                    # Non-urgent Delivery process. Same as Truck 1 and 2
                    nearestPkg = findNearestPkg(currAddress, startTruck.packages)
                    distToNext = float(distBetween(currAddress, nearestPkg.getAddress()))
                    
                    if distToNext > 0:
                        progress += (18/60)
                        startTruck.mileage += (18/60)
                        truckMileageWidget["text"] = str(round(startTruck.mileage,2))
                        totalTravelDist = (trucks[0].mileage + trucks[1].mileage + trucks[2].mileage)
                        totalDistWidget["text"] = str(round(totalTravelDist,2)) # Update gui

                        # Deliver package(s) once arriving at destination
                        if progress >= distToNext:
                            # Reset progress and update current address
                            progress = 0
                            currAddress = nearestPkg.getAddress()
                            
                            # Find any other packages with the same address.
                            sharedAddr = []
                            
                            if len(startTruck.packages) != 0:
                                for package in startTruck.packages:
                                    if package.getAddress() == currAddress:
                                        sharedAddr.append(package)
                                
                                # Deliver package(s)
                                for package in sharedAddr:
                                    package.updateStatus("Delivered")
                                    package.setDeliveredTime(currentTime)
                                    packageWidget = truckWidget.nametowidget(f"p{package.getID()}StatusLabel")
                                    packageWidget["text"] = package.getStatus()
                                    # Log UI state
                                    logUIState(msgTime,packageWidget)
                                    updatesWidget.insert(tk.END,f"\n[{msgTime}]: Package {package.getID()} delivered. Deadline was {package.getDeadline()}")
                                    updatesWidget.see(tk.END)
                                    startTruck.packages.remove(package)
                                
                                # Empty sharedAddr list
                                sharedAddr = []
            
                # If Truck package list is empty, deliveries complete, trigger return process.
                if len(startTruck.packages) == 0:
                    progress = 0
                    startTruck.setTruckStatus("Heading back to Hub")
                    truckStatusWidget["text"] = startTruck.getTruckStatus()

            # Start heading back to the Hub
            if startTruck.getTruckStatus() == "Heading back to Hub":
                distToNext = float(distBetween(currAddress, "HUB"))
                if distToNext > 0:
                    progress += (18/60)
                    startTruck.mileage += (18/60)
                    truckMileageWidget["text"] = str(round(startTruck.mileage,2))
                    totalTravelDist = (trucks[0].mileage + trucks[1].mileage + trucks[2].mileage)
                    totalDistWidget["text"] = str(round(totalTravelDist,2)) # Update gui

                    # Once returned, put Truck out of commission
                    if progress >= distToNext:
                        progress = 0
                        currAddress = "HUB"
                        updatesWidget.insert(tk.END,f"\n[{msgTime}]: Truck {startTruck.getTruckID()} returned to HUB.")
                        updatesWidget.see(tk.END)
                        startTruck.setTruckStatus("Finished Delivering")
                        truckStatusWidget["text"] = startTruck.getTruckStatus()
        
        # If all Trucks are done delivering, end program
        if all(truck.getTruckStatus() == "Finished Delivering" for truck in trucks):
            # Perform end-program tasks
            totalTravelDist = trucks[0].mileage + trucks[1].mileage + trucks[2].mileage
            totalDistWidget["text"] = round(totalTravelDist,2)
            updatesWidget.insert(tk.END,"\n=== Deliveries Complete ===")
            updatesWidget.see(tk.END)
            guiRoot.nametowidget("controlBtn")["text"] = "Exit"
            
            # Enable function to enter in a time to see package statuses
            timeSearchEntryWidget.config(state="normal") # enable entry field
            timeSearchBtnWidget.config(state="normal") # enable button
            timeSearchLabel.grid_forget() # hide disabled text
            break



    
def findNearestPkg(startAddr: str, packageList) -> Package:
    """ Similar to the NearestNeighbor function found in the Main.py file.
    This function takes in a starting address and a list of Package objects
    and finds the Package with the closest address to startAddr.
    
    Args:
        startAddr (str): The starting address to compare to.
        packageList (list[type[Package]]): A list structure of Package objects.
    
    Returns:
        nextPkg (Package): The Package object with the closest address.
    """
    nextPkg = Package()
    minDist = float('inf') # Unreachable high number

    for package in packageList:
        dist = float(distBetween(startAddr, package.getAddress()))
        if dist < minDist:
            minDist = dist
            nextPkg = package
    
    return nextPkg

def distBetween(add1: str, add2: str) -> float:
    """ Similar to the findDistBetween function found in Main.py.
    Takes in two strings as addresses and locates the distance between
    the address by searching the WGUPS Distance Table csv file. Returns
    the distance as a float.
    
    Args:
        add1 (str): String object of the first address.
        add2 (str): String object of the second address.
    
    Returns:
        dist (float): Float object of the distance between the addresses (in miles)
    """
    # Read WGUPS Distance Table csv file and put contents into a list of addresses and 2D list of distance values
    addresses = []
    distances = []

    with open("WGUPS Distance Table.csv", mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            addresses.append(line[0]) # The first item in the row will be the address
            distances.append(line[1:]) # The following items after will be distances

    # Find distance to closest address
    dist = 0.0

    idx1 = addresses.index(add1)
    idx2 = addresses.index(add2)

    if(distances[idx1][idx2] == ''):
            dist = distances[idx2][idx1]
            return dist
    dist = distances[idx1][idx2]
    return dist