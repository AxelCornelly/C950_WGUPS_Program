import csv
from PackageClass import Package
from HashTableClass import HashTable

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

def findDistBetween(loc1,loc2) -> float:
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

def nearestNeighbor(currPackage: Package, truckPackages: list[Package]) -> Package:
    """ Determines the next closest package using the nearest-neighbor greedy algorithm.
    
    Args:
        currPackage (Package): The current package to compare to.
        truckPackages (list): The list of packages that are on a truck.
    
    Returns:
        nearest (Package): The package with the nearest address to the current one.
    """
    minDist = float('inf') # Infinity
    nearest = currPackage # Initially set to currentPackage since it is closest to itself.
    
    # Loop through all the packages on the truck calling findDistBetween()
    for package in truckPackages:
        dist = findDistBetween(currPackage.getAddress(), package.getAddress())
        if dist < minDist:
            minDist = dist
            nearest = package
    
    return nearest



if __name__ == "__main__":
    readPackages("WGUPS Package File.csv")
    # packageHash.showContents()
    readDistances("WGUPS Distance Table.csv")
    # for row in addresses:
    #     print(row)
    
    # for row in distances:
    #   print(row)
    
