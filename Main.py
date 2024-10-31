import csv
import threading
from PackageClass import Package
from HashTableClass import HashTable
from TruckClass import Truck
from DeliverLogic import deliverPackages
from GUI import startGUI

# Initializing data structures
packageHash = HashTable() # Custom class that creates a hash table using lists.
distances = [] # List data structure to hold distance data. 2 dimensional
addresses = [] # List data structure to hold addresses. 1 dimensional
        
def readPackages(packageFile):
    """ This function reads in a csv file containing package data and appends them
    to the packageHash data structure.
    
    Args:
        packageFile (str): String path to the package csv file.
    """
    with open(packageFile, mode='r') as file:
        csvFile = csv.reader(file)
        next(csvFile) # Skips Header Row
        for line in csvFile:
            p = Package(line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7])
            # print(p.toString())
            packageHash.addPackage(p)

# Read in distance data and add to distance 2D list
def readDistances(distanceFile):
    """ Reads in a csv file of distances between delivery addresses.
    
    Args:
        distanceFile (str): String path to the distance csv file.
    """
    with open(distanceFile, mode='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            addresses.append(line[0]) # The first item in the row will be the address
            distances.append(line[1:]) # The following items after will be distances

def findDistBetween(loc1: str, loc2: str) -> float:
        """ Finds the distance between 2 entered addresses from the distances table. This function
        performs an index check to accommodate for the assumption that the distances between each
        address is the same in both directions. Therefore, the csv file would only contain half of
        the full table and would be formatted to not have any duplicate values.
        
        E.g:
        location1: 0.0, _ , _ , _ , _ , _
        location2: 2.3, 0.0, _ , _ , _ , _
        location3: 3.5, 6.6, 0.0, _ , _ , _
        and so on...
        
        Where 0.0 is the location's distance to itself.
        
        Args:
            loc1 (str): String of the first location.
            loc2 (str): String of the second location.
        
        Returns:
            dist (float): The distance between the two locations in miles.
        """
        dist = 0.0
        index1 = addresses.index(loc1) # index of first location
        index2 = addresses.index(loc2) # index of second location

        # Index check
        if(distances[index1][index2] == ''):
            dist = distances[index2][index1]
            return dist
        dist = distances[index1][index2]
        return dist

def nearestNeighbor(currAddress: str, packageList: list[Package]) -> Package:
    """ Determines the next closest package using the nearest-neighbor greedy algorithm.
    
    Args:
        currAddress (str): The current address to compare to.
        packageList (list): The list of packages.
    
    Returns:
        nearest (Package): The closest package to currAddress.
    """
    minDist = float('inf') # Infinity
    nearest = Package() # Initially set to empty Package object.
    
    # Loop through all the packages on the truck calling findDistBetween()
    for package in packageList:
        dist = float(findDistBetween(currAddress, package.getAddress()))
        if dist < minDist:
            minDist = dist
            nearest = package
    
    return nearest

def loadPackages(packageHashTable: HashTable, trucks: list[Truck]):
    """ Loads a maximum of 16 packages on to the truck. Performs checks to
    satisfy program assumptions such as:
    Max num of packages = 16
    Loading time is instant
    Complies with any and all Special Notes on packages
    
    Args:
        packages (HashTable): The HashTable object of packages to load from.
        trucks (list[Truck]): A list of Truck objects to load.
    """
    # Initially load packages manually based on certain restrictions
    
    # Check if package is dependent on another, load them on Truck 1
    for package in packageHashTable.getAllPackages():
        parentPkg = [13,15,19] # List of Package IDs of Packages that have dependents
        if package.requiresPackage or package.getID() in parentPkg:
            trucks[0].packages.append(package)
            package.updateStatus("On Truck")
            packageHashTable.removePackage(package.getID())
        
    # Load packages that must be on Truck 2
    for package in packageHashTable.getAllPackages():    
        if package.requiresTruck:
            trucks[1].packages.append(package)
            package.updateStatus("On Truck")
            packageHashTable.removePackage(package.getID())
        
    # Skip packages that are delayed. They'll be loaded when they arrive.
    for package in packageHashTable.getAllPackages():    
        if package.getStatus() == "Delayed":
            trucks[2].packages.append(package)
            packageHashTable.removePackage(package.getID())
    
    # General package loading
    for truck in trucks:
        # If there aren't any more packages, don't do anything
        if(len(packageHashTable.getAllPackages()) == 0):
            print("EMPTY")
            break
        
        # If truck is full or is out delivering, skip truck
        if(len(truck.packages) == truck.capacity or truck.getTruckStatus() == "Delivering"):
            continue

        # Load truck until capactity is reached
        while len(truck.packages) < truck.capacity:
            # Always check packages list to see if empty at any point
            if(len(packageHashTable.getAllPackages()) == 0):
                break
            
            # Find nearest package
            nearestPkg = nearestNeighbor("HUB", packageHashTable.getAllPackages())
            truck.packages.append(nearestPkg) # Add to truck's list
            nearestPkg.updateStatus("On Truck") # Update package status
            packageHashTable.removePackage(nearestPkg.getID()) # Remove from package HashTable
                                     

if __name__ == "__main__":
    readPackages("WGUPS Package File.csv")
    # packageHash.showContents()
    readDistances("WGUPS Distance Table.csv")
    
    t1 = Truck(1)
    t2 = Truck(2)
    t3 = Truck(3)
    truckList = [t1, t2, t3]
    loadPackages(packageHash, truckList)
    
    # for t in truckList:
    #     for p in t.packages:
    #         print(f"Truck {t.getTruckID()}: {p.toString()}")
        
    #     print(f"Truck {t.getTruckID()} has: {len(t.packages)} packages.")

    # thread1 = threading.Thread(target=deliverPackages, args=(truckList, t1, "08:00 AM"))
    # thread2 = threading.Thread(target=deliverPackages, args=(truckList, t2, "08:00 AM"))

    # thread1.start()
    # thread2.start()

    startGUI(truckList)
    