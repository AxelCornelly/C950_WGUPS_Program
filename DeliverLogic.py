import datetime
import time
import csv
from TruckClass import Truck
from PackageClass import Package

def deliverPackages(trucks, startTruck: Truck, startTime):
    """ Initiates the delivery of packages for a given truck.
    
    Args:
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

    while timer < 20000:
        # Program speed
        timer += 1
        time.sleep(0.1)

        # Continuously update current time while program runs, incrementing minutes
        currentTime = datetime.datetime.combine(datetime.date.today(), start_Time) + datetime.timedelta(minutes=timer)
        
        # When delayed packages arrive at 09:05 am, update statuses
        if currentTime.hour == 9 and currentTime.minute == 5:
            for p in trucks[2].packages:
                if p.getStatus() == "Delayed":
                    p.updateStatus("On Truck")
        
        # When 10:20am hits, update Package 9's address
        if currentTime.hour == 10 and currentTime.minute == 20:
            for p in trucks[2].packages:
                if p.getID() == 9:
                    p.updateAddress("410 S State St", "Salt Lake City", "UT", "84111")
        
        # Truck Delivery Process

        # Logic for Truck 1 and 2
        # Check if Truck is not Truck 3 and also not already done delivering
        if startTruck.getTruckID() != 3 and startTruck.getTruckStatus() != "Finished Delivering":
            if startTruck.getTruckStatus() != "Heading back to Hub":
                startTruck.setTruckStatus("Delivering")
                if len(startTruck.packages) != 0:
                    # Find next nearest address from current location
                    nextPkg = findNearestPkg(currAddress, startTruck.packages)
                    distToNext = float(distBetween(currAddress, nextPkg.getAddress()))

                    # Head to address
                    if distToNext > 0:
                        totalTravelDist += (18/60) # Increment travel distance. Truck travels at 18 mph
                        progress += (18/60) # Increment progress distance.
                        startTruck.mileage += (18/60) # Increment Truck's total mileage
                        # print(f"Dist to Next: {round(distToNext, 2)} miles")
                        # print(f"Progress: {round(progress, 2)} miles")

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
                                print(f"Truck {startTruck.getTruckID()} delivered Package {package.getID()} at {datetime.datetime.strftime(package.deliveredTime, "%H:%M %p")}. Deadline was {package.getDeadline()}")
                                startTruck.packages.remove(package)
                            
                            # Empty the sharedAddr list
                            sharedAddr = []
                
                # If Truck package list is empty, deliveries complete, trigger return process.
                if len(startTruck.packages) == 0: 
                    # print(f"Truck {startTruck.getTruckID()} Empty!")
                    progress = 0
                    startTruck.setTruckStatus("Heading back to Hub")
            
            # Start heading back to the Hub
            if startTruck.getTruckStatus() == "Heading back to Hub":
                distToNext = float(distBetween(currAddress, "HUB"))
                if distToNext > 0:
                    totalTravelDist += (18/60)
                    progress += (18/60)
                    startTruck.mileage += (18/60)

                    # Once returned, put Truck out of commission, start Truck 3
                    if progress >= distToNext:
                        progress = 0
                        currAddress = "HUB"
                        print(f"Truck {startTruck.getTruckID()} returned to Hub @ {datetime.datetime.strftime(currentTime, "%H:%M %p")}")
                        startTruck.setTruckStatus("Finished Delivering")
                        print(f"Truck {startTruck.getTruckID()} {startTruck.getTruckStatus()}")
                        if trucks[2].getTruckStatus() == "At Hub":
                            trucks[2].setTruckStatus("Delivering")
                            startTruck = trucks[2]
                            print(f"startTruck is now Truck {startTruck.getTruckID()}")
        
        # Logic for Truck 3 to start delivering. Delivers urgent packages first
        if startTruck.getTruckID() == 3 and startTruck.getTruckStatus() != "Finished Delivering":
            if startTruck.getTruckStatus() != "Heading back to Hub":
                # Update Truck status
                startTruck.setTruckStatus("Delivering")
                
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
                            totalTravelDist += (18/60) # Increment total travel
                            progress += (18/60) # Increment Truck progress
                            startTruck.mileage += (18/60) # Increment Truck mileage

                            if progress >= distToNext:
                                progress = 0
                                currAddress = nearestUrgent.getAddress()
                                
                                # Deliver any packages with a shared address
                                for package in urgentPkgs:
                                    if package.getAddress() == currAddress:
                                        package.updateStatus("Delivered")
                                        package.setDeliveredTime(currentTime)
                                        print(f"Truck {startTruck.getTruckID()} delivered Package {package.getID()} at {datetime.datetime.strftime(package.deliveredTime, "%H:%M %p")}. Deadline was {package.getDeadline()}")
                                        urgentPkgs.remove(package)
                                        startTruck.packages.remove(package)
                    
                    # Non-urgent Delivery process. Same as Truck 1 and 2
                    nearestPkg = findNearestPkg(currAddress, startTruck.packages)
                    distToNext = float(distBetween(currAddress, nearestPkg.getAddress()))
                    
                    if distToNext > 0:
                        totalTravelDist += (18/60) # Increment travel distance. Truck travels at 18 mph
                        progress += (18/60) # Increment progress distance.
                        startTruck.mileage += (18/60) # Increment Truck's total mileage
                        # print(f"Dist to Next: {round(distToNext, 2)} miles")
                        # print(f"Progress: {round(progress, 2)} miles")

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
                                    print(f"Truck {startTruck.getTruckID()} delivered Package {package.getID()} at {datetime.datetime.strftime(package.deliveredTime, "%H:%M %p")}. Deadline was {package.getDeadline()}")
                                    startTruck.packages.remove(package)
                                
                                # Empty sharedAddr list
                                sharedAddr = []
            
                # If Truck package list is empty, deliveries complete, trigger return process.
                if len(startTruck.packages) == 0: 
                    # print(f"Truck {startTruck.getTruckID()} Empty!")
                    progress = 0
                    startTruck.setTruckStatus("Heading back to Hub")

            # Start heading back to the Hub
            if startTruck.getTruckStatus() == "Heading back to Hub":
                distToNext = float(distBetween(currAddress, "HUB"))
                if distToNext > 0:
                    totalTravelDist += (18/60)
                    progress += (18/60)
                    startTruck.mileage += (18/60)

                    # Once returned, put Truck out of commission
                    if progress >= distToNext:
                        progress = 0
                        currAddress = "HUB"
                        print(f"Truck {startTruck.getTruckID()} returned to Hub @ {datetime.datetime.strftime(currentTime, "%H:%M %p")}")
                        startTruck.setTruckStatus("Finished Delivering")
                        print(f"Truck {startTruck.getTruckID()} {startTruck.getTruckStatus()}")
        
        # If all Trucks are done delivering, end program
        if all(truck.getTruckStatus() == "Finished Delivering" for truck in trucks):
            # Do end-of-program stuff:
            # total all trucks distance traveled
            # close program
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