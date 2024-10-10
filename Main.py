import csv
from PackageClass import Package
from HashTableClass import HashTable

# HashTable data structure to hold package data
packageHash = HashTable()
        
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
    

if __name__ == "__main__":
    readPackages("C950_WGUPS_Program/WGUPS Package File.csv")
    packageHash.showContents()
